import warnings

import requests as r

from .classes import Address, Invoice, Payments, SecretStr, User
from .constants import BASE_URL, TYPES


class Client:
    def __init__(self, token=None):
        self._session = r.Session()
        self.__token = token

    def set_token(self, token):
        self.__token = token

    def me(self):
        """Get your account details and balance."""

        user: dict = self._session.get(
            f"{BASE_URL}/me",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
        ).json()

        try:
            user["nsec"] = SecretStr(user["nsec"])
        except KeyError:
            pass

        return User(**user)

    def post_invoice(
        self,
        type: TYPES = "lightning",
        fiat: bool = False,
        amount: float = -1,
        webhook: str = None,
        secret: str = None,
    ) -> Invoice | Address:
        """Create an invoice.
        Args:
            type: bitcoin or lightning
            fiat: whether the amount is denominated in satoshis or local currency
            amount: amount to be paid
            webhook: remote endpoint to call when the invoice is paid
            secret: a secret value passed to the webhook to authenticate the request

        Returns:
            Invoice (lightning) or Address (bitcoin)
        """

        if amount == -1:
            raise ValueError("amount is required")

        invoice = {}

        invoice["type"] = type
        invoice["fiat"] = fiat
        invoice["amount"] = amount

        if webhook is not None:
            invoice["webhook"] = webhook

        if secret is not None:
            invoice["secret"] = secret

        r = self._session.post(
            f"{BASE_URL}/invoice",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
            json={
                "invoice": {
                    "type": type,
                    "fiat": fiat,
                    "amount": amount,
                    "webhook": webhook,
                    "secret": secret,
                }
            },
        ).json()

        if r["type"] == "lightning":
            return Invoice(**r)
        if r["type"] == "bitcoin":
            return Address(**r)

        raise ValueError("unknown invoice type", r["type"], r)

    def get_invoice(self, hash: str) -> Invoice | Address:
        """Fetch an invoice by passing a bitcoin address or lightning payment hash."""

        r = self._session.get(
            f"{BASE_URL}/invoice/{hash}",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
        ).json()

        if r["type"] == "lightning":
            return Invoice(**r)
        if r["type"] == "bitcoin":
            return Address(**r)

        raise ValueError("unknown invoice type", r["type"], r)

    def post_payment(self, payreq: str) -> Invoice:
        """Send a lightning payment."""

        r = self._session.post(
            f"{BASE_URL}/payments",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
            json={"payreq": payreq},
        ).json()

        if r["type"] == "lightning":
            return Invoice(**r)
        if r["type"] == "bitcoin":
            raise NotImplementedError(
                "bitcoin payments not supported with this endpoint"
            )

        raise ValueError("unknown invoice type", r["type"], r)

    def send(self, amount: float, username: str) -> dict:
        """Send an internal payment to another user."""

        r = self._session.post(
            f"{BASE_URL}/send",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
            json={"amount": amount, "username": username},
        )
        return r.json()

    def bitcoin_payment(self, amount: float, address: str) -> dict:
        """Send a bitcoin payment. This function hasn't been tested."""

        r = self._session.post(
            f"{BASE_URL}/bitcoin/send",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
            json={"amount": amount, "address": address},
        )
        warnings.warn(
            "This function hasn't been tested. Use at your own risk", UserWarning
        )
        return r.json()

    def get_payments(
        self,
        start: int | None = None,
        end: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Payments:
        """Get all payments sent or received by the current user

        Args:
            start: only payments after this unix time
            end: only payments before this unix time
            limit: limit to this integer number of results
            offset: start limiting from this integer offset
        """

        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        r = self._session.get(
            f"{BASE_URL}/payments",
            headers={
                "Authorization": f"Bearer {self.__token}",
                "Content-Type": "application/json",
            },
            params=params,
        )

        return Payments(**r.json())

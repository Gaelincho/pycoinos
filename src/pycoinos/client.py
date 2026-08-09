import warnings

import httpx

from .classes import Address, Invoice, Payments, SecretStr, User
from .constants import BASE_URL, TYPES


class Client:
    def __init__(self, token: str | None = None):
        self.__token = token
        self._client = httpx.AsyncClient(base_url=BASE_URL)

    async def aclose(self):
        await self._client.aclose()

    def set_token(self, token: str):
        self.__token = token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "application/json",
        }

    async def me(self) -> User:
        """Get your account details and balance."""
        resp = await self._client.get("/me", headers=self._headers())
        user: dict = resp.json()

        try:
            user["nsec"] = SecretStr(user["nsec"])
        except KeyError:
            pass

        return User(**user)

    async def post_invoice(
        self,
        type: TYPES = "lightning",
        fiat: bool = False,
        amount: float = -1,
        webhook: str | None = None,
        secret: str | None = None,
    ) -> Invoice | Address:
        """Create an invoice."""

        if amount == -1:
            raise ValueError("amount is required")

        payload = {
            "invoice": {
                "type": type,
                "fiat": fiat,
                "amount": amount,
                "webhook": webhook,
                "secret": secret,
            }
        }

        resp = await self._client.post(
            "/invoice",
            headers=self._headers(),
            json=payload,
        )
        data = resp.json()

        if data["type"] == "lightning":
            return Invoice(**data)
        if data["type"] == "bitcoin":
            return Address(**data)

        raise ValueError("unknown invoice type", data["type"], data)

    async def get_invoice(self, hash: str) -> Invoice | Address:
        """Fetch an invoice."""

        resp = await self._client.get(
            f"/invoice/{hash}",
            headers=self._headers(),
        )
        data = resp.json()

        if data["type"] == "lightning":
            return Invoice(**data)
        if data["type"] == "bitcoin":
            return Address(**data)

        raise ValueError("unknown invoice type", data["type"], data)

    async def post_payment(self, payreq: str) -> Invoice:
        """Send a lightning payment."""

        resp = await self._client.post(
            "/payments",
            headers=self._headers(),
            json={"payreq": payreq},
        )
        data = resp.json()

        if data["type"] == "lightning":
            return Invoice(**data)
        if data["type"] == "bitcoin":
            raise NotImplementedError(
                "bitcoin payments not supported with this endpoint"
            )

        raise ValueError("unknown invoice type", data["type"], data)

    async def send(self, amount: float, username: str) -> dict:
        """Send an internal payment."""

        resp = await self._client.post(
            "/send",
            headers=self._headers(),
            json={"amount": amount, "username": username},
        )
        return resp.json()

    async def bitcoin_payment(self, amount: float, address: str) -> dict:
        """Send a bitcoin payment. Not tested."""

        resp = await self._client.post(
            "/bitcoin/send",
            headers=self._headers(),
            json={"amount": amount, "address": address},
        )
        warnings.warn(
            "This function hasn't been tested. Use at your own risk",
            UserWarning,
        )
        return resp.json()

    async def get_payments(
        self,
        start: int | None = None,
        end: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Payments:
        """Get all payments."""

        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        resp = await self._client.get(
            "/payments",
            headers=self._headers(),
            params=params,
        )

        return Payments(**resp.json())

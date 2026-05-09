import warnings
from dataclasses import dataclass
from typing import Any

from .constants import TYPES


class SecretStr:
    def __init__(self, value: str):
        self.__value = value

    def getsecret(self):
        return self.__value

    def __str__(self):
        warnings.warn("You can access the secret value with `getsecret()`", UserWarning)
        return "*" * len(self.__value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__value == other

    def __hash__(self):
        return hash(self.__value)

    def __len__(self):
        return len(self.__value)

    def __bool__(self):
        return bool(self.__value)


@dataclass
class BaseUser:
    currency: str | None = None
    id: str | None = None
    npub: str | None = None
    picture: str | None = None
    pubkey: str | None = None
    username: str | None = None


@dataclass
class User(BaseUser):
    balance: float | None = None
    currencies: list[str] | None = None
    fiat: bool | None = None
    locked: Any | None = None
    locktime: int | None = None
    nsec: SecretStr | None = None
    prompt: bool | None = None


@dataclass
class BaseAddress:
    aid: str | None = None
    amount: float | None = None
    created: int | None = None
    currency: str | None = None
    hash: str | None = None
    id: str | None = None
    items: list | None = None
    own: bool | None = None
    pending: float | None = None
    rate: float | None = None
    received: float | None = None
    text: str | None = None
    tip: Any | None = None
    type: TYPES | None = None
    uid: str | None = None
    user: BaseUser | None = None
    webhook: str | None = None
    secret: str | None = None


@dataclass
class Address(BaseAddress):
    address_type: str | None = None


@dataclass
class Invoice(BaseAddress):
    expiry: int | None = None
    paymentHash: str | None = None
    confirmed: bool | None = None
    fee: float | None = None
    ourfee: float | None = None
    ref: str | None = None


@dataclass
class Payment(Address, Invoice):
    iid: str | None = None
    memo: str | None = None
    hex: str | None = None


@dataclass
class Payments:
    payments: list[Payment] | None = None
    count: int | None = None
    incoming: dict | None = None
    outcoming: dict | None = None

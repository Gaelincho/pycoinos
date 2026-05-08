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
    currency: str
    id: str
    npub: str
    picture: str
    pubkey: str
    username: str


@dataclass
class User(BaseUser):
    balance: float
    currencies: list[str]
    fiat: bool
    locked: Any
    locktime: int
    nsec: SecretStr
    prompt: bool


@dataclass
class BaseAddress:
    aid: str
    amount: float
    created: int
    currency: str
    hash: str
    id: str
    items: list
    own: bool
    pending: float
    rate: float
    received: float
    text: str
    tip: Any
    type: TYPES
    uid: str
    user: BaseUser | None
    webhook: str | None
    secret: str | None


@dataclass
class Address(BaseAddress):
    address_type: str


@dataclass
class Invoice(BaseAddress):
    expiry: int
    paymentHash: str
    confirmed: bool | None
    fee: float | None
    ourfee: float | None
    ref: str | None


@dataclass
class Payment(Address, Invoice):
    iid: str
    memo: str
    hex: str


@dataclass
class Payments:
    payments: list[Payment]
    count: int
    incoming: dict
    outcoming: dict

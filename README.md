# pycoinos

This package serves as a python toolkit for interacting with the [Coinos API](https://coinos.io/docs).

## Usage

The main entry point for the package is the `Client` class. This class provides methods for interacting with the Coinos API.

```python
from pycoinos import Client

client = Client("ey...") # your coinos token
```

The `Client` class has the following methods:

- `me()`: Get your account details and balance.
- `post_invoice()`: Create an invoice (lightning) or address (bitcoin).
- `get_invoice()`: Fetch an invoice by passing a bitcoin address or lightning payment hash.
- `post_payment()`: Send a lightning payment.
- `bitcoin_payment()`: Send a bitcoin payment.
- `send()`: Send an internal payment to another coinos user.
- `get_payments()`: Get all payments sent or received by the current user.
- `set_token()`: Update the token for the client.

## Changelog

- v0.1.0: Initial release

## License

Copyright (c) 2026 Gaelincho

The pycoinos package is distributed under the [MIT License](./LICENSE).

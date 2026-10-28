"""Demonstration digital wallet and payment tracker for Lab 5."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

# The demo PIN is stored as a salted PBKDF2 digest for this lab only.
PIN_SALT = b"lab5-demo-wallet-salt"
WALLET_PIN_HASH = hashlib.pbkdf2_hmac("sha256", b"4321", PIN_SALT, 200_000)
GATEWAY_SECRET = os.environ.get("GATEWAY_SECRET")
CASHBACK_RATE = 0.02
DAILY_LIMIT = 1000
wallet = {"balance": 0.0}
transactions = []


def hash_pin(pin):
    """Return a salted PBKDF2 digest for a wallet PIN."""
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), PIN_SALT, 200_000)


def add_money(amount, source="UPI", log=None):
    """Add a positive amount to the wallet and record the credit."""
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append(
        {
            "type": "credit",
            "amount": amount,
            "party": source,
            "time": datetime.now().isoformat(),
        }
    )
    if log is not None:
        log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the maximum amount allowed for a single payment."""
    global DAILY_LIMIT
    if new_limit >= 0:
        DAILY_LIMIT = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant when the PIN, balance, and daily limit allow it."""
    if not hmac.compare_digest(hash_pin(pin), WALLET_PIN_HASH):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount <= 0 or amount > wallet["balance"] or amount > DAILY_LIMIT:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append(
        {
            "type": "debit",
            "amount": amount,
            "party": merchant,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def mini_statement(count=3):
    """Print the most recent wallet transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, _merchant_type):
    """Return the wallet's standard cashback amount."""
    return round(amount * CASHBACK_RATE, 2)


def check_gateway(secret):
    """Compare a supplied key with the configured gateway key."""
    return GATEWAY_SECRET is not None and hmac.compare_digest(
        secret, GATEWAY_SECRET
    )


def receipt_path():
    """Create a securely named temporary receipt path."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf", delete=False
    ) as receipt_file:
        return receipt_file.name


def main():
    """Run the short, non-interactive wallet demonstration."""
    otp = secrets.randbelow(900_000) + 100_000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()


"""
Strategy Pattern Example: Payment Processing

Demonstrates using the Strategy pattern to implement multiple payment methods
that can be swapped at runtime without changing the shopping cart code.
"""

from abc import ABC, abstractmethod
from typing import Any


class PaymentStrategy(ABC):
    """Abstract payment strategy interface"""

    @abstractmethod
    def pay(self, amount: float) -> dict[str, Any]:
        """Process payment and return result"""


class CreditCardPayment(PaymentStrategy):
    """Credit card payment implementation"""

    def __init__(self, card_number: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount: float) -> dict[str, Any]:
        # Mask card number for display
        masked_card = f"****-****-****-{self.card_number[-4:]}"

        print("\nProcessing credit card payment...")
        print(f"Card: {masked_card}")
        print(f"Amount: ${amount:.2f}")
        print("Authorization: SUCCESS")

        return {
            "method": "Credit Card",
            "card": masked_card,
            "amount": amount,
            "status": "success",
            "transaction_id": "CC-12345",
        }


class PayPalPayment(PaymentStrategy):
    """PayPal payment implementation"""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> dict[str, Any]:
        print("\nProcessing PayPal payment...")
        print(f"PayPal account: {self.email}")
        print(f"Amount: ${amount:.2f}")
        print("Redirecting to PayPal...")
        print("Payment authorized")

        return {
            "method": "PayPal",
            "email": self.email,
            "amount": amount,
            "status": "success",
            "transaction_id": "PP-67890",
        }


class CryptocurrencyPayment(PaymentStrategy):
    """Cryptocurrency payment implementation"""

    def __init__(self, wallet_address: str, currency: str = "BTC"):
        self.wallet_address = wallet_address
        self.currency = currency

    def pay(self, amount: float) -> dict[str, Any]:
        # Simulate conversion rate
        crypto_amount = amount / 50000  # Simplified conversion

        print(f"\nProcessing {self.currency} payment...")
        print(f"Wallet: {self.wallet_address[:10]}...{self.wallet_address[-4:]}")
        print(f"Amount: ${amount:.2f} ({crypto_amount:.8f} {self.currency})")
        print("Waiting for blockchain confirmation...")
        print("Transaction confirmed")

        return {
            "method": "Cryptocurrency",
            "currency": self.currency,
            "wallet": self.wallet_address,
            "amount": amount,
            "crypto_amount": crypto_amount,
            "status": "success",
            "transaction_id": "CRYPTO-ABCDE",
        }


class ShoppingCart:
    """Shopping cart that uses payment strategies"""

    def __init__(self):
        self.items: list[dict[str, Any]] = []
        self.payment_strategy: PaymentStrategy | None = None

    def add_item(self, name: str, price: float, quantity: int = 1):
        """Add item to cart"""
        self.items.append({"name": name, "price": price, "quantity": quantity})
        print(f"Added {quantity}x {name} @ ${price:.2f} each")

    def get_total(self) -> float:
        """Calculate total cart value"""
        return float(sum(item["price"] * item["quantity"] for item in self.items))

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Set the payment strategy to use"""
        self.payment_strategy = strategy

    def checkout(self) -> dict[str, Any]:
        """Process checkout with selected payment strategy"""
        if not self.payment_strategy:
            msg = "No payment method selected"
            raise ValueError(msg)

        if not self.items:
            msg = "Cart is empty"
            raise ValueError(msg)

        total = self.get_total()

        print("\n" + "=" * 60)
        print("CHECKOUT SUMMARY")
        print("=" * 60)
        print("\nItems:")
        for item in self.items:
            print(f"  {item['quantity']}x {item['name']:<30} ${item['price']:.2f}")
        print(f"\nTotal: ${total:.2f}")

        result = self.payment_strategy.pay(total)

        print("\n" + "=" * 60)
        print("PAYMENT SUCCESSFUL")
        print(f"Transaction ID: {result['transaction_id']}")
        print("=" * 60)

        return result


def main():
    """Demonstrate the Strategy pattern with different payment methods"""

    print("=" * 60)
    print("Strategy Pattern: Payment Processing")
    print("=" * 60)

    # Scenario 1: Credit Card Payment
    print("\n--- Scenario 1: Credit Card Payment ---")
    cart1 = ShoppingCart()
    cart1.add_item("Python Programming Book", 49.99)
    cart1.add_item("Laptop Stand", 39.99)
    cart1.add_item("USB-C Cable", 12.99, quantity=2)

    credit_card = CreditCardPayment(
        card_number="1234567812345678", cvv="123", expiry="12/25"
    )
    cart1.set_payment_strategy(credit_card)
    cart1.checkout()

    # Scenario 2: PayPal Payment
    print("\n\n--- Scenario 2: PayPal Payment ---")
    cart2 = ShoppingCart()
    cart2.add_item("Wireless Mouse", 29.99)
    cart2.add_item("Keyboard", 79.99)

    paypal = PayPalPayment("user@example.com")
    cart2.set_payment_strategy(paypal)
    cart2.checkout()

    # Scenario 3: Cryptocurrency Payment
    print("\n\n--- Scenario 3: Cryptocurrency Payment ---")
    cart3 = ShoppingCart()
    cart3.add_item("Software License", 199.99)

    crypto = CryptocurrencyPayment(
        wallet_address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", currency="BTC"
    )
    cart3.set_payment_strategy(crypto)
    cart3.checkout()

    # Scenario 4: Changing Strategy at Runtime
    print("\n\n--- Scenario 4: Switching Payment Methods ---")
    cart4 = ShoppingCart()
    cart4.add_item("Monitor", 299.99)

    print("\nCustomer tries PayPal first...")
    cart4.set_payment_strategy(PayPalPayment("customer@email.com"))

    print("\nCustomer changes mind, switches to credit card...")
    cart4.set_payment_strategy(
        CreditCardPayment(card_number="9876543298765432", cvv="456", expiry="06/26")
    )
    cart4.checkout()

    print("\n\n" + "=" * 60)
    print("Benefits of Strategy Pattern:")
    print("- Payment methods can be swapped at runtime")
    print("- Easy to add new payment methods")
    print("- Shopping cart doesn't depend on specific payment implementations")
    print("- Each payment method is encapsulated in its own class")
    print("- Eliminates conditional statements for payment processing")
    print("=" * 60)


if __name__ == "__main__":
    main()

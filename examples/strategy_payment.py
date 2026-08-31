"""
Strategy Pattern Example: Payment Processing

Demonstrates the library's payment and sorting strategies being swapped at
runtime without changing the code that uses them.
"""

from design_patterns.behavioral.strategy import (
    BubbleSort,
    CreditCardPayment,
    CryptocurrencyPayment,
    DataSorter,
    MergeSort,
    PaymentStrategy,
    PayPalPayment,
    QuickSort,
    ShoppingCart,
    SortStrategy,
)


def checkout_with(prices: list[float], strategy: PaymentStrategy) -> None:
    """Fill a cart with the given prices and pay with the given strategy."""
    cart = ShoppingCart()
    for price in prices:
        cart.add_item(price)
    cart.set_payment_strategy(strategy)
    print(f"  Total ${cart.get_total():.2f} -> {cart.checkout()}")


def main() -> None:
    """Demonstrate the Strategy pattern with payment and sorting strategies"""

    print("=" * 60)
    print("Strategy Pattern: Payment Processing")
    print("=" * 60)

    print("\n--- Scenario 1: Credit Card Payment ---")
    checkout_with([49.99, 39.99, 12.99, 12.99], CreditCardPayment("1234567812345678"))

    print("\n--- Scenario 2: PayPal Payment ---")
    checkout_with([29.99, 79.99], PayPalPayment("user@example.com"))

    print("\n--- Scenario 3: Cryptocurrency Payment ---")
    checkout_with([199.99], CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"))

    print("\n--- Scenario 4: Switching Payment Methods ---")
    cart = ShoppingCart()
    cart.add_item(299.99)
    print("Customer tries PayPal first...")
    cart.set_payment_strategy(PayPalPayment("customer@example.com"))
    print("Customer changes mind, switches to credit card...")
    cart.set_payment_strategy(CreditCardPayment("9876543298765432"))
    print(f"  {cart.checkout()}")

    print("\n--- Scenario 5: Sorting Strategies ---")
    data = [64, 34, 25, 12, 22, 11, 90]
    sorter = DataSorter(BubbleSort())
    strategies: list[SortStrategy] = [BubbleSort(), QuickSort(), MergeSort()]
    for strategy in strategies:
        sorter.set_strategy(strategy)
        print(f"  {type(strategy).__name__:<10} {sorter.sort_data(data)}")

    print("\n" + "=" * 60)
    print("Benefits of Strategy Pattern:")
    print("- Payment methods can be swapped at runtime")
    print("- Easy to add new payment methods")
    print("- Shopping cart doesn't depend on specific payment implementations")
    print("- Each payment method is encapsulated in its own class")
    print("- Eliminates conditional statements for payment processing")
    print("=" * 60)


if __name__ == "__main__":
    main()

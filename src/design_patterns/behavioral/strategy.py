"""Strategy Pattern Module

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes
them interchangeable. Strategy lets the algorithm vary independently from clients that
use it. This pattern is useful when you have multiple ways to perform an operation and
want to choose the appropriate one at runtime.

Example:
    Using different payment strategies:

    ```python
    cart = ShoppingCart()
    cart.add_item(100)
    cart.add_item(50)

    # Pay with credit card
    cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))
    cart.checkout()

    # Pay with PayPal
    cart.set_payment_strategy(PayPalPayment("user@example.com"))
    cart.checkout()
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Abstract base class for payment strategies."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process a payment.

        Args:
            amount: The amount to pay.

        Returns:
            A message indicating payment status.
        """
        pass


class CreditCardPayment(PaymentStrategy):
    """Payment strategy using credit card."""

    def __init__(self, card_number: str) -> None:
        """Initialize credit card payment.

        Args:
            card_number: The credit card number.
        """
        self.card_number = card_number

    def pay(self, amount: float) -> str:
        """Process credit card payment.

        Args:
            amount: The amount to pay.

        Returns:
            Payment confirmation message.
        """
        return f"Paid ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}"


class PayPalPayment(PaymentStrategy):
    """Payment strategy using PayPal."""

    def __init__(self, email: str) -> None:
        """Initialize PayPal payment.

        Args:
            email: The PayPal account email.
        """
        self.email = email

    def pay(self, amount: float) -> str:
        """Process PayPal payment.

        Args:
            amount: The amount to pay.

        Returns:
            Payment confirmation message.
        """
        return f"Paid ${amount:.2f} using PayPal account {self.email}"


class CryptocurrencyPayment(PaymentStrategy):
    """Payment strategy using cryptocurrency."""

    def __init__(self, wallet_address: str) -> None:
        """Initialize cryptocurrency payment.

        Args:
            wallet_address: The cryptocurrency wallet address.
        """
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        """Process cryptocurrency payment.

        Args:
            amount: The amount to pay.

        Returns:
            Payment confirmation message.
        """
        return f"Paid ${amount:.2f} using Crypto wallet {self.wallet_address[:10]}..."


class ShoppingCart:
    """Shopping cart that uses different payment strategies."""

    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        self._items: list[float] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, price: float) -> None:
        """Add an item to the cart.

        Args:
            price: The price of the item.
        """
        self._items.append(price)

    def get_total(self) -> float:
        """Calculate the total price of all items.

        Returns:
            The total price.
        """
        return sum(self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Set the payment strategy.

        Args:
            strategy: The payment strategy to use.
        """
        self._payment_strategy = strategy

    def checkout(self) -> str:
        """Process the payment using the selected strategy.

        Returns:
            Payment confirmation message.

        Raises:
            ValueError: If no payment strategy is set.
        """
        if self._payment_strategy is None:
            raise ValueError("Payment strategy not set")

        total = self.get_total()
        if total == 0:
            return "Cart is empty"

        return self._payment_strategy.pay(total)


class SortStrategy(ABC):
    """Abstract base class for sorting strategies."""

    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        """Sort the given data.

        Args:
            data: The list of integers to sort.

        Returns:
            The sorted list.
        """
        pass


class BubbleSort(SortStrategy):
    """Bubble sort algorithm strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Sort using bubble sort.

        Args:
            data: The list to sort.

        Returns:
            The sorted list.
        """
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSort(SortStrategy):
    """Quick sort algorithm strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Sort using quick sort.

        Args:
            data: The list to sort.

        Returns:
            The sorted list.
        """
        if len(data) <= 1:
            return data.copy()

        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]

        return self.sort(left) + middle + self.sort(right)


class MergeSort(SortStrategy):
    """Merge sort algorithm strategy."""

    def sort(self, data: list[int]) -> list[int]:
        """Sort using merge sort.

        Args:
            data: The list to sort.

        Returns:
            The sorted list.
        """
        if len(data) <= 1:
            return data.copy()

        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])

        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        """Merge two sorted lists.

        Args:
            left: First sorted list.
            right: Second sorted list.

        Returns:
            Merged sorted list.
        """
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class DataSorter:
    """Context class that uses different sorting strategies."""

    def __init__(self, strategy: SortStrategy) -> None:
        """Initialize with a sorting strategy.

        Args:
            strategy: The sorting strategy to use.
        """
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change the sorting strategy.

        Args:
            strategy: The new sorting strategy.
        """
        self._strategy = strategy

    def sort_data(self, data: list[int]) -> list[int]:
        """Sort data using the current strategy.

        Args:
            data: The list to sort.

        Returns:
            The sorted list.
        """
        return self._strategy.sort(data)

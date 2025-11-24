# Strategy Pattern

**Category:** Behavioral Pattern

## Overview

Define a family of algorithms, encapsulate each one, and make them interchangeable. This pattern lets algorithms vary independently from clients that use them, enabling runtime selection of behavior without complex conditional logic.

## Usage Guidelines

**Use when:**

- Multiple ways to perform an operation need to be chosen at runtime
- Code contains many conditionals that select behavior variants
- Related algorithms share a common interface but differ in implementation
- Algorithm implementation details should be isolated from client code

**Avoid when:**

- Only one way to perform the operation exists
- The algorithm is trivial and doesn't justify abstraction
- The behavior never changes or has no variants
- The indirection overhead is unacceptable for performance

## Implementation

```python
from abc import ABC, abstractmethod

# Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

# Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using PayPal account {self.email}"

class CryptocurrencyPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using Crypto wallet {self.wallet_address[:10]}..."

# Context
class ShoppingCart:
    def __init__(self):
        self._items: list[float] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, price: float) -> None:
        self._items.append(price)

    def get_total(self) -> float:
        return sum(self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy

    def checkout(self) -> str:
        if self._payment_strategy is None:
            raise ValueError("Payment strategy not set")

        total = self.get_total()
        if total == 0:
            return "Cart is empty"

        return self._payment_strategy.pay(total)
```

### Usage

```python
# Create shopping cart
cart = ShoppingCart()
cart.add_item(100.00)
cart.add_item(50.00)

# Pay with credit card
cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))
print(cart.checkout())  # Paid $150.00 using Credit Card ending in 3456

# Change strategy to PayPal
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())  # Paid $150.00 using PayPal account user@example.com

# Change strategy to Cryptocurrency
cart.set_payment_strategy(CryptocurrencyPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"))
print(cart.checkout())  # Paid $150.00 using Crypto wallet 0x742d35Cc...
```

## Trade-offs

**Benefits:**

1. Algorithms can be switched at runtime for flexibility
2. New strategies can be added without modifying context (Open/Closed Principle)
3. Eliminates complex conditional logic through clean object composition
4. Each strategy can be tested independently

**Drawbacks:**

1. Creates many strategy objects increasing class count
2. Clients must understand different strategies to select appropriately
3. Context and strategy must share data with communication overhead
4. Overkill for simple algorithms that rarely change

## Real-World Examples

- Sorting algorithms choosing between bubble sort, quick sort, merge sort
- Compression algorithm selection (ZIP, RAR, TAR)
- Route planning with different strategies (shortest, fastest, scenic)
- Authentication methods (OAuth, JWT, Basic Auth)

## Related Patterns

- State
- Template Method
- Command
- Factory

## API Reference

::: design_patterns.behavioral.strategy
    options:
      show_root_heading: true
      show_source: true

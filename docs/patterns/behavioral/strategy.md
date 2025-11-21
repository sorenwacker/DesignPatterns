# Strategy Pattern

**Category:** Behavioral Pattern

## Intent

Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it, enabling runtime selection of algorithms.

## Problem

When you have multiple ways to perform an operation, hardcoding the logic leads to:

- Inflexible code with multiple conditional statements
- Difficulty adding new algorithms without modifying existing code
- Coupling between the context and specific algorithm implementations
- Complex testing as all variations must be tested together

## When to Use

Use the Strategy pattern when:

- **Multiple algorithms**: You have different ways to perform an operation and need to choose at runtime
- **Conditional complexity**: Your code contains many conditionals that select behavior variants
- **Algorithm isolation**: You want to isolate algorithm implementation details from client code
- **Runtime flexibility**: The behavior needs to be selected or changed at runtime
- **Algorithm families**: Related algorithms share a common interface but differ in implementation
- **Client customization**: Different clients need different variations of an algorithm

## When NOT to Use

Avoid the Strategy pattern when:

- **Single algorithm**: Only one way to perform the operation exists
- **Simple logic**: The algorithm is trivial and doesn't justify abstraction
- **Stable requirements**: The behavior never changes or has no variants
- **Performance critical**: The indirection overhead is unacceptable
- **Increased objects**: Creating many strategy objects adds unwanted complexity

## Structure

The Strategy pattern involves:

- **Strategy Interface**: Declares method(s) common to all algorithms
- **Concrete Strategies**: Implement different variations of the algorithm
- **Context**: Maintains a reference to a strategy object and delegates work to it

## Implementation

### Payment Strategy Example

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

### Usage Example

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

## Key Benefits

1. **Runtime flexibility**: Algorithms can be switched at runtime
2. **Open/Closed Principle**: New strategies can be added without modifying context
3. **Eliminates conditionals**: Replaces complex conditional logic with clean object composition
4. **Testability**: Each strategy can be tested independently
5. **Reusability**: Strategies can be reused across different contexts
6. **Encapsulation**: Algorithm implementation details are hidden

## Drawbacks

1. **Increased objects**: Creates many strategy objects
2. **Client awareness**: Clients must understand different strategies to select appropriately
3. **Communication overhead**: Context and strategy must share data
4. **Simple cases**: Overkill for simple algorithms that rarely change
5. **Context dependency**: Strategies may depend on context data structure

## Real-World Examples

- **Sorting algorithms**: Choosing between bubble sort, quick sort, merge sort based on data size
- **Compression**: Selecting compression algorithm (ZIP, RAR, TAR) based on requirements
- **Route planning**: Different navigation strategies (shortest, fastest, scenic)
- **Authentication**: Multiple authentication methods (OAuth, JWT, Basic Auth)
- **Pricing strategies**: Different pricing rules (regular, discount, wholesale)
- **Validation**: Different validation strategies for various input types

## Related Patterns

- **State**: Similar structure but intent differs (Strategy focuses on algorithms, State on behavior changes)
- **Template Method**: Defines algorithm structure in base class vs encapsulating complete algorithms
- **Command**: Encapsulates requests vs encapsulating algorithms
- **Factory**: Can be used to create appropriate strategy instances

## API Reference

::: design_patterns.behavioral.strategy
    options:
      show_root_heading: true
      show_source: true

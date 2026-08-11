"""Tests for the Strategy pattern."""

import pytest

from design_patterns.behavioral.strategy import (
    BubbleSort,
    CreditCardPayment,
    CryptocurrencyPayment,
    DataSorter,
    MergeSort,
    PayPalPayment,
    QuickSort,
    ShoppingCart,
)


def test_credit_card_payment():
    """Test credit card payment strategy."""
    payment = CreditCardPayment("1234-5678-9012-3456")
    result = payment.pay(100.0)
    assert "Credit Card ending in 3456" in result
    assert "$100.00" in result


def test_paypal_payment():
    """Test PayPal payment strategy."""
    payment = PayPalPayment("user@example.com")
    result = payment.pay(50.50)
    assert "PayPal account user@example.com" in result
    assert "$50.50" in result


def test_cryptocurrency_payment():
    """Test cryptocurrency payment strategy."""
    payment = CryptocurrencyPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
    result = payment.pay(250.75)
    assert "Crypto wallet" in result
    assert "$250.75" in result


def test_shopping_cart_add_items():
    """Test adding items to shopping cart."""
    cart = ShoppingCart()
    cart.add_item(100.0)
    cart.add_item(50.0)
    assert cart.get_total() == 150.0


def test_shopping_cart_empty():
    """Test empty shopping cart."""
    cart = ShoppingCart()
    assert cart.get_total() == 0.0


def test_shopping_cart_checkout_without_strategy():
    """Test checkout without setting payment strategy."""
    cart = ShoppingCart()
    cart.add_item(100.0)

    with pytest.raises(ValueError, match="Payment strategy not set"):
        cart.checkout()


def test_shopping_cart_checkout_with_credit_card():
    """Test checkout with credit card."""
    cart = ShoppingCart()
    cart.add_item(100.0)
    cart.add_item(50.0)
    cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))

    result = cart.checkout()
    assert "$150.00" in result
    assert "Credit Card" in result


def test_shopping_cart_checkout_with_paypal():
    """Test checkout with PayPal."""
    cart = ShoppingCart()
    cart.add_item(75.0)
    cart.set_payment_strategy(PayPalPayment("test@example.com"))

    result = cart.checkout()
    assert "$75.00" in result
    assert "PayPal" in result


def test_shopping_cart_empty_checkout():
    """Test checkout with empty cart."""
    cart = ShoppingCart()
    cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))

    result = cart.checkout()
    assert result == "Cart is empty"


def test_bubble_sort():
    """Test bubble sort strategy."""
    sorter = DataSorter(BubbleSort())
    data = [64, 34, 25, 12, 22, 11, 90]
    result = sorter.sort_data(data)
    assert result == [11, 12, 22, 25, 34, 64, 90]
    assert data == [64, 34, 25, 12, 22, 11, 90]  # Original unchanged


def test_quick_sort():
    """Test quick sort strategy."""
    sorter = DataSorter(QuickSort())
    data = [64, 34, 25, 12, 22, 11, 90]
    result = sorter.sort_data(data)
    assert result == [11, 12, 22, 25, 34, 64, 90]


def test_merge_sort():
    """Test merge sort strategy."""
    sorter = DataSorter(MergeSort())
    data = [64, 34, 25, 12, 22, 11, 90]
    result = sorter.sort_data(data)
    assert result == [11, 12, 22, 25, 34, 64, 90]


def test_sort_strategy_change():
    """Test changing sort strategy at runtime."""
    sorter = DataSorter(BubbleSort())
    data = [5, 3, 8, 1]

    result1 = sorter.sort_data(data)
    assert result1 == [1, 3, 5, 8]

    sorter.set_strategy(QuickSort())
    result2 = sorter.sort_data(data)
    assert result2 == [1, 3, 5, 8]


def test_sort_empty_list():
    """Test sorting an empty list."""
    sorter = DataSorter(QuickSort())
    result = sorter.sort_data([])
    assert result == []


def test_sort_single_element():
    """Test sorting a single element."""
    sorter = DataSorter(MergeSort())
    result = sorter.sort_data([42])
    assert result == [42]


def test_sort_already_sorted():
    """Test sorting already sorted data."""
    sorter = DataSorter(BubbleSort())
    data = [1, 2, 3, 4, 5]
    result = sorter.sort_data(data)
    assert result == [1, 2, 3, 4, 5]

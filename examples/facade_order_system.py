"""
Facade Pattern Example: Order Processing System

Demonstrates using the Facade pattern to simplify a complex order processing
system that involves multiple subsystems (inventory, payment, shipping, notifications).
"""

from datetime import datetime

# ============================================================================
# COMPLEX SUBSYSTEMS
# ============================================================================


class InventoryService:
    """Manages product inventory"""

    def __init__(self):
        self.inventory = {
            "LAPTOP-001": {"name": "Laptop", "quantity": 10, "price": 999.99},
            "MOUSE-002": {"name": "Mouse", "quantity": 50, "price": 29.99},
            "KEYBOARD-003": {"name": "Keyboard", "quantity": 30, "price": 79.99},
        }

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product is available"""
        print(f"  [Inventory] Checking availability of {product_id} (qty: {quantity})")
        if product_id not in self.inventory:
            print(f"  [Inventory] Product {product_id} not found")
            return False

        available = self.inventory[product_id]["quantity"] >= quantity
        if available:
            print(
                f"  [Inventory] ✓ Available: {self.inventory[product_id]['quantity']} in stock"
            )
        else:
            print("  [Inventory] ✗ Insufficient stock")
        return available

    def reserve_items(self, product_id: str, quantity: int) -> bool:
        """Reserve items from inventory"""
        print(f"  [Inventory] Reserving {quantity}x {product_id}")
        if self.check_availability(product_id, quantity):
            self.inventory[product_id]["quantity"] -= quantity
            print(
                f"  [Inventory] ✓ Reserved. Remaining: {self.inventory[product_id]['quantity']}"
            )
            return True
        return False

    def get_price(self, product_id: str) -> float:
        """Get product price"""
        return self.inventory.get(product_id, {}).get("price", 0.0)


class PaymentService:
    """Processes payments"""

    def validate_payment_info(self, payment_info: dict) -> bool:
        """Validate payment information"""
        print("  [Payment] Validating payment information...")
        required_fields = ["card_number", "cvv", "expiry"]
        for field in required_fields:
            if field not in payment_info:
                print(f"  [Payment] ✗ Missing field: {field}")
                return False
        print("  [Payment] ✓ Payment information valid")
        return True

    def charge(self, amount: float, payment_info: dict) -> dict:
        """Charge the payment method"""
        print(f"  [Payment] Processing charge of ${amount:.2f}")
        # Simulate payment processing
        masked_card = f"****-****-****-{payment_info['card_number'][-4:]}"
        print(f"  [Payment] Card: {masked_card}")
        print("  [Payment] ✓ Charge successful")

        return {
            "transaction_id": f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": amount,
            "status": "completed",
        }

    def refund(self, transaction_id: str) -> bool:
        """Process a refund"""
        print(f"  [Payment] Processing refund for {transaction_id}")
        print("  [Payment] ✓ Refund processed")
        return True


class ShippingService:
    """Manages shipping"""

    def calculate_shipping_cost(self, weight: float, destination: str) -> float:
        """Calculate shipping cost"""
        print(f"  [Shipping] Calculating cost for {destination}")
        base_cost = 5.99
        weight_cost = weight * 0.50
        total = base_cost + weight_cost
        print(f"  [Shipping] Cost: ${total:.2f}")
        return total

    def create_shipment(self, order_id: str, address: dict) -> str:
        """Create a shipment"""
        print(f"  [Shipping] Creating shipment for order {order_id}")
        print(f"  [Shipping] Destination: {address['city']}, {address['state']}")

        tracking_number = f"TRACK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"  [Shipping] ✓ Shipment created: {tracking_number}")
        return tracking_number

    def schedule_pickup(self, tracking_number: str) -> datetime:
        """Schedule package pickup"""
        print(f"  [Shipping] Scheduling pickup for {tracking_number}")
        pickup_time = datetime.now()
        print("  [Shipping] ✓ Pickup scheduled")
        return pickup_time


class NotificationService:
    """Sends notifications"""

    def send_order_confirmation(self, email: str, order_id: str) -> None:
        """Send order confirmation email"""
        print(f"  [Notification] Sending order confirmation to {email}")
        print(f"  [Notification] Order ID: {order_id}")
        print("  [Notification] ✓ Email sent")

    def send_shipping_notification(self, email: str, tracking_number: str) -> None:
        """Send shipping notification"""
        print(f"  [Notification] Sending shipping notification to {email}")
        print(f"  [Notification] Tracking: {tracking_number}")
        print("  [Notification] ✓ Email sent")

    def send_error_notification(self, email: str, error: str) -> None:
        """Send error notification"""
        print(f"  [Notification] Sending error notification to {email}")
        print(f"  [Notification] Error: {error}")
        print("  [Notification] ✓ Email sent")


# ============================================================================
# FACADE
# ============================================================================


class OrderFacade:
    """
    Facade that simplifies the complex order processing workflow.
    Coordinates multiple subsystems to process orders.
    """

    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
        self.notifications = NotificationService()
        self.order_counter = 1000

    def place_order(
        self,
        customer_email: str,
        items: list[dict],
        payment_info: dict,
        shipping_address: dict,
    ) -> dict:
        """
        Simplified interface for placing an order.
        Handles all the complexity of coordinating multiple services.
        """
        order_id = f"ORDER-{self.order_counter}"
        self.order_counter += 1

        print(f"\n{'='*70}")
        print(f"Processing Order: {order_id}")
        print(f"{'='*70}")

        try:
            # Step 1: Validate payment information
            print("\nStep 1: Validating Payment")
            if not self.payment.validate_payment_info(payment_info):
                raise ValueError("Invalid payment information")

            # Step 2: Check inventory
            print("\nStep 2: Checking Inventory")
            total_amount = 0
            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]

                if not self.inventory.check_availability(product_id, quantity):
                    raise ValueError(
                        f"Product {product_id} not available in requested quantity"
                    )

                price = self.inventory.get_price(product_id)
                total_amount += price * quantity

            # Step 3: Calculate shipping
            print("\nStep 3: Calculating Shipping")
            total_weight = sum(item.get("weight", 1.0) for item in items)
            shipping_cost = self.shipping.calculate_shipping_cost(
                total_weight, shipping_address["state"]
            )
            total_amount += shipping_cost

            # Step 4: Process payment
            print("\nStep 4: Processing Payment")
            payment_result = self.payment.charge(total_amount, payment_info)

            # Step 5: Reserve inventory
            print("\nStep 5: Reserving Items")
            for item in items:
                if not self.inventory.reserve_items(
                    item["product_id"], item["quantity"]
                ):
                    # Rollback: refund payment
                    self.payment.refund(payment_result["transaction_id"])
                    raise ValueError(f"Failed to reserve {item['product_id']}")

            # Step 6: Create shipment
            print("\nStep 6: Creating Shipment")
            tracking_number = self.shipping.create_shipment(order_id, shipping_address)
            self.shipping.schedule_pickup(tracking_number)

            # Step 7: Send notifications
            print("\nStep 7: Sending Notifications")
            self.notifications.send_order_confirmation(customer_email, order_id)
            self.notifications.send_shipping_notification(
                customer_email, tracking_number
            )

            # Success!
            result = {
                "order_id": order_id,
                "status": "success",
                "total_amount": total_amount,
                "tracking_number": tracking_number,
                "transaction_id": payment_result["transaction_id"],
            }

            print(f"\n{'='*70}")
            print(f"✓ Order {order_id} placed successfully!")
            print(f"  Total: ${total_amount:.2f}")
            print(f"  Tracking: {tracking_number}")
            print(f"{'='*70}")

            return result

        except Exception as e:
            print(f"\n{'='*70}")
            print(f"✗ Order failed: {e!s}")
            print(f"{'='*70}")

            # Send error notification
            self.notifications.send_error_notification(customer_email, str(e))

            return {"order_id": order_id, "status": "failed", "error": str(e)}


# ============================================================================
# DEMONSTRATION
# ============================================================================


def main():
    """Demonstrate the Facade pattern simplifying complex order processing"""

    print("=" * 70)
    print("Facade Pattern: Order Processing System")
    print("=" * 70)

    # Create the facade
    order_system = OrderFacade()

    # Scenario 1: Successful order
    print("\n\n--- Scenario 1: Successful Order ---")

    result1 = order_system.place_order(
        customer_email="alice@example.com",
        items=[
            {"product_id": "LAPTOP-001", "quantity": 1, "weight": 5.0},
            {"product_id": "MOUSE-002", "quantity": 2, "weight": 0.3},
        ],
        payment_info={
            "card_number": "1234567812345678",
            "cvv": "123",
            "expiry": "12/25",
        },
        shipping_address={
            "street": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105",
        },
    )

    # Scenario 2: Failed order (insufficient stock)
    print("\n\n--- Scenario 2: Order with Insufficient Stock ---")

    result2 = order_system.place_order(
        customer_email="bob@example.com",
        items=[
            {"product_id": "LAPTOP-001", "quantity": 50, "weight": 5.0}  # Too many
        ],
        payment_info={
            "card_number": "9876543298765432",
            "cvv": "456",
            "expiry": "06/26",
        },
        shipping_address={
            "street": "456 Oak Ave",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
        },
    )

    # Scenario 3: Another successful order
    print("\n\n--- Scenario 3: Another Successful Order ---")

    result3 = order_system.place_order(
        customer_email="charlie@example.com",
        items=[{"product_id": "KEYBOARD-003", "quantity": 1, "weight": 1.5}],
        payment_info={
            "card_number": "5555444433332222",
            "cvv": "789",
            "expiry": "09/27",
        },
        shipping_address={
            "street": "789 Elm Dr",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
        },
    )

    # Summary
    print("\n\n" + "=" * 70)
    print("Benefits of Facade Pattern:")
    print("- Simple interface to complex subsystem")
    print("- Client code doesn't need to know about all subsystems")
    print("- Easy to change subsystem implementations")
    print("- Reduces coupling between client and subsystems")
    print("- Coordinates complex workflows in one place")
    print("=" * 70)

    print("\n\nWithout Facade, clients would need to:")
    print("1. Manually coordinate 4 different services")
    print("2. Understand the workflow and order of operations")
    print("3. Handle error conditions and rollbacks")
    print("4. Know all the details of each subsystem")
    print("\nWith Facade, clients just call: order_system.place_order()")


if __name__ == "__main__":
    main()

"""
Observer Pattern Example: Event Notification System

Demonstrates using the Observer pattern to build an event system where
multiple components can react to user events without tight coupling.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List


class Observer(ABC):
    """Abstract observer interface"""

    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Called when an event occurs"""
        pass


class Subject:
    """Subject that observers can subscribe to"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Add an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Attached observer: {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        """Remove an observer"""
        self._observers.remove(observer)
        print(f"Detached observer: {observer.__class__.__name__}")

    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notify all observers of an event"""
        print(f"\n[EVENT] {event_type}")
        for observer in self._observers:
            observer.update(event_type, data)


class UserService(Subject):
    """User service that generates events"""

    def register_user(self, email: str, name: str) -> None:
        """Register a new user and notify observers"""
        user_data = {
            "email": email,
            "name": name,
            "timestamp": datetime.now().isoformat(),
        }
        print(f"\nRegistering user: {name} ({email})")
        self.notify("user_registered", user_data)

    def user_logged_in(self, email: str) -> None:
        """User login event"""
        login_data = {"email": email, "timestamp": datetime.now().isoformat()}
        print(f"\nUser logged in: {email}")
        self.notify("user_logged_in", login_data)

    def user_made_purchase(self, email: str, amount: float, item: str) -> None:
        """User purchase event"""
        purchase_data = {
            "email": email,
            "amount": amount,
            "item": item,
            "timestamp": datetime.now().isoformat(),
        }
        print(f"\nUser {email} purchased {item} for ${amount:.2f}")
        self.notify("user_made_purchase", purchase_data)


class EmailNotificationObserver(Observer):
    """Sends email notifications for events"""

    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "user_registered":
            self._send_welcome_email(data)
        elif event_type == "user_made_purchase":
            self._send_receipt(data)

    def _send_welcome_email(self, data: Dict[str, Any]) -> None:
        print(
            f"  [EMAIL] Sending welcome email to {data['email']}"
        )
        print(f"          Subject: Welcome {data['name']}!")

    def _send_receipt(self, data: Dict[str, Any]) -> None:
        print(
            f"  [EMAIL] Sending receipt to {data['email']}"
        )
        print(
            f"          Subject: Your purchase of {data['item']} (${data['amount']:.2f})"
        )


class AnalyticsObserver(Observer):
    """Tracks analytics for events"""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        event_record = {"type": event_type, "data": data}
        self.events.append(event_record)
        print(f"  [ANALYTICS] Logged {event_type} event")

        if event_type == "user_registered":
            print(f"              New user: {data['name']}")
        elif event_type == "user_made_purchase":
            print(
                f"              Revenue: ${data['amount']:.2f}"
            )

    def get_summary(self) -> Dict[str, int]:
        """Get event summary"""
        summary = {}
        for event in self.events:
            event_type = event["type"]
            summary[event_type] = summary.get(event_type, 0) + 1
        return summary


class DatabaseObserver(Observer):
    """Persists events to database"""

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        record = {
            "event_type": event_type,
            "data": data,
            "recorded_at": datetime.now().isoformat(),
        }
        self.records.append(record)
        print(
            f"  [DATABASE] Saved {event_type} to database (Record #{len(self.records)})"
        )


class AdminNotificationObserver(Observer):
    """Notifies admins of important events"""

    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "user_registered":
            print(
                f"  [ADMIN] New user registered: {data['name']}"
            )

        if event_type == "user_made_purchase":
            if data["amount"] > 100:
                print(
                    f"  [ADMIN] High-value purchase alert: ${data['amount']:.2f}"
                )


def main():
    """Demonstrate the Observer pattern with event system"""

    print("=" * 70)
    print("Observer Pattern: Event Notification System")
    print("=" * 70)

    # Create the subject (user service)
    user_service = UserService()

    # Create observers
    print("\n--- Setting up observers ---")
    email_observer = EmailNotificationObserver()
    analytics_observer = AnalyticsObserver()
    database_observer = DatabaseObserver()
    admin_observer = AdminNotificationObserver()

    # Attach observers
    user_service.attach(email_observer)
    user_service.attach(analytics_observer)
    user_service.attach(database_observer)
    user_service.attach(admin_observer)

    # Generate events
    print("\n\n" + "=" * 70)
    print("Triggering Events")
    print("=" * 70)

    # Event 1: User registration
    user_service.register_user("alice@example.com", "Alice Smith")

    # Event 2: User login
    user_service.user_logged_in("alice@example.com")

    # Event 3: User purchase
    user_service.user_made_purchase("alice@example.com", 49.99, "Python Book")

    # Event 4: Another user registration
    user_service.register_user("bob@example.com", "Bob Johnson")

    # Event 5: High-value purchase
    user_service.user_made_purchase("bob@example.com", 299.99, "Laptop")

    # Event 6: Another login
    user_service.user_logged_in("bob@example.com")

    # Show analytics summary
    print("\n\n" + "=" * 70)
    print("Analytics Summary")
    print("=" * 70)
    summary = analytics_observer.get_summary()
    for event_type, count in summary.items():
        print(f"  {event_type}: {count}")

    print(f"\nTotal events tracked: {len(analytics_observer.events)}")
    print(f"Total database records: {len(database_observer.records)}")

    # Demonstrate dynamic observer management
    print("\n\n" + "=" * 70)
    print("Dynamic Observer Management")
    print("=" * 70)

    print("\n--- Detaching admin observer ---")
    user_service.detach(admin_observer)

    print("\n--- Triggering event without admin observer ---")
    user_service.user_made_purchase("alice@example.com", 199.99, "Monitor")

    print("\n\n" + "=" * 70)
    print("Benefits of Observer Pattern:")
    print("- Loose coupling between subject and observers")
    print("- Easy to add/remove observers at runtime")
    print("- Observers can be reused across different subjects")
    print("- Subject doesn't need to know about observer implementations")
    print("- Supports broadcast communication")
    print("=" * 70)


if __name__ == "__main__":
    main()

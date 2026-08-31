"""
Observer Pattern Example: Event Notification System

Demonstrates the library's Subject and Observer being used to build an event
system where several components react to user events without tight coupling.
"""

from datetime import datetime
from typing import Any

from design_patterns.behavioral.observer import Observer, Subject


class UserService(Subject):
    """Subject that records the latest user event and notifies observers"""

    def __init__(self) -> None:
        super().__init__()
        self.event_type: str = ""
        self.event_data: dict[str, Any] = {}

    def _emit(self, event_type: str, data: dict[str, Any]) -> None:
        self.event_type = event_type
        self.event_data = {**data, "timestamp": datetime.now().isoformat()}
        print(f"\n[EVENT] {event_type}")
        self.notify()

    def register_user(self, email: str, name: str) -> None:
        """Register a new user and notify observers"""
        print(f"\nRegistering user: {name} ({email})")
        self._emit("user_registered", {"email": email, "name": name})

    def user_logged_in(self, email: str) -> None:
        """User login event"""
        print(f"\nUser logged in: {email}")
        self._emit("user_logged_in", {"email": email})

    def user_made_purchase(self, email: str, amount: float, item: str) -> None:
        """User purchase event"""
        print(f"\nUser {email} purchased {item} for ${amount:.2f}")
        self._emit(
            "user_made_purchase", {"email": email, "amount": amount, "item": item}
        )


class EventObserver(Observer):
    """Observer that reads the event a UserService just emitted"""

    def update(self, subject: Subject) -> None:
        if isinstance(subject, UserService):
            self.on_event(subject.event_type, subject.event_data)

    def on_event(self, event_type: str, data: dict[str, Any]) -> None:
        """React to one event; subclasses decide how"""


class EmailNotificationObserver(EventObserver):
    """Sends email notifications for events"""

    def on_event(self, event_type: str, data: dict[str, Any]) -> None:
        if event_type == "user_registered":
            print(f"  [EMAIL] Sending welcome email to {data['email']}")
            print(f"          Subject: Welcome {data['name']}!")
        elif event_type == "user_made_purchase":
            print(f"  [EMAIL] Sending receipt to {data['email']}")
            print(
                f"          Subject: Your purchase of {data['item']} "
                f"(${data['amount']:.2f})"
            )


class AnalyticsObserver(EventObserver):
    """Tracks analytics for events"""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def on_event(self, event_type: str, data: dict[str, Any]) -> None:
        self.events.append({"type": event_type, "data": data})
        print(f"  [ANALYTICS] Logged {event_type} event")
        if event_type == "user_registered":
            print(f"              New user: {data['name']}")
        elif event_type == "user_made_purchase":
            print(f"              Revenue: ${data['amount']:.2f}")

    def get_summary(self) -> dict[str, int]:
        """Get event summary"""
        summary: dict[str, int] = {}
        for event in self.events:
            summary[event["type"]] = summary.get(event["type"], 0) + 1
        return summary


class DatabaseObserver(EventObserver):
    """Persists events to database"""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def on_event(self, event_type: str, data: dict[str, Any]) -> None:
        self.records.append({"event_type": event_type, "data": data})
        print(
            f"  [DATABASE] Saved {event_type} to database (Record #{len(self.records)})"
        )


class AdminNotificationObserver(EventObserver):
    """Notifies admins of important events"""

    def on_event(self, event_type: str, data: dict[str, Any]) -> None:
        if event_type == "user_registered":
            print(f"  [ADMIN] New user registered: {data['name']}")
        if event_type == "user_made_purchase" and data["amount"] > 100:
            print(f"  [ADMIN] High-value purchase alert: ${data['amount']:.2f}")


def main() -> None:
    """Demonstrate the Observer pattern with event system"""

    print("=" * 70)
    print("Observer Pattern: Event Notification System")
    print("=" * 70)

    user_service = UserService()

    print("\n--- Setting up observers ---")
    email_observer = EmailNotificationObserver()
    analytics_observer = AnalyticsObserver()
    database_observer = DatabaseObserver()
    admin_observer = AdminNotificationObserver()
    for observer in (
        email_observer,
        analytics_observer,
        database_observer,
        admin_observer,
    ):
        user_service.attach(observer)
        print(f"Attached observer: {type(observer).__name__}")

    print("\n\n" + "=" * 70)
    print("Triggering Events")
    print("=" * 70)
    user_service.register_user("alice@example.com", "Alice Smith")
    user_service.user_logged_in("alice@example.com")
    user_service.user_made_purchase("alice@example.com", 49.99, "Python Book")
    user_service.register_user("bob@example.com", "Bob Johnson")
    user_service.user_made_purchase("bob@example.com", 299.99, "Laptop")
    user_service.user_logged_in("bob@example.com")

    print("\n\n" + "=" * 70)
    print("Analytics Summary")
    print("=" * 70)
    for event_type, count in analytics_observer.get_summary().items():
        print(f"  {event_type}: {count}")
    print(f"\nTotal events tracked: {len(analytics_observer.events)}")
    print(f"Total database records: {len(database_observer.records)}")

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

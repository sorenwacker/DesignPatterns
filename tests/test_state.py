"""Tests for the State pattern."""

from design_patterns.behavioral.state import Document, TrafficLight


def test_document_initial_state():
    """Test that document starts in draft state."""
    doc = Document()
    assert doc.get_status() == "Draft"


def test_document_publish_from_draft():
    """Test publishing a draft document."""
    doc = Document()
    result = doc.publish()

    assert result == "Document sent for moderation"
    assert doc.get_status() == "Moderation"


def test_document_approve_draft():
    """Test that draft cannot be approved directly."""
    doc = Document()
    result = doc.approve()

    assert "Cannot approve" in result
    assert doc.get_status() == "Draft"


def test_document_approve_from_moderation():
    """Test approving a document in moderation."""
    doc = Document()
    doc.publish()
    result = doc.approve()

    assert "approved and published" in result
    assert doc.get_status() == "Published"


def test_document_reject_from_moderation():
    """Test rejecting a document in moderation."""
    doc = Document()
    doc.publish()
    result = doc.reject()

    assert "rejected" in result
    assert doc.get_status() == "Draft"


def test_document_full_workflow():
    """Test complete document workflow."""
    doc = Document()

    assert doc.get_status() == "Draft"

    doc.publish()
    assert doc.get_status() == "Moderation"

    doc.approve()
    assert doc.get_status() == "Published"


def test_document_reject_published():
    """Test unpublishing a published document."""
    doc = Document()
    doc.publish()
    doc.approve()

    result = doc.reject()
    assert "unpublished" in result
    assert doc.get_status() == "Draft"


def test_document_publish_already_published():
    """Test publishing an already published document."""
    doc = Document()
    doc.publish()
    doc.approve()

    result = doc.publish()
    assert "already published" in result
    assert doc.get_status() == "Published"


def test_document_reject_draft():
    """Test that draft cannot be rejected."""
    doc = Document()
    result = doc.reject()

    assert "Cannot reject" in result
    assert doc.get_status() == "Draft"


def test_traffic_light_initial_state():
    """Test that traffic light starts red."""
    light = TrafficLight()
    assert light.get_color() == "Red"


def test_traffic_light_red_to_green():
    """Test transition from red to green."""
    light = TrafficLight()
    result = light.next()

    assert "Red to Green" in result
    assert light.get_color() == "Green"


def test_traffic_light_green_to_yellow():
    """Test transition from green to yellow."""
    light = TrafficLight()
    light.next()  # Red to Green
    result = light.next()

    assert "Green to Yellow" in result
    assert light.get_color() == "Yellow"


def test_traffic_light_yellow_to_red():
    """Test transition from yellow to red."""
    light = TrafficLight()
    light.next()  # Red to Green
    light.next()  # Green to Yellow
    result = light.next()

    assert "Yellow to Red" in result
    assert light.get_color() == "Red"


def test_traffic_light_full_cycle():
    """Test complete traffic light cycle."""
    light = TrafficLight()

    assert light.get_color() == "Red"

    light.next()
    assert light.get_color() == "Green"

    light.next()
    assert light.get_color() == "Yellow"

    light.next()
    assert light.get_color() == "Red"


def test_traffic_light_multiple_cycles():
    """Test multiple cycles of traffic light."""
    light = TrafficLight()

    for _ in range(3):
        light.next()  # Red to Green
        light.next()  # Green to Yellow
        light.next()  # Yellow to Red

    assert light.get_color() == "Red"

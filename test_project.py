from datetime import date, timedelta

import pytest

from project import (
    CURRENCY,
    MAX_CAKES_PER_DAY,
    MAX_MESSAGE_LENGTH,
    Order,
    calculate_price,
    is_date_available,
    load_orders,
    next_available_date,
    next_order_id,
    save_orders,
    selected_date,
    validate_message,
)



def make_order(order_id=1):
    return Order(order_id, "Anna", "Happy Birthday!", "medium", "floral", date(2026, 11, 20))


def booked(day, count):
    orders = []
    for i in range(count):
        orders.append(Order(i + 1, "Test", "Hi", "small", "plain", day))
    return orders


def test_validate_message():
    assert validate_message("Happy Birthday Anna!") == "Happy Birthday Anna!"
    assert validate_message("Alles Gute, Jürgen!") == "Alles Gute, Jürgen!"
    assert validate_message("  Hi  ") == "  Hi  "  # returned exactly as typed
    assert validate_message("") == ""  # a cake with no message is allowed
    assert validate_message("x" * MAX_MESSAGE_LENGTH) == "x" * MAX_MESSAGE_LENGTH
    with pytest.raises(ValueError):
        validate_message("x" * (MAX_MESSAGE_LENGTH + 1))


def test_calculate_price():
    assert calculate_price("small", "plain") == 25000
    assert calculate_price("medium", "floral") == 50000
    assert calculate_price("large", "fancy") == 72000
    assert calculate_price("small", "custom figurine") == 35000
    with pytest.raises(ValueError):
        calculate_price("giant", "plain")
    with pytest.raises(ValueError):
        calculate_price("small", "sparkly")


def test_selected_date():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    assert selected_date(str(today)) == today
    assert selected_date(str(tomorrow)) == tomorrow
    assert selected_date(f" {tomorrow} ") == tomorrow  # spaces are ignored
    with pytest.raises(ValueError):
        selected_date(str(yesterday))
    with pytest.raises(ValueError):
        selected_date("next friday")
    with pytest.raises(ValueError):
        selected_date("20/11/2030")
    with pytest.raises(ValueError):
        selected_date("")


def test_is_date_available():
    day = date.today() + timedelta(days=7)
    assert is_date_available([], day)
    assert is_date_available(booked(day, MAX_CAKES_PER_DAY - 1), day)
    assert not is_date_available(booked(day, MAX_CAKES_PER_DAY), day)
    # a full day does not affect the next day
    assert is_date_available(booked(day, MAX_CAKES_PER_DAY), day + timedelta(days=1))


def test_next_available_date():
    day = date.today() + timedelta(days=7)
    one_day_full = booked(day, MAX_CAKES_PER_DAY)
    assert next_available_date(one_day_full, day) == day + timedelta(days=1)

    # full days are skipped
    two_days_full = one_day_full + booked(day + timedelta(days=1), MAX_CAKES_PER_DAY)
    assert next_available_date(two_days_full, day) == day + timedelta(days=2)


def test_next_order_id():
    assert next_order_id([]) == 1
    assert next_order_id([make_order(1), make_order(2), make_order(3)]) == 4
    assert next_order_id([make_order(2), make_order(7), make_order(4)]) == 8


def test_order_price():
    assert make_order().price() == 50000


def test_order_message_is_checked():
    with pytest.raises(ValueError):
        Order(1, "Anna", "x" * (MAX_MESSAGE_LENGTH + 1), "small", "plain", date(2026, 11, 20))
    order = Order(1, "Anna", "", "small", "plain", date(2026, 11, 20))
    assert order.message == ""


def test_order_unknown_size():
    order = Order(1, "Anna", "Hi", "giant", "plain", date(2026, 11, 20))
    with pytest.raises(ValueError):
        order.price()


def test_order_to_dict():
    assert make_order().to_dict() == {
        "id": 1,
        "customer": "Anna",
        "message": "Happy Birthday!",
        "size": "medium",
        "design": "floral",
        "collection_date": "2026-11-20",
        "price": 50000,
    }


def test_order_str():
    text = str(make_order())
    assert "Order number : 1" in text
    assert "Customer     : Anna" in text
    assert 'Lettering    : "Happy Birthday!"' in text
    assert "Size         : Medium" in text
    assert "Design       : Floral" in text
    assert "Collection   : 2026-11-20" in text
    assert f"Total cost   : {CURRENCY}50000.00" in text


import json
from datetime import date, timedelta

DATA_FILE = "orders.json"
MAX_CAKES_PER_DAY = 5
MAX_MESSAGE_LENGTH = 40
CURRENCY = "Ks"

SIZES = {"small": 25000, "medium": 45000, "large": 65000}
DESIGNS = {"plain": 0, "floral": 5000,
           "fancy": 7000, "custom figurine": 10000}


def main():
    orders = load_orders()

    print("=== Cherry Bakery Cake Orders ===")
    name = get_name()
    message = get_message()
    size = get_choice("Cake size", SIZES)
    design = get_choice("Cake design (extra cost)", DESIGNS)
    requested_date = get_date()

    # Check the day is not full. This may change the date or cancel the order.
    final_date = choose_date(orders, requested_date)
    if final_date is None:
        print("Order cancelled. Nothing was saved.")
        return

    order = Order(next_order_id(orders), name,
                  message, size, design, final_date)
    orders.append(order)
    save_orders(orders)

    print()
    print(order)


class Order:
    def __init__(self, order_id, customer, message, size, design, collection_date):
        self.order_id = order_id
        self.customer = customer
        self.message = message
        self.size = size
        self.design = design
        self.collection_date = collection_date

    def __str__(self):
        return (
            "=== ORDER CONFIRMED ===\n"
            f"Order number : {self.order_id}\n"
            f"Customer     : {self.customer}\n"
            f'Lettering    : "{self.message}"\n'
            f"Size         : {self.size.title()}\n"
            f"Design       : {self.design.title()}\n"
            f"Collection   : {self.collection_date}\n"
            f"Total cost   : {CURRENCY}{self.price():.2f}"
        )

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = validate_message(message)

    def price(self):
        return calculate_price(self.size, self.design)

    def to_dict(self):
        # JSON can't store an Order, so we turn it into a dictionary
        return {
            "id": self.order_id,
            "customer": self.customer,
            "message": self.message,
            "size": self.size,
            "design": self.design,
            "collection_date": str(self.collection_date),
            "price": self.price(),
        }


def validate_message(text):
    if len(text) > MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Message is too long. Maximum characters is {MAX_MESSAGE_LENGTH}.")
    return text


def calculate_price(size, design):
    if size not in SIZES or design not in DESIGNS:
        raise ValueError("Unavailable size or design")
    return SIZES[size] + DESIGNS[design]


def get_name():
    while True:
        name = input("May I get your name? ").strip()
        if name != "":
            return name
        print("Please enter your name")


def get_message():
    while True:
        try:
            message = validate_message(
                input("What message or name would you like written on the cake? "))
        except ValueError as error:
            print(f"  {error}")
            continue

        # Read it back so the customer can catch any mistake
        print(f' You would like "{message}" written on the cake.')
        answer = input(
            "Just to double-check, is it correct? (yes or no) ").strip().lower()
        if answer == "yes":
            return message


def get_choice(label, options):
    names = list(options)
    print(f"\n{label}:")
    for i in range(len(names)):
        print(f"  {i + 1}. {names[i].title()} ({CURRENCY}{options[names[i]]})")

    while True:
        answer = input(
            "Enter the corresponding number of the option you want: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            return names[int(answer) - 1]
        print(
            f"  Please enter a valid number for options from 1 to {len(names)}.")


def selected_date(text):
    """Turn text like 2026-11-20 into a date. Past dates are not allowed."""
    try:
        day = date.fromisoformat(text.strip())
    except ValueError:
        raise ValueError("Please use the format YYYY-MM-DD")
    if day < date.today():
        raise ValueError("That date has already passed")
    return day


def is_date_available(orders, day):
    """True if fewer than MAX_CAKES_PER_DAY cakes are booked for that day."""
    count = 0
    for order in orders:
        if order.collection_date == day:
            count += 1
    return count < MAX_CAKES_PER_DAY


def next_available_date(orders, day):
    """Add 1 day at a time until we find a day that is not full."""
    day = day + timedelta(days=1)
    while not is_date_available(orders, day):
        day = day + timedelta(days=1)
    return day


def choose_date(orders, day):
    if is_date_available(orders, day):
        return day

    print("That date is fully booked.")
    day = next_available_date(orders, day)
    while True:
        answer = input(
            f"Would {day} work for you? (yes/ no/ cancel): ")
        answer = answer.strip().lower()
        if answer == "yes":
            return day
        elif answer == "no":
            day = next_available_date(orders, day)
        elif answer == "cancel":
            return None
        else:
            print("Please type yes, no or cancel.")


def load_orders(path=DATA_FILE):
    """Read saved orders. If there is no file yet, there are no orders."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    orders = []
    for item in data:
        day = date.fromisoformat(item["collection_date"])
        orders.append(
            Order(item["id"], item["customer"], item["message"],
                  item["size"], item["design"], day)
        )
    return orders


def save_orders(orders, path=DATA_FILE):
    data = []
    for order in orders:
        data.append(order.to_dict())
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def next_order_id(orders):
    highest = 0
    for order in orders:
        if order.order_id > highest:
            highest = order.order_id
    return highest + 1


def get_date():
    while True:
        try:
            return selected_date(input("\nDesired collection date (YYYY-MM-DD): "))
        except ValueError as error:
            print(f"  {error}")


if __name__ == "__main__":
    main()

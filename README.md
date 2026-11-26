# Bakery Order-Entry Program
## CHERRY birthday Cake Order

#### Video Demo: https://youtu.be/yjB3Ap2huHE?si=YGAfNOroZZHISw3l

#### Description:

Cherry Bakery takes cake orders in a paper notebook, and that causes two problems. When staff write down the message a customer wants on the cake, they sometimes hear it wrong or the handwriting is hard to read, so the cake ends up with a mistake. The bakery also has no quick way to see how many cakes are already booked for a day, so it sometimes accepts more orders than it can bake. I wrote this program to fix both problems.

It is a command-line program written in Python. For each order it asks for the customer's name, the message for the cake, the size, the design and the collection date. The message is typed in directly, and then the program shows it back and asks if it is correct. The order does not move on until the answer is yes, so the lettering is exactly what the customer typed. The message can be left empty for a plain cake, but it cannot be longer than 40 characters.

After the date is entered, the program counts the saved orders for that day. The limit is 5 cakes per day. If the day is full, it says so and offers the next day. If the customer says no, it offers the day after that, and it keeps going, skipping any other full days, until the customer says yes or types cancel. Then the order is saved, a confirmation with the exact lettering is printed, and the total cost is worked out from the size and the design. Orders are saved in a JSON file, so the program remembers them the next time it runs.

#### Files

- `project.py` is the whole program.
  - `main()` runs one order from start to finish.
  - `Order` is a class for one cake order. It stores the details, prints the confirmation with `__str__`, checks the message in a setter, works out its price with `price()`, and turns itself into a dictionary with `to_dict()` so it can be saved.
  - `validate_message()` raises an error if the message is too long, and otherwise returns it exactly as typed.
  - `calculate_price()` adds the price of the size and the extra cost of the design.
  - `selected_date()` turns text like 2026-12-05 into a date, and rejects the wrong format or a date in the past.
  - `is_date_available()` counts the orders on a day and checks it against the limit.
  - `next_available_date()` adds one day at a time until it finds a day that is not full.
  - `choose_date()` is the loop that asks if the new date works, and returns the date or `None` if the customer cancels.
  - `load_orders()`, `save_orders()` and `next_order_id()` handle the saved orders.
  - `get_name()`, `get_message()`, `get_choice()` and `get_date()` ask a question again until the answer is valid.
- `test_project.py` has the pytest tests for these functions and for the Order` class`.
- `requirements.txt` lists pytest. The program itself only uses `json` and `datetime`, which come with Python.
- `orders.json` is created by the program the first time an order is saved.

#### Design choices

I used a JSON file to store the orders as it is simple, easy to read, and does not need anything extra to be installed. Each order is saved as a small dictionary, and dates are saved as text and turned back into dates when the file is loaded.

I made the order a class because an order has both information (name, message, size, design, date) and things it needs to do (check its message, work out its price, print itself, convert itself for saving). Putting the check in the message setter means an order can never hold a message that is too long. I also calculate the price when it is needed instead of storing it, so it always matches the size and design.

At first I thought the message should be required, but then I decided not to, because some customers just want a plain cake. So an empty message is allowed and only a too-long message is rejected. I also made `next_available_date` skip full days, because there is no point offering a customer a day that is already booked, and I added a cancel answer so a customer who does not like any of the offered days is not stuck in the loop.

The daily limit, the maximum message length, the currency and the prices are written as constants at the top of `project.py`, so they are easy to change. I also kept functions like `selected_date` and `is_date_available` free of `input()` and `print()`, because that makes them much easier to test.

#### How to run

    pip install -r requirements.txt
    python project.py
    pytest

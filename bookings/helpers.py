def get_seat_cost() -> int:
    return 5


def calc_seats_to_book(required_seats: int, table_seats: int) -> int:
    if required_seats % 2 != 0 and required_seats < table_seats:
        return required_seats + 1
    return required_seats


def calc_total_cost(seat_to_book: int, table_seats: int) -> int:
    cost_per_seat = get_seat_cost()
    if seat_to_book == table_seats:
        return (table_seats - 1) * cost_per_seat
    return seat_to_book * cost_per_seat

"""Utils module"""

from datetime import date, timedelta


def get_last_business_day(day: date | str):
    """Retrieve Last business day"""
    if isinstance(day, str):
        day = date.fromisoformat(day)
    match day.weekday():
        case 6:  # Sunday
            return day - timedelta(days=2)
        case 5:  # Saturday
            return day - timedelta(days=1)
        case _:  # Business Days
            return day

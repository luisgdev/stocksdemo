# Create your tests here.

import pytest
from stocksapi.utils import get_last_business_day


@pytest.mark.parametrize(
    ("input_", "output"),
    (
        ("2024-05-01", "2024-05-01"),
        ("2024-05-02", "2024-05-02"),
        ("2024-05-20", "2024-05-20"),
        ("2024-05-19", "2024-05-17"),
        ("2024-05-18", "2024-05-17"),
        ("2024-05-17", "2024-05-17"),
        ("2024-05-16", "2024-05-16"),
    ),
)
def test__get_last_business_day(input_, output):
    """Test function"""
    assert get_last_business_day(input_).isoformat() == output

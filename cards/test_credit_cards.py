from cards.credit_card import CreditCard
import pytest


def test_format_currency():
    card = CreditCard('Default User', 1, 16, 1000, 500, 250)
    assert card.format_currency(15) == '$15.00'
    assert card.format_currency(1000) == '$1,000.00'

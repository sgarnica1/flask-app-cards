from credit_card import make_report


def print_reports(cards: list) -> None:
    """Print report for each card in a list of cards

    Args:
      list: List of card dictionaries

    Returns:
      None
    """
    counter = 1
    for card in cards:
        print(f'\n- - - TARJETA {counter} - - -')
        make_report(card)
        print("\n")
        counter += 1

from cards.credit_card import CreditCard


class User:
    def __init__(self, name) -> None:
        self.name = name
        self.cards = []

    def add_card(self, card) -> None:
        """Add a Card instance to the user's cards list

        Args:
          card: Card instance of the class CreditCard from credit_card

        Returns:
          None
        """
        self.cards.append(card)

    def delete_card(self, card_number):
        """Deletes a card from the user's cards list based on the card number

        Args:
          card_number: Card's card number

        Returns:
          None
        """
        for card in self.cards:
            current_card_number = card.get_card_number()
            if card_number == current_card_number:
                self.cards.remove(card)

    def print_reports(self) -> None:
        """Print report for each card in a list of cards

        Args:
          list: List of card dictionaries

        Returns:
          None
        """

        for card in self.cards:
            card.export_info()

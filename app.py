import cards.credit_card as card
import cards.user as user

user1 = user.User('Sergio Garnica González')

card1 = card.CreditCard(user1.name, "16", 5000, 3000, 2000)
card2 = card.CreditCard(user1.name, "16", 1000, 2000, 2000)
user1.add_card(card1)
user1.add_card(card2)
user1.print_reports()
user1.delete_card(card1.get_card_number())
user1.print_reports()

import cards.user as user
import cards.credit_card as card
import cards.service_card as scard

user1 = user.User('Sergio Garnica González')

card1 = card.CreditCard(user1.name, 16, 5000, 3000, 2000)
card2 = card.CreditCard(user1.name, 16, 1000, 2000, 2000)
card3 = scard.ServiceCard(user1.name, 6000)
user1.add_card(card1)
user1.add_card(card2)
user1.add_card(card3)

card3.make_report()
card3.partial_payment()
card3.make_report()

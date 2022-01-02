import cards.credit_card as card

card_1 = {
    "name": "Sergio",
    "card_number": "4152313468171276",
    "interest_rate": 16,
    "loan": 6700,
    "payment": 300,
    "new_charges": 20
}
card_2 = {
    "name": "Emilio",
    "interest_rate": 10,
    "loan": 500,
    "payment": 30,
    "new_charges": 20
}
card_3 = {
    "name": "Diego",
    "interest_rate": 12,
    "loan": 500,
    "payment": 300,
    "new_charges": 20
}

card_1 = card.calculate_new_loan(card_1)

card_1 = card.recurrent_payment(card_1)
print(card_1)

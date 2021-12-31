import math


def create_card() -> dict:
    name = input("Nombre del titular: ")
    card_number = input("Número de la tarjeta: ")
    interest_rate = float(input("Tasa de interés: "))
    loan = float(input("Deuda actual: $"))

    invalid = True
    while invalid:
        payment = float(input("Pago a realizar: $"))
        if payment > loan:
            print(
                "No es posible realizar un pago mayor a la deuda actual. Intrpduce una nueva cantidad")
        else:
            invalid = False

    new_charges = float(input("Nuevos cargos: $"))

    return {
        "name": name,
        "card_number": card_number,
        "interest_rate": interest_rate,
        "loan": loan,
        "payment": payment,
        "new_charges": new_charges
    }


def calculate_new_loan(card: dict) -> dict:
    monthly_interest = card["interest_rate"] / 12
    recalculated_loan = (card["loan"] - card["payment"]
                         ) * (1 + monthly_interest)
    new_loan = recalculated_loan + card["new_charges"]
    card["new_loan"] = new_loan
    return card


def make_report(card: dict) -> None:
    card_copy = card.copy()
    for key, value in card.items():
        if key == "name" or key == "interest_rate" or key == "card_number":
            continue
        card_copy[key] = format_currency(value)

    print(f"Nombre del titular: {card_copy['name']}")
    print(f"Tasa de interés: {card_copy['interest_rate']}%")
    print(f"Deuda actual: {card_copy['loan']}")
    print(f"Pago realizado: {card_copy['payment']}")
    print(f"Cargos nuevos: {card_copy['new_charges']}")

    if "new_loan" in card:
        print("\nDEUDA ACTUALIZADA")
        print(f"Próximo pago mensual: {card_copy['new_loan']}")


def format_currency(money: float) -> str:
    return "${:,.2f}".format(money)


def print_reports(cards: list) -> None:
    counter = 1
    for card in cards:
        print(f'\n- - - TARJETA {counter} - - -')
        make_report(card)
        print("\n")
        counter += 1


def recurrent_payment(card: dict) -> dict:
    payment = card["payment"]

    if "new_loan" in card:
        current_loan = card["new_loan"]
    else:
        current_loan = card["loan"]

    counter = 1

    number_of_payments = math.ceil(current_loan / payment)

    while current_loan > 0:
        if current_loan - payment >= 0:
            print(f'Pago {counter} de {number_of_payments}')
            print(f'Deuda actual: {format_currency(current_loan)}')
            print(
                f'Pago: {format_currency(current_loan)} - {format_currency(payment)}')
            print(
                f'Deuda actualizada: {format_currency(current_loan - payment)}\n')
            counter += 1
        else:
            print(f'Pago {counter} de {number_of_payments}')
            print(f'Deuda actual: {format_currency(current_loan)}\n')
            print(f'Último pago de {format_currency(current_loan)}')
        current_loan -= payment

    card["loan"] = 0
    card["payment"] = 0
    card["new_charges"] = 0
    if "new_loan" in card:
        card["new_loan"] = 0

    return card


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

card_1 = calculate_new_loan(card_1)

card_1 = recurrent_payment(card_1)
print(card_1)

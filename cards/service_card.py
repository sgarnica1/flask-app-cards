from cards.credit_card import CreditCard
import random


class ServiceCard(CreditCard):
    def __init__(self, name, user_id, loan) -> None:
        super().__init__(name=name, user_id=user_id, interest_rate=0,
                         loan=loan, payment=0, new_charges=0)
        self.card_number = self.create_card_number()
        self.type = "service"
        self.loan = loan

    def __str__(self) -> str:
        """Prints the information of a card

        Args:
          self

        Returns:
          str
        """

        return f"""
          REPORTE TARJETA CON TERMINACION {self.card_number[-4:]}
          Nombre del titular: {self.name}
          Número de tarjeta: {self.card_number}
          Fecha de vencimiento: {self.expiration_date}
          CVV: {self.cvv}
          Tipo: {self.type}
          Deuda actual: {self.format_currency(self.loan)}
          \n
        """

    def create_card_number(self) -> str:
        """Creates a card number based on random numbers

        Args:
          None

        Returns:
          str: Card number at 16 digits. Firts 8 always the same
        """
        card_number = "48153136"
        for _ in range(8):
            card_number += str(random.randint(0, 9))
        return card_number

    def create_card_dict(self) -> dict:
        """Creates a card based on class constructor

        Args:
          None

        Returns:
          dict: Created card info
        """

        return {
            "name": self.name,
            "card_number": self.card_number,
            "expiration_date": self.expiration_date,
            "cvv": self.cvv,
            "type": self.type,
            "loan": self.loan,
            "payment": self.payment,
        }

    def pay(self):
        invalid = True

        print(
            f'\n- - - PAGO TOTAL DE LA TARJETA CON TERMINACION {self.card_number[-4:]} - - -')
        print(f'Deuda actual: {self.format_currency(self.loan)}')
        while invalid:
            payment = float(
                input("Ingresa la cantidad a pagar (Solo se aceptan pagos totales): $"))
            if payment < self.loan:
                print("Solo se aceptan pagos totales\n")
            elif payment > self.loan:
                print("Tu pago excede la deuda, intenta de nuevo \n")
            else:
                invalid = False
        self.loan = 0.0
        print("\n")
        self.make_report()

    def accept_only_total_payments(func):
        def wrapper(*args, **kwargs):
            print("Solo se pueden realizar pagos totales")
            return
            func(*args, **kwargs)
        return wrapper

    @accept_only_total_payments
    def recurrent_payment(self) -> dict:
        return super().recurrent_payment()

    @accept_only_total_payments
    def partial_payment(self) -> None:
        return super().partial_payment()

from cards.credit_card import CreditCard
import random


class ServiceCard(CreditCard):
    def __init__(self, name, loan) -> None:
        super().__init__(name=name, interest_rate=0,
                         loan=loan, payment=0, new_charges=0)
        self.__card_number = self.__create_card_number()
        self.__type = "Servicios"
        self.loan = loan

    def __create_card_number(self) -> str:
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
            "card_number": self.get_card_number(),
            "expiration_date": self.get_expiration_date(),
            "cvv": self.get_cvv(),
            "type": self.__type,
            "loan": self.loan,
            "payment": self.payment,
        }

    def make_report(self) -> None:
        """Prints the information of a card

        Args:
          dict: Card dictionary

        Returns:
          None
        """

        print(f"Nombre del titular: {self.name}")
        print(f"Número de tarjeta: {self.__card_number}")
        print(f"Fecha de vencimiento: {self.get_expiration_date()}")
        print(f"CVV: {self.get_cvv()}")
        print(f"Tipo: {self.__type}")
        print(f"Deuda actual: {self.format_currency(self.loan)}")
        print("\n\n")

    def pay(self):
        invalid = True

        print(
            f'\n- - - PAGO TOTAL DE LA TARJETA CON TERMINACION {self.__card_number[-4:]} - - -')
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

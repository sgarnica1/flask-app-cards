import math
import random
from datetime import date


class CreditCard:
    def __init__(self, name: str, interest_rate: float, loan: float, payment: float, new_charges: float) -> None:
        self.name = name
        self.__card_number = self.__create_card_number()
        self.__expiration_date = self.__create_expiration_date()
        self.__cvv = self.__create_cvv()
        self.__type = "Crédito"

        self.interest_rate = float(interest_rate)
        self.loan = float(loan)
        if payment > loan:
            self.payment = float(loan)
        else:
            self.payment = float(payment)
        self.new_charges = float(new_charges)
        self.new_loan = self.__calculate_new_loan()

    def __create_card_number(self) -> str:
        """Creates a card number based on random numbers

        Args:
          None

        Returns:
          str: Card number at 16 digits. Firts 8 always the same
        """
        card_number = "41523134"
        for _ in range(8):
            card_number += str(random.randint(0, 9))
        return card_number

    def __create_expiration_date(self) -> str:
        """Creates card's expiration date based on current date and adding 5 years to the current year. 

        Args:
          None

        Returns:
          str: Card's expiration date in the following format mm/yy
        """
        cdate = date.today()
        cdate = str(cdate).split("-")

        # Get year and month from current date. Add 5 years to the year variable
        year = str(int(cdate[0]) + 5)
        month = cdate[1]

        return f"{month}/{year[2:4]}"

    def __create_cvv(self) -> str:
        """Creates card's cvv based on 3 random numbers

        Args:
          None

        Returns:
          str: Card's cvv 
        """
        cvv = ""
        for _ in range(3):
            cvv += str(random.randint(0, 9))
        return cvv

    def get_card_number(self) -> str:
        """Return card number

        Args:
          None

        Returns:
          str: Card number at 16 digits.
        """
        return self.__card_number

    def get_expiration_date(self) -> str:
        """Return expiration date

        Args:
          None

        Returns:
          str: Expiration date in format mm/yy.
        """
        return self.__expiration_date

    def get_cvv(self) -> str:
        """Return card's cvv

        Args:
          None

        Returns:
          str: Card's cvv.
        """
        return self.__cvv

    def get_type(self) -> str:
        """Return type of card

        Args:
          None

        Returns:
          str: Type of card (CREDIT OR SERVICE).
        """
        return self.__type

    def __calculate_new_loan(self) -> float:
        """Calculates new loan of a card based on its current info

        Args:
          self: Constructor values

        Returns:
          float: Calculated new loan
        """
        monthly_interest = self.interest_rate / 12
        recalculated_loan = (self.loan - self.payment
                             ) * (1 + monthly_interest)
        new_loan = recalculated_loan + self.new_charges

        self.loan = 0
        self.new_charges = 0
        return new_loan

    def update(self) -> None:
        """Updates loan, payment, new charges and new loan information

        Args:
          self: Card information

        Returns:
          None
        """
        self.loan = self.new_loan
        payment = float(input("Ingresa tu pago mensual: $"))
        if payment > self.loan:
            self.payment = float(self.loan)
        else:
            self.payment = float(payment)
        self.new_charges = float(input("Ingresa los cargos adicionales: $"))
        self.new_loan = self.__calculate_new_loan()
        self.make_report()

    def create_card_dict(self) -> dict:
        """Creates a card based on class constructor

        Args:
          None

        Returns:
          dict: Created card info
        """

        return {
            "name": self.name,
            "card_number": self.__card_number,
            "expiration_date": self.__expiration_date,
            "cvv": self.__cvv,
            "type": self.__type,
            "interest_rate": self.interest_rate,
            "loan": self.loan,
            "payment": self.payment,
            "new_charges": self.new_charges,
            "new_loan": self.new_loan
        }

    def make_report(self) -> None:
        """Prints the information of a card

        Args:
          dict: Card dictionary

        Returns:
          None
        """

        print(
            f'\n- - - REPORTE TARJETA CON TERMINACION {self.__card_number[-4:]} - - -')
        print(f"Nombre del titular: {self.name}")
        print(f"Número de tarjeta: {self.__card_number}")
        print(f"Fecha de vencimiento: {self.__expiration_date}")
        print(f"CVV: {self.__cvv}")
        print(f"Tipo: {self.__type}")
        print(f"Tasa de interés: {self.interest_rate}%")
        print(f"Pago mensual: {self.format_currency(self.payment)}")
        print(
            f"Deuda actual: {self.format_currency(self.new_loan)}")

        print("\n\n")

    def recurrent_payment(self) -> dict:
        """Pays the total loan based on the payment amount and displays for long will it take to pay it.
        Updates loan, payment, new charges and new loan to value of zero. 

        Args:
          self: constructor information

        Returns:
          None
        """
        payment = self.payment
        current_loan = self.new_loan

        counter = 1

        number_of_payments = math.ceil(current_loan / payment)

        while current_loan > 0:
            if current_loan - payment >= 0:
                print(f'Pago {counter} de {number_of_payments}')
                print(f'Deuda actual: {self.format_currency(current_loan)}')
                print(
                    f'Pago: {self.format_currency(current_loan)} - {self.format_currency(payment)}')
                print(
                    f'Deuda actualizada: {self.format_currency(current_loan - payment)}\n')
                counter += 1
            else:
                print(f'Pago {counter} de {number_of_payments}')
                print(f'Deuda actual: {self.format_currency(current_loan)}')
                print(
                    f'Pago: {self.format_currency(current_loan)} - {self.format_currency(payment)}')
                print(
                    f'Deuda actualizada: {self.format_currency(current_loan - current_loan)}\n')
            current_loan -= payment

        self.payment = 0
        self.new_loan = 0

    def partial_payment(self) -> None:
        current_loan = self.new_loan

        print(
            f'\n- - - PAGO PARCIAL DE LA TARJETA CON TERMINACION {self.__card_number[-4:]} - - -')
        print(f'Deuda actual: {self.format_currency(current_loan)}')

        invalid = True

        while invalid:
            payment = float(input("Ingresa el monto a pagar: $"))
            if float(payment) > float(current_loan):
                print("Tu pago no puede ser mayor a tu deuda actual\n")
            else:
                invalid = False

        if self.new_loan - payment < self.payment:
            self.payment = self.new_loan - payment
        self.new_loan -= payment

        print(f'Deuda actualizada: {self.format_currency(self.new_loan)}\n')

    def format_currency(self, money: float) -> str:
        """Formats a float into a string with a currency format

        Args:
          float: Money in floating format

        Returns:
          str: Money in string formatted into a currency
        """
        return "${:,.2f}".format(money)



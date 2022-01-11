from flask import Flask, render_template, redirect, url_for, flash, request

# CLASSES
from cards.credit_card import CreditCard
from cards.service_card import ServiceCard

# CONTROLLER
from controllers.index_controller import index
from controllers.user_controller import index
import controllers.user_controller as user_controller

# DB
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)


# GET index
def index(type: str, card_number: int):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'SELECT * FROM {type}_cards WHERE card_number = {card_number}')
        data = cursor.fetchall()
        data = data[0]
    except:
        flash('An error ocurred. Please try again later', 'danger')
        return redirect(url_for('index_bp.index'))

    # QUERY USER
    user_id = data[1]
    user = user_controller.query_user(user_id)
    user_dict = user_controller.create_user_dict(user[0])

    # CREATE CARD DICTIONARY
    if type == "credit":
        card_dict = create_credit_card_dict(data)

    elif type == "service":
        card_dict = create_service_card_dict(data)

    return render_template(
        'card-info.html',
        card=card_dict,
        user=user_dict,
        title=f"{type.capitalize()} Card Info"
    )


# GET ADD CARD
def add_card_get(user_id: int, type: str):
    try:
        user = user_controller.query_user(user_id)
        return render_template(
            f'add-card.html',
            user=user[0],
            title=f"Add {type.capitalize()} Card",
            type=type
        )
    except:
        flash('An error ocurred. Please try again later.', 'danger')
        return redirect(url_for('index_bp.index'))


# POST ADD CARD
def add_card_post(type: str):
    try:
        if request.method == 'POST':
            # GET FORM DATA
            user_id = request.form['user_id']
            loan = float(request.form['loan'])

            # QUERY USER AND GET FULLNAME
            user = user_controller.query_user(user_id)[0]
            fullname = f'{user[1]} {user[2]}'

            # CURSOR MYSQL
            cursor = mysql.connection.cursor()

            if type == "credit":
                interest_rate = float(request.form['interest_rate'])
                payment = float(request.form['payment'])
                new_charges = float(request.form['new_charges'])

                # CREATE CREDIT CARD INSTANCE BASED ON REQUEST INFO
                new_card = CreditCard(fullname, user_id, interest_rate,
                                      loan, payment, new_charges)

                # INSERT NEW CARD INTO MYSQL TABLE
                cursor.execute("""
                INSERT INTO credit_cards (user_id, card_number, expiration_date, cvv, type, interest_rate, loan, payment, new_charges, new_loan)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, new_card.card_number, new_card.expiration_date, new_card.cvv, new_card.type, new_card.interest_rate, new_card.loan, new_card.payment, new_card.new_charges, new_card.new_loan))

            elif type == "service":
                new_card = ServiceCard(fullname, user_id, loan)

                # INSERT NEW SERVICE CARD INTO MYSQL TABLE
                cursor.execute("""
                INSERT INTO service_cards (user_id, card_number, expiration_date, cvv, type, loan, payment)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, new_card.card_number, new_card.expiration_date, new_card.cvv, new_card.type, new_card.loan, new_card.payment))

            # COMMIT MYSQL CODE
            mysql.connection.commit()

            return redirect(url_for('.index', type=type, card_number=new_card.card_number))
    except:
        flash(
            'There was an error creating the card. Please try again later.', 'danger')
        return redirect(url_for('user_bp.index', id=user_id))


# DELETE CARD
def delete_card(type: str, id: int):
    try:
        cursor = mysql.connection.cursor()
        # GET USER ID
        cursor.execute(f'SELECT user_id from {type}_cards WHERE card_id={id}')
        user_id = cursor.fetchall()[0]

        # DELETE CARD
        cursor.execute(f'DELETE FROM {type}_cards WHERE card_id = {id}')
        mysql.connection.commit()

        # REDIRECT TO USER PAGE
        return redirect(url_for('user_bp.index', id=user_id))
    except:
        flash(
            'There was an error deleting the card. Please try again later.', 'danger')
        return redirect(url_for('index_bp.index'))


# CREATE CARD REPORT
def create_report(type: str, card_number: str):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            f'SELECT * FROM {type}_cards WHERE card_number = {card_number}')
        data = cursor.fetchall()
        data = data[0]

        # QUERY USER
        user_id = data[1]
        user = user_controller.query_user(user_id)[0]
        user_dict = user_controller.create_user_dict(user)

        if type == 'credit':
            card_dict = create_credit_card_dict(data)
            card = CreditCard(user_dict['fullname'], user_id, card_dict['interest_rate'],
                              card_dict['loan'], card_dict['payment'], card_dict['new_charges'])

        elif type == "service":
            card_dict = create_service_card_dict(data)
            card = ServiceCard(
                user_dict["fullname"], user_id, card_dict['loan'])

        card.card_number = card_dict['card_number']['full']
        card.expiration_date = card_dict["expiration_date"]["full"]
        card.cvv = card_dict['cvv']

        card.create_report()

        flash(
            'Card report created successfully!', 'success')
        return redirect(url_for('.index', card_number=card_number, type=type))

    except:
        flash(
            'Error creating card report. Please try again later.', 'danger')
        return redirect(url_for('.index', card_number=card_number, type=type))


# RECALCULATE LOAN
def recalculate_loan(card_number: str):
    try:
        if request.method == 'POST':
            loan = float(request.form['new_loan'])
            interest_rate = float(request.form['interest_rate'])
            payment = float(request.form['payment'])
            new_charges = float(request.form['new_charges'])

            credit_card = CreditCard(
                'Default user', 0, interest_rate, loan, payment, new_charges)

            new_loan = credit_card.new_loan

            cursor = mysql.connection.cursor()

            cursor.execute(f"""
              UPDATE credit_cards
              SET loan={loan},
              payment={payment},
              new_charges={new_charges},
              new_loan={new_loan}
              WHERE card_number={card_number}
            """)
            mysql.connection.commit()

            print(credit_card)
            return redirect(url_for('.index', type='credit', card_number=card_number))
    except:
        flash(
            'Error recalculating loan. Please try again later.', 'danger')
        return redirect(url_for('.index', type='credit', card_number=card_number))


# TOTAL PAYMENT
def make_total_payment(type_card: str, card_number: str):
    try:
        if request.method == 'POST':
            cursor = mysql.connection.cursor()
            if type_card == 'credit':
                cursor.execute(
                    f'SELECT new_loan FROM credit_cards WHERE card_number={card_number}')
                loan = cursor.fetchall()[0][0]
                print(loan)

                if loan == 0:
                    flash('Loan has been already payed!', 'success')

                else:
                    cursor.execute(f"""
                      UPDATE {type_card}_cards
                      SET loan = 0,
                      new_charges = 0,
                      new_loan = 0
                      WHERE card_number = {card_number}
                    """)
                    mysql.connection.commit()

                    flash('Payment made successfully!', 'success')

            elif type_card == 'service':
                cursor.execute(
                    f'SELECT loan FROM service_cards WHERE card_number={card_number}')
                loan = cursor.fetchall()[0][0]

                if loan == 0:
                    flash('Loan has been already payed!', 'success')

                else:
                    cursor.execute(f"""
                      UPDATE {type_card}_cards
                      SET loan = 0
                      WHERE card_number = {card_number}
                    """)
                    mysql.connection.commit()

                    flash('Payment made successfully!', 'success')

    except:
        flash(
            'There was an error with the payment. Please try again later.', 'danger')

    return redirect(url_for('.index', type=type_card, card_number=card_number))


# PARTIAL PAYMENT
def make_partial_payment(card_number: str):
    try:
        if request.method == 'POST':
            cursor = mysql.connection.cursor()
            cursor.execute(
                f'SELECT payment, new_loan FROM credit_cards WHERE card_number={card_number}')
            payment, loan = cursor.fetchall()[0]

            if loan == 0:
                flash('Loan has been already payed!', 'success')

            else:
                if loan - payment < 0:
                    updated_loan = 0
                else:
                    updated_loan = loan - payment

                cursor.execute(f"""
                    UPDATE credit_cards
                    SET new_loan = {updated_loan}
                    WHERE card_number = {card_number}
                  """)
                mysql.connection.commit()

                flash('Payment made successfully!', 'success')

    except:
        flash(
            'There was an error with the payment. Please try again later.', 'danger')

    return redirect(url_for('.index', type='credit', card_number=card_number))


# HELPERS
def create_credit_card_dict(card: list) -> dict:
    return {
        "card_id": card[0],
        "card_number": {
            "n1": card[2][0:4],
            "n2": card[2][4:8],
            "n3": card[2][8:12],
            "n4": card[2][12:16],
            "full": card[2]
        },
        "expiration_date": {
            "year": card[3].strftime('%Y'),
            "month": card[3].strftime('%m'),
            "full": card[3].strftime('%Y %m %d')
        },
        "cvv": card[4],
        "type": card[5],
        "interest_rate": card[6],
        "loan": card[7],
        "payment": card[8],
        "new_charges": card[9],
        "new_loan": card[10]
    }


def create_service_card_dict(card: list) -> dict:
    return {
        "card_id": card[0],
        "card_number": {
            "n1": card[2][0:4],
            "n2": card[2][4:8],
            "n3": card[2][8:12],
            "n4": card[2][12:16],
            "full": card[2]
        },
        "expiration_date": {
            "year": card[3].strftime('%Y'),
            "month": card[3].strftime('%m'),
            "full": card[3].strftime('%Y %m %d')
        },
        "cvv": card[4],
        "type": card[5],
        "loan": card[6],
        "payment": card[7],
    }

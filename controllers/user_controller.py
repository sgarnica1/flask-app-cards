from flask import Flask, render_template, redirect, url_for, flash, request

# CLASSES
from cards.user import User
from cards.credit_card import CreditCard
from cards.service_card import ServiceCard

# CONTROLLERS
from controllers.index_controller import index
from controllers.cards_controller import create_credit_card_dict, create_service_card_dict

# DB
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)


# GET SINGLE USER
def index(id: int):
    # FETCH USER
    user = query_user(id)
    user_dict = create_user_dict(user[0])

    cursor = mysql.connection.cursor()

    # FETCH CREDIT CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM credit_cards
      INNER JOIN users ON users.user_id = credit_cards.user_id
      WHERE users.user_id={id}
    """)
    credit_card = cursor.fetchall()

    credit_card_data = []
    if len(credit_card) > 0:
        for card in credit_card:
            data = create_credit_card_dict(card)
            credit_card_data.append(data)

    # FETCH SERVICE CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM service_cards
      INNER JOIN users ON users.user_id = service_cards.user_id
      WHERE users.user_id={id}
    """)
    service_card = cursor.fetchall()

    service_card_data = []
    if len(service_card) > 0:
        for card in service_card:
            data = create_service_card_dict(card)
            service_card_data.append(data)

    cards = credit_card_data + service_card_data

    # SORT CARDS BY EXPIRATION YEAR
    cards = sorted(cards, key=lambda i: i['expiration_date']['full'])

    return render_template(
        'user.html',
        user=user_dict,
        cards=cards,
        title=user_dict['firstname'],
    )


# GET/POST ADD SINGLE USER
def add_user():
    if request.method == 'GET':
        return render_template('add-user.html', title="Add User")

    elif request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (firstname, lastname) VALUES (%s, %s)', (firstname, lastname))
        mysql.connection.commit()
        return redirect(url_for('index_bp.index'))


# DELETE SINGLE USER
def delete_user(user_id: int):
    user = query_user(user_id)

    cursor = mysql.connection.cursor()

    # FETCH CREDIT CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM credit_cards
      INNER JOIN users ON users.user_id = credit_cards.user_id
      WHERE users.user_id={user_id}
    """)
    credit_card = cursor.fetchall()

    # FETCH SERVICE CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM service_cards
      INNER JOIN users ON users.user_id = service_cards.user_id
      WHERE users.user_id={user_id}
    """)
    service_card = cursor.fetchall()

    if len(credit_card) > 0 or len(service_card) > 0:
        flash('You must delete all cards before deleting user', 'danger')
        return redirect(url_for('.index', id=user_id))
    else:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(f'DELETE FROM users WHERE user_id={user_id}')
            mysql.connection.commit()
            flash('User deleted succesfully', 'success')
            return redirect(url_for('index_bp.index'))
        except:
            flash('There was an error deleting the user')
            return redirect(url_for('.index', id=user_id))


# CREATE USER REPORT
def create_report(user_id: int):
    # FETCH USER
    user = query_user(user_id)
    user_dict = create_user_dict(user[0])

    # NEW USER INSTANCE
    new_user = User(user_dict['fullname'])

    cursor = mysql.connection.cursor()

    # FETCH CREDIT CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM credit_cards
      INNER JOIN users ON users.user_id = credit_cards.user_id
      WHERE users.user_id={user_id}
    """)
    credit_card = cursor.fetchall()

    # FETCH SERVICE CARD DATA
    cursor.execute(f"""
      SELECT *
      FROM service_cards
      INNER JOIN users ON users.user_id = service_cards.user_id
      WHERE users.user_id={user_id}
    """)
    service_card = cursor.fetchall()

    if len(credit_card) > 0:
        for card in credit_card:
            card_dict = create_credit_card_dict(card)
            new_card = CreditCard(user_dict['fullname'], user_id, card_dict['interest_rate'],
                                  card_dict['loan'], card_dict['payment'], card_dict['new_charges'])
            # CHANGE CARD DATA
            new_card.card_number = card_dict['card_number']['full']
            new_card.expiration_date = card_dict["expiration_date"]["full"]
            new_card.cvv = card_dict['cvv']

            # ADD CARD TO USER
            new_user.add_card(new_card)

    if len(service_card) > 0:
        for card in service_card:
            card_dict = create_service_card_dict(card)
            new_card = ServiceCard(
                user_dict['fullname'], user_id, card_dict['loan'])

            # CHANGE CARD DATA
            new_card.card_number = card_dict['card_number']['full']
            new_card.expiration_date = card_dict["expiration_date"]["full"]
            new_card.cvv = card_dict['cvv']

            # ADD CARD TO USER
            new_user.add_card(new_card)

    new_user.generate_card_reports()
    return(redirect(url_for('.index', id=user_id)))


# HELPERS
def query_user(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM users WHERE user_id={id}')
    return cursor.fetchall()


def create_user_dict(user: list) -> dict:
    """ Creates a dictionary based on user information

    Args:
    list: user list (id, firstname, lastname)

    Rerturn:
    dict: user dictionary crated with args

    """
    firstname = user[1]
    fullname = f'{user[1]} {user[2]}'
    return {
        "user_id": user[0],
        "firstname": firstname,
        "fullname": fullname
    }

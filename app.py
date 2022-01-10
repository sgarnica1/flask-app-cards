from cards.service_card import ServiceCard
from cards.credit_card import CreditCard
from cards.user import User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index_get():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    return render_template('index.html', users=data, title="Users")


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):

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


@app.route('/add/user', methods=['GET'])
def get_add_user():
    return render_template('add-user.html', title="Add User")


@app.route('/add/user', methods=['POST'])
def post_add_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (firstname, lastname) VALUES (%s, %s)', (firstname, lastname))
        mysql.connection.commit()
    return redirect(url_for('index_get'))


@app.route('/add/user/<int:user_id>/<string:type>-card', methods=['GET'])
def get_add_card(user_id, type):
    user = query_user(user_id)
    return render_template(
        f'add-card.html',
        user=user[0],
        title=f"Add {type.capitalize()} Card",
        type=type
    )


@app.route('/add/<string:type>-card', methods=['POST'])
def post_add_card(type):
    if request.method == 'POST':
        # GET FORM DATA
        user_id = request.form['user_id']
        loan = float(request.form['loan'])

        # QUERY USER AND GET FULLNAME
        user = query_user(user_id)[0]
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

        return redirect(url_for('get_user', id=user_id))


@app.route('/<string:type>-card/<int:card_number>', methods=['GET'])
def get_card(type, card_number):
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'SELECT * FROM {type}_cards WHERE card_number = {card_number}')
    data = cursor.fetchall()
    data = data[0]

    # QUERY USER
    user_id = data[1]
    user = query_user(user_id)
    user_dict = create_user_dict(user[0])

    # CREATE CARD DICTIONARY
    if type == "credit":
        card_dict = create_credit_card_dict(data)

    elif type == "service":
        card_dict = create_service_card_dict(data)

    return render_template('card-info.html', card=card_dict, user=user_dict, title=f"{type.capitalize()} Card Info")


# DELETE
@ app.route('/delete/<string:type>-card/<int:id>', methods=['DELETE', 'GET'])
def delete_card(type: str, id: int):
    cursor = mysql.connection.cursor()
    # GET USER ID
    cursor.execute(f'SELECT user_id from {type}_cards WHERE card_id={id}')
    user_id = cursor.fetchall()[0]

    # DELETE CARD
    cursor.execute(f'DELETE FROM {type}_cards WHERE card_id = {id}')
    mysql.connection.commit()

    # REDIRECT TO USER PAGE
    return redirect(url_for('get_user', id=user_id))


@app.route('/delete/user/<int:user_id>', methods=['DELETE', 'GET'])
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
        flash('You must delete all cards before deleting user')
        return redirect(url_for('get_user', id=user_id))
    else:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(f'DELETE FROM users WHERE user_id={user_id}')
            mysql.connection.commit()
            flash('User deleted succesfully')
            return redirect(url_for('index_get'))
        except:
            flash('There was an error deleting the user')
            return redirect(url_for('get_user', id=user_id))


# GENERATE REPORTS
@ app.route('/report/user/<int:user_id>')
def user_report(user_id: int):
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
            new_user.add_card(new_card)

    if len(service_card) > 0:
        for card in service_card:
            card_dict = create_service_card_dict(card)
            new_card = ServiceCard(
                user_dict['fullname'], user_id, card_dict['loan'])
            new_user.add_card(new_card)

    new_user.generate_card_reports()
    return(redirect(url_for('get_user', id=user_id)))


@ app.route('/report/<string:type>/<string:card_number>')
def card_report(type: str, card_number: str):
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'SELECT * FROM {type}_cards WHERE card_number = {card_number}')
    data = cursor.fetchall()
    data = data[0]

    # QUERY USER
    user_id = data[1]
    user = query_user(user_id)[0]
    user_dict = create_user_dict(user)

    if type == 'credit':
        card_dict = create_credit_card_dict(data)
        card = CreditCard(user_dict['fullname'], user_id, card_dict['interest_rate'],
                          card_dict['loan'], card_dict['payment'], card_dict['new_charges'])

    elif type == "service":
        card_dict = create_service_card_dict(data)
        card = ServiceCard(user_dict["fullname"], user_id, card_dict['loan'])

    card.card_number = card_dict['card_number']['full']
    card.expiration_date = card_dict["expiration_date"]["full"]
    card.cvv = card_dict['cvv']

    card.create_report()

    return redirect(url_for('get_card', card_number=card_number, type=type))


# 404 ERROR
@ app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title="Not Found")


# MIDDLEWARE
def query_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)

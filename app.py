from cards.service_card import ServiceCard
from cards.credit_card import CreditCard
from flask import Flask, render_template, request, redirect, url_for
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

    # FETCH CREDIT CARD DATA
    cursor = mysql.connection.cursor()
    cursor.execute(f"""
      SELECT users.user_id, credit_cards.card_id, users.firstname, users.lastname, credit_cards.card_number, credit_cards.expiration_date, credit_cards.type
      FROM credit_cards
      INNER JOIN users ON users.user_id = credit_cards.user_id
      WHERE users.user_id={id}
    """)
    credit_card = cursor.fetchall()

    credit_card_data = []
    if len(credit_card) > 0:
        for card in credit_card:
            data = {
                "card_id": card[1],
                "fullname": user_dict["fullname"],
                "card_number": {
                    "n1": card[4][0:4],
                    "n2": card[4][4:8],
                    "n3": card[4][8:12],
                    "n4": card[4][12:16],
                    "full": card[4]
                },
                "expiration_date": {
                    "year": card[5].strftime('%Y')[-2:],
                    "month": card[5].strftime('%m')
                },
                "type": card[6]
            }
            credit_card_data.append(data)

    # FETCH SERVICE CARD DATA
    cursor.execute(f"""
      SELECT users.user_id, service_cards.card_id, users.firstname, users.lastname, service_cards.card_number, service_cards.expiration_date, service_cards.type
      FROM service_cards
      INNER JOIN users ON users.user_id = service_cards.user_id
      WHERE users.user_id={id}
    """)
    service_card = cursor.fetchall()

    service_card_data = []
    if len(service_card) > 0:
        for card in service_card:
            data = {
                "card_id": card[1],
                "fullname": user_dict['fullname'],
                "card_number": {
                    "n1": card[4][0:4],
                    "n2": card[4][4:8],
                    "n3": card[4][8:12],
                    "n4": card[4][12:16],
                    "full": card[4]
                },
                "expiration_date": {
                    "year": card[5].strftime('%Y')[-2:],
                    "month": card[5].strftime('%m'),
                },
                "type": card[6]
            }
            service_card_data.append(data)

    cards = credit_card_data + service_card_data

    # SORT CARDS BY EXPIRATION YEAR
    cards = sorted(cards, key=lambda i: i['expiration_date']['year'])

    return render_template(
        'user.html',
        user=user_dict,
        cards=cards,
        title=user_dict['firstname']
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
    return redirect(url_for('index'))


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
            new_card = CreditCard(fullname, interest_rate,
                                  loan, payment, new_charges)

            # INSERT NEW CARD INTO MYSQL TABLE
            cursor.execute("""
              INSERT INTO credit_cards (user_id, card_number, expiration_date, cvv, type, interest_rate, loan, payment, new_charges, new_loan)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """, (user_id, new_card.get_card_number(), new_card.get_expiration_date(), new_card.get_cvv(), new_card.get_type(), new_card.interest_rate, new_card.loan, new_card.payment, new_card.new_charges, new_card.new_loan))

        elif type == "service":
            new_card = ServiceCard(fullname, loan)

            # INSERT NEW SERVICE CARD INTO MYSQL TABLE
            cursor.execute("""
              INSERT INTO service_cards (user_id, card_number, expiration_date, cvv, type, loan, payment)
              VALUES (%s, %s, %s, %s, %s, %s, %s)
              """, (user_id, new_card.get_card_number(), new_card.get_expiration_date(), new_card.get_cvv(), new_card.get_type(), new_card.loan, new_card.payment))

        # COMMIT MYSQL CODE
        mysql.connection.commit()

        # CREATE CARD JSON
        new_card.export_info()

        return redirect(url_for('index'))


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
        card_dict = {
            "card_id": data[0],
            "card_number": {
                "n1": data[2][0:4],
                "n2": data[2][4:8],
                "n3": data[2][8:12],
                "n4": data[2][12:16],
                "full": data[2]
            },
            "expiration_date": {
                "year": data[3].strftime('%Y'),
                "month": data[3].strftime('%m')
            },
            "cvv": data[4],
            "type": data[5],
            "interest_rate": data[6],
            "loan": data[7],
            "payment": data[8],
            "new_charges": data[9],
            "new_loan": data[10]
        }

    elif type == "service":
        card_dict = {
            "card_id": data[0],
            "card_number": {
                "n1": data[2][0:4],
                "n2": data[2][4:8],
                "n3": data[2][8:12],
                "n4": data[2][12:16],
                "full": data[2]
            },
            "expiration_date": {
                "year": data[3].strftime('%Y'),
                "month": data[3].strftime('%m')
            },
            "cvv": data[4],
            "type": data[5],
            "loan": data[6],
            "payment": data[7],
        }

    return render_template('card-info.html', card=card_dict, user=user_dict, title=f"{type.capitalize()} Card Info")


@ app.route('/delete/<string:type>-card/<int:id>', methods=['DELETE'])
def delete_card(type, id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM {type}_cards WHERE card_id = {id}')
    mysql.connection.commit()
    return redirect(url_for('index'))


# 404 ERROR
@app.errorhandler(404)
def not_found():
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)

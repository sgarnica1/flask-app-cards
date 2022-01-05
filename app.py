from cards.service_card import ServiceCard
from cards.credit_card import CreditCard
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    return render_template('index.html', users=data, title="Users")


@app.route('/user/<user_id>/add-credit-card')
def add_card_get(user_id):
    user = query_user(user_id)
    return render_template(
        'add-credit-card.html',
        user=user[0],
        title="Add Credit Card"
    )


@app.route('/add-credit-card', methods=['POST'])
def add_card_post():
    if request.method == 'POST':
        # GET FORM DATA
        user_id = request.form['user_id']
        interest_rate = float(request.form['interest_rate'])
        loan = float(request.form['loan'])
        payment = float(request.form['payment'])
        new_charges = float(request.form['new_charges'])

        # QUERY USER AND GET FULLNAME
        user = query_user(user_id)[0]
        fullname = f'{user[1]} {user[2]}'

        # CREATE CARD INSTANCE BASED ON REQUEST INFO
        new_card = CreditCard(fullname, interest_rate,
                              loan, payment, new_charges)
        new_card.export_info()

        # INSERT NEW CARD INTO MYSQL TABLE
        cursor = mysql.connection.cursor()
        cursor.execute("""
          INSERT INTO credit_cards (user_id, card_number, expiration_date, cvv, type, interest_rate, loan, payment, new_charges, new_loan)
          VALUES (%s, %s, current_timestamp(), %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, new_card.get_card_number(), new_card.get_cvv(), new_card.get_type(), new_card.interest_rate, new_card.loan, new_card.payment, new_card.new_charges, new_card.new_loan))
        mysql.connection.commit()

        return redirect(url_for('index'))


@app.route('/user/<user_id>/add-service-card')
def add_service_card_get(user_id):
    user = query_user(user_id)
    return render_template(
        'add-service-card.html',
        user=user[0],
        title="Add Service Card"
    )


@app.route('/add-service-card', methods=['POST'])
def add_service_card_post():
    if request.method == 'POST':
        # GET FORM DATA
        user_id = request.form['user_id']
        loan = float(request.form['loan'])

        # QUERY USER AND GET FULLNAME
        user = query_user(user_id)[0]
        fullname = f'{user[1]} {user[2]}'

        # CREATE CARD INSTANCE BASED ON REQUEST INFO
        new_card = ServiceCard(fullname, loan)
        new_card.export_info()

        # INSERT NEW CARD INTO MYSQL TABLE
        cursor = mysql.connection.cursor()
        cursor.execute("""
          INSERT INTO service_cards (user_id, card_number, expiration_date, cvv, type, loan, payment)
          VALUES (%s, %s, current_timestamp(), %s, %s, %s, %s)
        """, (user_id, new_card.get_card_number(), new_card.get_cvv(), new_card.get_type(), new_card.loan, new_card.payment))
        mysql.connection.commit()

        return redirect(url_for('index'))


@app.route('/add-user')
def add_user_get():
    return render_template('add-user.html', title="Add New User")


@app.route('/add-user', methods=['POST'])
def add_user_post():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (firstname, lastname) VALUES (%s, %s)', (firstname, lastname))
        mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/user/<id>')
def user_info(id):

    # FETCH USER
    user = query_user(id)
    firstname = user[0][1]

    # FETCH CREDIT CARD DATA
    cursor = mysql.connection.cursor()
    cursor.execute(f"""
      SELECT users.user_id, credit_cards.card_id, users.firstname, users.lastname, credit_cards.card_number, credit_cards.expiration_date
      FROM credit_cards
      INNER JOIN users ON users.user_id = credit_cards.user_id
      WHERE users.user_id={id}
    """)
    credit_card_data = cursor.fetchall()

    # FETCH sERVICE CARD DATA
    cursor.execute(f"""
      SELECT users.user_id, service_cards.card_id, users.firstname, users.lastname, service_cards.card_number, service_cards.expiration_date
      FROM service_cards
      INNER JOIN users ON users.user_id = service_cards.user_id
      WHERE users.user_id={id}
    """)
    service_card_data = cursor.fetchall()

    return render_template(
        'user.html',
        user=user[0],
        credit=credit_card_data,
        service=service_card_data,
        title=firstname
    )


@ app.route('/credit-card/<card_number>')
def credit_card_info(card_number):
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'SELECT * FROM credit_cards WHERE card_number = {card_number}')
    data = cursor.fetchall()
    return render_template('credit-card-info.html', card=data[0], title="Credit Card Info")


@ app.route('/service-card/<card_number>')
def service_card_info(card_number):
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'SELECT * FROM service_cards WHERE card_number = {card_number}')
    data = cursor.fetchall()
    return render_template('service-card-info.html', card=data[0], title="Service Card Info")


@ app.route('/delete/credit-card/<id>')
def delete_credit_card(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM credit_cards WHERE card_id = {id}')
    mysql.connection.commit()
    return redirect(url_for('index'))


@ app.route('/delete/service-card/<id>')
def delete_service_card(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM service_cards WHERE card_id = {id}')
    mysql.connection.commit()
    return redirect(url_for('index'))


# MIDDLEWARE
def query_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


def query_user(id: int):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM users WHERE user_id={id}')
    return cursor.fetchall()


if __name__ == '__main__':
    app.run(port=5000, debug=True)

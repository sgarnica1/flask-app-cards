# BLUEPRINTS
from routes.index_bp import index_bp
from routes.user_bp import user_bp
from routes.cards_bp import cards_bp

# CLASSES
from cards.service_card import ServiceCard
from cards.credit_card import CreditCard
from cards.user import User

# FLASK
from flask import Flask, render_template, request, redirect, url_for, flash

# DB
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object('config')

# DB CONNECTION
mysql = MySQL(app)


# ROUTES
app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(cards_bp, url_prefix='/card')


# 404 ERROR
@ app.errorhandler(404)
def not_found(err):
    return render_template('404.html', title="Not Found")


if __name__ == '__main__':
    app.run(port=5000, debug=True)

import mysql.connector
from cryptography.fernet import Fernet
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_bcrypt import Bcrypt
import constants
import json
import re

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"
bcryptObj = Bcrypt(app)
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def create_user_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL,
            tema_interes TEXT NOT NULL
        )
    '''.format(constants.TBL_NAME))


def register_user_to_db(form):
    for field in constants.NOT_EMPTY_INPUTS:
        if len(form[field]) == 0:
            return jsonify(isError=True,
                           message="Algun campo invalido",
                           statusCode=400,
                           data={}), 400

    username = form['username']
    password = bcryptObj.generate_password_hash(form['password']).decode('utf-8')
    email = form['email']
    tema_interes = form['tema_interes']
    match= re.fullmatch(regex, email) 


    if match is None:
      return jsonify(message= "Email no valido"), 400

    if form['password'] != form['password2']:
        return jsonify(message="Contras no coiniciden"), 400

    try:
        conn = mysql.connector.connect(
            host=constants.DB_HOST,
            user=constants.DB_USER,
            password=constants.DB_PASSWORD,
            database=constants.DB_NAME,
            autocommit = True
        )
        cursor = conn.cursor()
        create_user_table(cursor)
        cursor.execute('SELECT * FROM {} WHERE username=%s OR email=%s'.format(constants.TBL_NAME), (username, email))
        existingInfo = cursor.fetchone()
        if existingInfo is not None:
            print("Usuario o correo electronico ya registrado.")
            return jsonify(message="Usuario ya existe"), 409
        else:
            cursor.execute('INSERT INTO {} (username, password, email, tema_interes) values (%s,%s,%s,%s)'.format(constants.TBL_NAME), (username, password, email, tema_interes))
        conn.commit()
        conn.close()
        return jsonify(message="Success"), 201
    except Exception as err:
        print(err)
        return jsonify(message="Algo salio mal"), 502


@app.route("/")
def index():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        response = register_user_to_db(request.form)

        if response == '200 OK' OR 201
            print("sign up bien")
            # return redirect(url_for('index'))
        else:
            print("salio mal", response)
            # return render_template('register.html') #Con mensajito de contraseñas no coinciden}

    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

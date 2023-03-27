import sqlite3
from cryptography.fernet import Fernet
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import constants

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"
bcryptObj = Bcrypt(app)


@app.route("/signback/", methods=["POST"])
def register_user_to_db():
    form = request.json
    for field in constants.NOT_EMPTY_INPUTS:
        if len(form[field]) == 0:
            return jsonify(isError= True,
                    message= "Algun campo invalido",
                    statusCode= 400,
                    data= {}), 400
        
    username = form['username']
    password = bcryptObj.generate_password_hash(form['password'])
    email = form['email']
    tema_interes = form['tema_interes']

    if form['password'] != form['password2']:
        return jsonify(message= "Contras no coiniciden"), 400

    try:
        conn = sqlite3.connect(constants.URL_DB) 
        c = conn.cursor()
        c.execute('SELECT * FROM %s WHERE username=:nombre_usuario OR email=:email' % (constants.TBL_NAME), {"nombre_usuario":username, "email":email})
        existingInfo = c.fetchone()
        if existingInfo is not None:
            print("Usuario o correo electronico ya registrado.")
            return jsonify(message= "Usuario ya existe"), 409
            #pass  # or render_template a special error template.
        else:
            c.execute('INSERT INTO %s (username,password,email,tema_interes) values (?,?,?,?)' % (constants.TBL_NAME),(username,password,email,tema_interes))
        conn.commit()
        conn.close()
        return jsonify(message= "Success"), 201
    except Exception as err:
        print(err)
        return jsonify(message= "Algo salio mal"), 502



@app.route("/")
def index():
    return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        response = register_user_to_db(request.form)

        if response == 200:
            print("sign up bien")
            # return redirect(url_for('index'))
        else:
            print("salio mal", response)
            # return render_template('register.html') #Con mensajito de contraseñas no coinciden}

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
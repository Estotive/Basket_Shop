from datetime import timedelta

from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb

from form import about, home, auth, admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

mysql = MySQL(app)


def create_connection(host, user, password, db):
    connection = False
    try:
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = db
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        print("Connection to MySQL DB successful")
        connection = True
        return connection

    except MySQLdb.OperationalError as e:
        print(f'MySQL server has gone away: {e}, trying to reconnect')
        raise e


connect_db = create_connection('localhost', 'root', 'rasengan8631', 'basket_shop')
# connect_db = create_connection('MartinyukI120.mysql.pythonanywhere-services.com', 'MartinyukI120', 'rasengan8631', 'MartinyukI120$Basket_Shop')

app.add_url_rule('/', view_func=home.index)

app.add_url_rule('/about', view_func=about.about)

# Auth forms
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=auth.login)
app.add_url_rule('/logout', view_func=auth.logout)
app.add_url_rule('/register', methods=['GET', 'POST'], view_func=auth.register)

# Admin panel
app.add_url_rule('/admin', methods=['GET', 'POST'], view_func=admin.admin)
app.add_url_rule('/delete', methods=['GET', 'POST'], view_func=admin.delete)


@app.route('/payment/<idtovar>', methods=['GET', 'POST'])
def payment(idtovar):
    if not session.get("username"):
        return redirect("/login")
    msg = ''
    msgr = ''
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM tovar WHERE idtovar={idtovar}")
    tovar = cursor.fetchall()
    if request.method == 'POST':
        pokupatel = request.form['pokupatel']
        phone = request.form['phone']
        address = request.form['address']
        idtovar = request.form['idtovar']
        try:
            cursor.execute(f'''INSERT INTO `zakaz` (`pokupatel`, `phone`, `address`, `tovar_idtovar`)
                    VALUES ('{pokupatel}', '{phone}', '{address}', '{idtovar}') ''')
            mysql.connection.commit()
            msgr = "Заказ оформлен"
        except(Exception,):
            msg = "Данные неверны"
        cursor.close()
    return render_template('payment.html', msg=msg, tovar=tovar, msgr=msgr)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    cursor = mysql.connection.cursor()
    cursor.execute(f'''SELECT * FROM reviews''')
    rev = cursor.fetchall()
    if request.method == 'POST':
        if session:
            user = session['username']
            cursor.execute(f'''SELECT * FROM account WHERE login = '{user}' ''')
            name = cursor.fetchone()
            description = request.form['desc']
            cursor.execute(
                f'''INSERT INTO `reviews` (`desc`, `username`) VALUES ('{description}', '{name['login']}') ''')
            mysql.connection.commit()
            return redirect("/reviews")
        else:
            return redirect("/register")
    return render_template("reviews.html", rev=rev)


@app.route('/help')
def help():
    return render_template("help.html")


@app.route('/katalog', methods=['GET', 'POST'])
def katalog():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from tovar")
    katalog = cursor.fetchall()
    return render_template("katalog.html", katalog=katalog)


# @app.route('/korzina', methods=['GET', 'POST'])
# def korzina():
# cursor = mysql.connection.cursor()
# return render_template("korzina.html")


if __name__ == "__main__":
    app.run(debug=True)

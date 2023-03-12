from flask import Flask, render_template, session, redirect, request

from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def admin():
    if session['username'] != 'admin':
        return redirect('/')
    cursor = mysql.connection.cursor()
    msg = ''
    msgr = ''
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        opisanie = request.form['opisanie']
        image = request.form['image']
        type = request.form['type']
        print(name, price, opisanie, image, type)
        try:
            cursor.execute(f'''INSERT INTO `tovar` (`name`, `price`, `opisanie`, `image`, `type_idtype`) 
                                VALUES ('{name}', '{price}', '{opisanie}', '{image}', '{type}')''')
            mysql.connection.commit()
            msgr = 'Товар добавлен'
        except(Exception,):
            msg = 'Данные неверны'
    cursor.execute(f"SELECT * FROM zakaz")
    guest = cursor.fetchall()
    return render_template('admin.html', msg=msg, msgr=msgr, guest=guest)

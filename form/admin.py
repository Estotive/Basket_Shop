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

def delete():
    if session['username'] != 'admin':
        return redirect('/')
    cursor = mysql.connection.cursor()
    msg = ''
    msgr = ''
    try:
        if request.method == 'POST':
            name = request.form["name"]
            cursor.execute(f'''SELECT * from tovar WHERE name='{name}' ''')
            tov = cursor.fetchone()
            if tov is None:
                msg = "Товар не найден"
            else:
                cursor.execute(f'''DELETE from tovar WHERE name='{name}' ''')
                mysql.connection.commit()
                msgr = "Товар удален"
    except(Exception, ):
        msg = "Данные неверны"
    return render_template('delete.html', msg=msg, msgr=msgr)

import sys
import random
from flask import Flask
from flask import redirect, url_for
from flask import request
from flask import render_template
from flask import session
from UserDao import UserDao
from AdminDao import AdminDao
from Item import Item
from ItemDao import ItemDao
from User import User
from Request import Request
from RequestDao import RequestDao

app = Flask(__name__)

import socket    
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)    

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        admin = AdminDao()
        dao = UserDao()
        if dao.check(request.form['email'], request.form['password']):
            if admin.check(request.form['email'], request.form['password']):
                session["admin"] = "yes"
            else:
                session["admin"] = "no"

            session['email'] = request.form['email']
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        dao = UserDao()
        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        new_user = User(email, password, fname, lname)
        dao.add(new_user)
        return redirect(url_for('login'))
    return render_template('create_user.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html', **locals())

@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    return render_template('inventory.html', **locals())

@app.route('/items', methods = ['POST', 'GET'])
def items():
    dao = ItemDao()
    items = dao.get_all()

    return render_template('items.html', **locals())

@app.route('/info_desk', methods = ['POST', 'GET'])
def info_desk():
    dao = ItemDao()
    items = dao.get_infodesk()
    session['storage'] = "infodesk"

    return render_template('info_desk.html', **locals())

@app.route('/gac', methods = ['POST', 'GET'])
def gac():
    dao = ItemDao()
    items = dao.get_gac()
    session['storage'] = "gac"
    return render_template('gac.html', **locals())

@app.route('/delete_item', methods = ['POST', 'GET'])
def delete_item():
    dao = ItemDao()
    number = request.form['item_number']
    dao.delete(number)

    if session['storage'] == "infodesk":
        return redirect(url_for('inventory'))

    if session['storage'] == "gac":
        return redirect(url_for('gac'))


@app.route('/add_item', methods = ['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        quantity = request.form['quantity']
        unit = request.form['unit']
        item_number = random.randrange(1000, 9999)
        storage_area = request.form['storage_area']

        dao = ItemDao()
        item = Item(name, desc, quantity, unit, item_number, storage_area)
        dao.add(item)
        return redirect(url_for('inventory'))

    return render_template('add_item.html')

@app.route('/edit_item_page', methods = ['POST', 'GET'])
def edit_item_page():
    name = request.form['name']
    desc = request.form['desc']
    quantity = request.form['quantity']
    unit = request.form['unit']
    item_number = request.form['item_number']
    storage_area = request.form['storage_area']

    return render_template('edit_item_page.html', **locals())

@app.route('/edit_item', methods = ['POST', 'GET'])
def edit_item():
    name = request.form['name']
    desc = request.form['desc']
    quantity = request.form['quantity']
    unit = request.form['unit']
    item_number = request.form['item_number']
    storage_area = request.form['storage_area']

    dao = ItemDao()
    dao.edit(name, desc, quantity, unit, item_number, storage_area)
    if session['storage'] == "infodesk":
        return redirect(url_for('info_desk'))

    if session['storage'] == "gac":
        return redirect(url_for('gac'))

@app.route('/requests')
def requests():
    return render_template('requests.html', **locals())

@app.route('/request_item', methods = ['POST', 'GET'])
def request_item():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        quantity = request.form['quantity']
        unit = request.form['unit']
        email = session['email']
        status = "pending"
        request_number = random.randrange(1000, 9999)

        new_request = Request(name, desc, quantity, unit, email, status, request_number)

        dao = RequestDao()
        dao.add(new_request)
        return redirect(url_for('requests'))

    return render_template('request_item.html')

@app.route('/view_requests', methods = ['POST', 'GET'])
def view_requests():
    dao = RequestDao()
    requests = dao.get_all()

    return render_template('view_requests.html', **locals())

@app.route('/view_user_requests', methods = ['POST', 'GET'])
def view_user_requests():
    dao = RequestDao()
    requests = dao.get_specific(session["email"])

    return render_template('view_requests.html', **locals())

@app.route('/delete_request', methods = ['POST', 'GET'])
def delete_request():
    dao = RequestDao()
    number = request.form['request_number']
    dao.delete(number)

    return redirect(url_for('view_requests'))


if __name__ == '__main__':
    app.secret_key = 'some secret key'
    port = 8000 #the custom port you want
    #app.run(host='0.0.0.0', port=port)
    app.run(host=IPAddr, port=port)
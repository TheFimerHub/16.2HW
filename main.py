import json
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///work_order.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.drop_all()

with app.app_context():
    db.create_all()

    with open("data/user_data.json", 'r', encoding='UTF-8') as users:
        for u in json.load(users):
            user_data = User(**u)
            db.session.add(user_data)
            db.session.commit()

    with open('data/offers_data.json', 'r', encoding='UTF-8') as offers:
        for off in json.load(offers):
            offer_data = Offer(**off)
            db.session.add(offer_data)
            db.session.commit()

    with open('data/orders_data.json', 'r', encoding='UTF-8') as orders:
        for ord in json.load(orders):
            order_data = Order(**ord)
            db.session.add(order_data)
            db.session.commit()


def for_jsonify_user_data(obj):
    return {
        'first_name': obj.first_name,
        'last_name': obj.last_name,
        'age': obj.age,
        'email': obj.email,
        'role': obj.role,
        'phone': obj.phone
    }


def for_jsonify_order_data(obj):
    return {
        'name': obj.name,
        'description': obj.description,
        'start_date': obj.start_date,
        'end_date': obj.end_date,
        'address': obj.address,
        'price': obj.price
    }


def for_jsonify_offer_data(obj):
    return {
        'order_id': obj.order_id,
        'executor_id': obj.executor_id
    }


@app.route('/users', methods=['GET', 'POST']) #1
def users_page():
    if request.method == 'GET':
        result = list()
        for user in db.session.query(User).all():
            result.append(for_jsonify_user_data(user))
        return jsonify(result)

    elif request.method == 'POST':
        date = request.json
        for data in date:
            plus_obj = User(**data)
            db.session.add(plus_obj)
            db.session.commit()
        return 'Post completed', 201


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE']) #1.2
def user_id_page(id):
    usr = User.query.get(id)
    if request.method == 'GET':
        return jsonify(for_jsonify_user_data(usr))

    elif request.method == 'PUT':
        obj = User.query.get(id)
        date = request.json

        obj.first_name = date["first_name"]
        obj.last_name = date["last_name"]
        obj.age = date['age']
        obj.email = date['email']
        obj.role = date['role']
        obj.phone = date['phone']

        db.session.add(obj)
        db.session.commit()
        return 'Put ompleted', 201

    elif request.method == 'DELETE':
        obj = User.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return 'Delete completed', 201

@app.route('/orders', methods=['GET', 'POST']) #2
def orders_page():
    result = list()
    if request.method == 'GET':
        for ord in db.session.query(Order).all():
            result.append(for_jsonify_order_data(ord))
        return jsonify(result)

    elif request.method == 'POST':
        date = request.json
        for data in date:
            plus_obj = User(**data)
            db.session.add(plus_obj)
            db.session.commit()
        return 'Post completed', 201


@app.route('/orders/<int:id>', methods=['GET']) #2.2
def order_id_page(id):
    ord = Order.query.get(id)
    if request.method == 'GET':
        return jsonify(for_jsonify_order_data(ord))

    elif request.method == 'PUT':
        obj = User.query.get(id)
        date = request.json

        obj.id = date['id']
        obj.name = date["name"]
        obj.description = date["description"]
        obj.start_date = date['start_date']
        obj.end_date = date['end_date']
        obj.address = date['address']
        obj.price = date['price']
        obj.customer_id = date['customer_id']
        obj.executor_id = date['executor_id']

        db.session.add(obj)
        db.session.commit()
        return 'Put ompleted', 201

    elif request.method == 'DELETE':
        obj = User.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return 'Delete completed', 201



@app.route('/offers', methods=['GET']) #3
def offers_page():
    result = list()
    if request.method == 'GET':
        for off in db.session.query(Offer).all():
            result.append(for_jsonify_offer_data(off))
        return jsonify(result)

    elif request.method == 'POST':
        date = request.json
        for data in date:
            plus_obj = User(**data)
            db.session.add(plus_obj)
            db.session.commit()
        return 'Post completed', 201

@app.route('/offers/<int:id>', methods=['GET']) #3.2
def offer_id_page(id):
    off = Offer.query.get(id)
    if request.method == 'GET':
        return jsonify(for_jsonify_offer_data(off))

    elif request.method == 'PUT':
        obj = User.query.get(id)
        date = request.json

        obj.order_id = date["order_id"]
        obj.executor_id = date["executor_id"]

        db.session.add(obj)
        db.session.commit()
        return 'Put ompleted', 201

    elif request.method == 'DELETE':
        obj = User.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return 'Delete completed', 201


if __name__ == '__main__':
    app.run(debug=True)

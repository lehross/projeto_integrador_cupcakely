import mysql.connector
from flask import Flask, render_template, request
from pandas import DataFrame, concat

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

global session
session = DataFrame({
    'productId': [],
    'amount': [],
    'price': [],
    'name': []
})

def get_conn():
    try:
        connection = mysql.connector.connect(
            host='host',
            database='database',
            user='user',
            password='***')

        print('Connection Opened!')
        return connection
    except:
        raise Exception
    

def close_conn(conn):
    if conn.is_connected():
        conn.close()
        print('Connection Closed!')


def add_item_to_table(name, price):
    try:
        conn = get_conn()
    except:
        print('Connection Failed!')
        pass

    query = f'''
                INSERT INTO Products (Name, Price) VALUES ("{name}", {price})
            '''

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    close_conn(conn)


def get_all_items():
    try:
        conn = get_conn()
    except:
        print('Connection Failed!')
        pass

    query = '''
                SELECT * FROM Products
            '''

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    close_conn(conn)

    if len(result) % 3 == 1:
        result.extend(['', ''])
    elif len(result) % 3 == 2:
        result.append('')

    return zip(*[iter(result)]*3)


def place_order(name, email, phone, address, number, cpf, payment, delivery, total, items):
    try:
        conn = get_conn()
    except:
        print('Connection Failed!')
        pass

    query = f'''
            INSERT INTO Orders (Name, Email, Phone, Address, Number, Cpf, Payment, Delivery, Total, Items) Values ("{name}", "{email}", "{phone}", "{address}", {number}, "{cpf}", {payment}, {delivery}, {total}, "{items}")
            '''

    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    close_conn(conn)

    print('Pedido Inserido!')


@app.route('/')
def home():
    lst_items = get_all_items()

    return render_template('index.html', items_list=lst_items, data=session)


@app.route('/addCart')
def add_cart():
    lst_items = get_all_items()

    productId = request.args.get('Id')
    print(f'Product Id - {productId}')

    try:
        conn = get_conn()
        query = f'''SELECT Price, Name FROM Products WHERE Id = {productId}'''

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        price = result[0][0]
        name = result[0][1]
        print(f'{name} - {price}')

        close_conn(conn)

        global session
        session = concat([session, DataFrame({'productId': [productId], 'amount': [1], 'price': [price], 'name': [name]})], ignore_index=True)
        print(session)
    
    except:
        print('Erro')
        pass
    
    return render_template('index.html', items_list=lst_items, data=session)


@app.route('/cart')
def cart():
    if len(session) == 0:
        items_in_cart = []
        names = []
        prices = []
        amount = []
    
    else:
        items_in_cart = session.groupby(['name'])['amount', 'price'].apply(lambda x : x.sum()).reset_index()
        print(items_in_cart)
        
        names = items_in_cart['name'].tolist() if len(items_in_cart['name'].tolist()) > 0 else []
        prices = items_in_cart['price'].tolist() if len(items_in_cart['price'].tolist()) > 0 else []
        amount = items_in_cart['amount'].tolist() if len(items_in_cart['amount'].tolist()) > 0 else []

    return render_template('cart.html', data=session, names=names, prices=prices, amount=amount, zip=zip, items=zip(names, prices, amount))


@app.route('/closeOrder')
def close_order():
    items_in_cart = session.groupby(['name'])['amount', 'price'].apply(lambda x : x.sum()).reset_index()
    print(items_in_cart)
    
    names = items_in_cart['name'].tolist() if len(items_in_cart['name'].tolist()) > 0 else []
    prices = items_in_cart['price'].tolist() if len(items_in_cart['price'].tolist()) > 0 else []
    amount = items_in_cart['amount'].tolist() if len(items_in_cart['amount'].tolist()) > 0 else []
    total = sum(prices)

    return render_template('close_order.html', data=session, names=names, prices=prices, amount=amount, zip=zip, items=zip(names, prices, amount), total=total)


@app.route('/closedOrder', methods=["POST"])
def closed_order():
    global session
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        number = request.form.get('number')
        cpf = request.form.get('cpf')
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        payment = request.form.get('payment')
        delivery = request.form.get('delivery')

        items_in_cart = session.groupby(['name'])['amount', 'price'].apply(lambda x : x.sum()).reset_index()
        prices = items_in_cart['price'].tolist() if len(items_in_cart['price'].tolist()) > 0 else []
        total = sum(prices)
        names = items_in_cart['name'].tolist()
        amount = items_in_cart['amount'].tolist()
        items = list(zip(names, amount))

        place_order(name, email, phone, address, number, cpf, payment, delivery, total, items)

        session = DataFrame({
            'productId': [],
            'amount': [],
            'price': [],
            'name': []
        })

        return render_template('order_closed.html')
    
    else:
        lst_items = get_all_items()

        return render_template('index.html', items_list=lst_items, data=session)


# add_item_to_table('Chocolate', 5.00)
# add_item_to_table('Chocolate Branco', 5.50)
# add_item_to_table('Morango', 5.00)
# add_item_to_table('Leite Ninho', 6.00)
# add_item_to_table('Nutella', 7.50)
# add_item_to_table('Misto', 5.50)
# add_item_to_table('Chocolate Meio Amargo', 6.00)
# add_item_to_table('Frutas Vermelhas', 6.50)
# add_item_to_table('Trufado', 6.50)
# add_item_to_table('Brigadeiro', 6.00)
# add_item_to_table('Gotas de Chocolate', 5.50)
# add_item_to_table('Red Velvet', 7.00)
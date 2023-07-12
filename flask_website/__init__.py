from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
from decouple import config
import os
import random
import string

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

conn = psycopg2.connect(
    host="localhost",
    database="shopcart",
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    port='5432'
)
cur = conn.cursor()



class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(email, password):
        # Retrieve user data from the database or other storage
        conn = psycopg2.connect(database='shopcart', user=config('DB_USER'), password=config('DB_PASSWORD'),
                                host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s and passw = %s", (email, password,))
        user = cur.fetchone()
        if user:
            return User(user[0])
        return None

def check_user():
    if current_user.is_authenticated:
        id = current_user.id
        cur.execute("select * from users where id = %s", (id,))
        user = cur.fetchone()
        return user
    return False

def generate_random_id(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.sample(characters, k=length))
@login_manager.user_loader
def load_user(user_id):
    cur.execute("SELECT email, passw FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if user:
        email, password = user
        return User.get(email, password)
    return None

@app.route('/')
def index():
    cur.execute(open("flask_website/sql/functions/show_prod.sql", "r").read())
    products = cur.fetchall()
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()

    context = {
        'products': products,
        'categories': categories,
        'user': check_user(),
        'current_user': current_user,
    }
    return render_template('home.html', **context)

@app.route('/store/')
def store():
    cur.execute(open("flask_website/sql/functions/show_prod.sql", "r").read())
    products = cur.fetchall()
    cur.execute("SELECT count(*) from product")
    row = cur.fetchone()
    product_count = row[0]
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()
    context = {
        'products': products,
        'categories': categories,
        'product_count': product_count,
        'user': check_user(),
        'current_user': current_user,
    }
    return render_template('store/store.html', **context)


@app.route('/category/<string:category_name>/')
def products_by_category(category_name):
    cur.execute("SELECT * FROM product WHERE category_name = %s;", (category_name,))
    products = cur.fetchall()
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()
    cur.execute("SELECT count(*) from product WHERE category_name = %s;", (category_name,))
    row = cur.fetchone()
    product_count = row[0]

    context = {
        'products': products,
        'categories': categories,
        'product_count': product_count,
        'user': check_user(),
        'current_user': current_user,
    }
    return render_template('store/store.html', **context)

def add_quantity(item):
    cur.execute("select * from product where id = %s", (str(item[1]), ))
    product = cur.fetchone()
    cur.execute("update cartitem set quantity=quantity+1, sub_total= sub_total + %s where id = %s", (str(product[3]), str(item[0]), ))
    conn.commit()
    return redirect('product_detail')

@app.route('/product/<string:prod_id>', methods=['GET', 'POST'])
def product_detail(prod_id):
    cur.execute("select * from product where id = %s", (str(prod_id), ))
    product = cur.fetchone()
    cur.execute("select * from variation where prod_id = %s and label = \'color\'", (prod_id, ))
    color_variation = cur.fetchall()
    cur.execute("select * from variation where prod_id = %s and label = \'size\'", (prod_id, ))
    size_variation = cur.fetchall()
    user = check_user()
    if request.method == 'POST':
        if user:
            cur.execute("select * from cart where user_id= %s and is_valid=True", (str(user[0]), ))
            cart = cur.fetchone()
            if cart is None:
                id = generate_random_id(20)
                cur.execute("insert into cart (id, user_id, is_valid) values (%s, %s, True)", (id, str(user[0]), ))
                conn.commit()
                cur.execute("select * from cart where id= %s", (str(id), ))
                cart = cur.fetchone()
                cart_item_id = generate_random_id(30)
                cur.execute("insert into cartitem (id, prod_id, cart_id, sub_total) values (%s, %s, %s, %s)", (str(cart_item_id), (prod_id), str(id), str(product[3]), ))
                conn.commit()
            else:
                cur.execute("select * from cartitem where cart_id = %s", (str(cart[0]), ))
                item = cur.fetchone()
                if item is None:
                    cart_item_id = generate_random_id(30)
                    cur.execute("insert into cartitem (id, prod_id, cart_id, sub_total) values (%s, %s, %s, %s)", (str(cart_item_id), (prod_id), str(cart[0]), str(product[3]), ))
                    conn.commit()
                else:
                    add_quantity(item)

            return redirect('/cart')
        else:
            return redirect('/signin')
        
    else:
        context = {
            'product': product,
            'color_variations': color_variation,
            'size_variations': size_variation,
            'user': user,
            'current_user': current_user,
        }

        return render_template('store/product_detail.html', **context)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get(email, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Wrong email or password!"
    else: 
        return render_template('account/signin.html')

@app.route('/dashboard')
@login_required
def dashboard():
    id = current_user.id
    cur.execute("select * from users where id = %s", (id,))
    user = cur.fetchone()

    cur.execute("select count(*) from orders where user_id = %s", (str(user[0]), ))
    orders_count = cur.fetchone()
    context ={
        'current_user': current_user,
        'user': user,
        'orders_count': orders_count
    }
    return render_template('account/dashboard.html', **context)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

def total_amount():
    user = check_user()
    cur.execute("select * from cart where user_id = %s and is_valid = True", (str(user[0])))
    cart = cur.fetchone()
    cur.execute("select * from cartitem where cart_id = %s", (str(cart[0])) )
    cartitems = cur.fetchall()
    total = 0
    for cartitem in cartitems:
        total += cartitem[5]
    cart[4] = total
    return total

@app.route('/cart')
def add_to_cart():
    user = check_user()
    cur.execute("select * from cartitem where cart_id in (select id from cart where user_id = %s)", (str(user[0]), ))
    cartitems = cur.fetchall()
    product_ids = tuple(item[1] for item in cartitems)
    cur.execute("select * from product where id in %s", (product_ids,))
    products = cur.fetchall()
    context =  {
        'cartitems': cartitems,
        'user': check_user(),
        'current_user': current_user,
        'products': products,
        'total': total_amount(),
    }

    return render_template('store/cart.html', **context)

@app.route('/cart/checkout', methods=['GET', 'POST'])
def checkout():
    user = check_user()
    cur.execute("select * from cartitem where cart_id in (select id from cart where user_id = %s)", (str(user[0]), ))
    cartitems = cur.fetchall()
    if request.method == 'POST':
        # infomation
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        first_address = request.form['address_line_1']
        second_address = request.form['address_line_2']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        id = generate_random_id(20)
        cur.execute("insert into payment (id, user_id, cart_id, amount_paid, first_name, last_name, phone, email, first_address, second_address, country, state, city) values (%s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s)", (id, str(user[0]), str(cartitems[0][2]), str(total_amount()), str(first_name), str(last_name), str(phone), str(email), str(first_address), str(second_address), str(country), str(state), str(city),))
        conn.commit()
        
        return redirect('/order/payment')
    
    else:
        product_ids = tuple(item[1] for item in cartitems)
        cur.execute("select * from product where id in %s", (product_ids,))
        products = cur.fetchall()

        context = {
            'cartitems': cartitems,
            'products': products,
            'user': user,
            'current_user': current_user,
        }
        return render_template('store/checkout.html', **context)

def create_order_product(cartitems, order_id, variation_id):
    if variation_id is None:
        for cartitem in cartitems:
            id = generate_random_id(20)
            prod_price = cartitem[5] / cartitem[4]
            cur.execute('insert into orderproduct (id, order_id, prod_id, quantity, prod_price) values (%s, %s, %s, %s, %s)', (str(id), str(order_id), str(cartitem[1]), cartitem[4], prod_price))
            conn.commit()

@app.route('/order/payment', methods=['GET', 'POST'])
def place_order():
    user = check_user()
    cur.execute("select * from cart where user_id = %s and is_valid = True", (user[0]))
    cart = cur.fetchone()

    cur.execute("select * from cartitem where cart_id = %s", (str(cart[0]), ))
    cartitems = cur.fetchall()
    cur.execute("select * from payment where user_id =%s and cart_id= %s and status=\'delay\'", (user[0], cart[0]))
    payment = cur.fetchone()

    if request.method == 'POST':
        payment[4] = 'success'
        id = generate_random_id(20)
        cur.execute("insert into orders (id, user_id, payment_id, total_price) values (%s, %s, %s, %s)", (str(id), str(user[0]), str(payment[0]), str(payment[5]), ))
        conn.commit()
        cur.execute("select * from orders where id = %s", (str(id), ))
        order = cur.fetchone()
        create_order_product(cartitems=cartitems, order_id=id, variation_id=payment[2])

        cur.execute("update cart set is_valid = False where id = %s", (cart[0]))
        conn.commit()
        cur.execute("select * from orderproduct where order_id = %s", (id))
        orderproducts = cur.fetchall()

        context = {
            'order': order,
            'orderproducts': orderproducts,
            'user': user,
            'current_user': current_user,
        }
        
        return render_template('order/order_complete.html', )
    else:
        product_ids = tuple(item[1] for item in cartitems)
        cur.execute("select * from product where id in %s", (product_ids))
        products = cur.fetchall()

        context = {
            'cartitems': cartitems,
            'products': products,
            'payment': payment,
            'user': user,
            'current_user': current_user,
        }
        return render_template('order/payment.html', **context)
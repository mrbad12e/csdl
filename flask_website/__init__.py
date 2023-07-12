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
            cur.execute("select * from cart where user_id= %s", (str(user[0]), ))
            cart = cur.fetchone()
            if cart is None:
                id = generate_random_id(20)
                cur.execute("insert into cart (id, user_id, is_valid) values (%s, %s, True)", (id, str(user[0]), ))
                conn.commit()
                cur.execute("select * from cart where id= %s", (str(id), ))
                cart = cur.fetchone()
                cart_item_id = generate_random_id(30)
                cur.execute("insert into cartitem (id, prod_id, cart_id) values (%s, %s, %s)", (str(cart_item_id), (prod_id), str(id), ))
                conn.commit()
            else: 
                cart_item_id = generate_random_id(30)
                cur.execute("insert into cartitem (id, prod_id, cart_id) values (%s, %s, %s)", (str(cart_item_id), (prod_id), str(cart[0]), ))
                conn.commit()
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
    }

    return render_template('store/cart.html', **context)
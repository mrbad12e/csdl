from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
from decouple import config
import os
import random
import string, decimal

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
    cur.execute("select * from product where id = %s", (str(item[0]), ))
    product = cur.fetchone()
    cur.execute("update cartitem set quantity=quantity+1 where prod_id = %s and cart_id = %s and variation_id =%s", (str(product[3]), str(item[0]), str(item[1]), str(item[2]), ))
    conn.commit()
    return redirect('product_detail')

@app.route('/product/<string:prod_id>', methods=['GET', 'POST'])
def product_detail(prod_id):
    cur.execute("select * from product where id = %s", (str(prod_id), ))
    product = cur.fetchone()
    cur.execute("select * from variation where prod_id = %s and label = \'color\'", (prod_id, ))
    color_variation = cur.fetchall()
    user = check_user()
    cur.execute("select count(rate) from reviewrating where prod_id = %s", (prod_id, ))
    countReview = cur.fetchone()
    countReview = countReview[0]

    if request.method == 'POST':
        if user:
            variation = request.form.get('color')
            user_id = user[0]
            cur.callproc('add_to_cart', (prod_id, variation, user_id))
            conn.commit()
            return redirect('/cart')
        else:
            return redirect('/signin')
    else:
        context = {
            'product': product,
            'color_variations': color_variation,
            'user': user,
            'current_user': current_user,
            'countReview': countReview,
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
            user=check_user()
            cur.execute("select count(*) from orders where user_id = %s", (str(user[0]), ))
            orders_count = cur.fetchone()
            context = {
                'message': "Sign in succesfully",
                'user': user,
                'current_user': current_user,
                'orders_count': orders_count,
            }
            return render_template('account/dashboard.html', **context)
        else:
            context = {
                'message': "Wrong email or password!",
            }
            return render_template('account/signin.html', **context)
    else: 
        return render_template('account/signin.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        id = generate_random_id(8)
        cur.execute("insert into users (id, email, passw) values (%s, %s, %s)", (id, email, password, ))
        conn.commit()
        notices = cur.connection.notices

        user = User.get(email, password)
        if user:
            login_user(user)
            cur.execute("select count(*) from orders where user_id = %s", (id, ))
            orders_count = cur.fetchone()
            context ={
                'current_user': current_user,
                'user': user,
                'message': notices[-1],
                'orders_count': orders_count,
            }
            return render_template('account/dashboard.html', **context)
        else:
            context ={
                'current_user': current_user,
                'message': notices[-1],
            }
            return render_template('account/register.html', **context)
    else: 
        return render_template('account/register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    id = current_user.id
    cur.execute("select * from users where id = %s", (id,))
    user = cur.fetchone()

    cur.execute("select count(*) from orders where user_id = %s", (str(user[0]), ))
    orders_count = cur.fetchone()
    cur.execute("select images from user_profile where id = %s", (str(user[0]), ))
    image = cur.fetchone()
    context ={
        'current_user': current_user,
        'user': user,
        'image': image,
        'orders_count': orders_count
    }
    return render_template('account/dashboard.html', **context)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/cart')
def add_to_cart():
    user = check_user()
    if not user:
        return redirect('/signin')
    cur.execute("select * from cart where user_id = %s and is_valid = True", (str(user[0]), ))
    cart = cur.fetchone()
    cur.execute("select * from cartitem where cart_id =%s order by created_at DESC", (str(cart[0]), ))
    cartitems = cur.fetchall()
    
    product_ids = tuple(item[0] for item in cartitems)
    if not product_ids:
        return redirect('/store')
    products = []
    for product_id in product_ids:
        cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
        product = cur.fetchall()
        products.extend(product)

    variation_ids = tuple(item[2] for item in cartitems)
    variations=[]
    for variation_id in variation_ids:
        cur.execute("select * from variation where id = %s", (variation_id,))
        variation = cur.fetchall()
        variations.extend(variation)
    

    context =  {
        'cartitems': cartitems,
        'user': check_user(),
        'current_user': current_user,
        'products': products,
        'variations': variations,
        'total': cart[4],
    }
    return render_template('store/cart.html', **context)

@app.route('/minus/<string:cart_id>/<string:variation_id>/', methods=['POST'])
def reduce_quantity(cart_id, variation_id):
    cur.execute('update cartitem set quantity=quantity-1 where cart_id=%s and variation_id=%s', (cart_id, variation_id, ))
    conn.commit()

    return redirect('/cart')

@app.route('/plus/<string:cart_id>/<string:variation_id>/', methods=['POST'])
def add_cart(cart_id, variation_id):
    cur.execute('update cartitem set quantity=quantity+1 where cart_id=%s and variation_id=%s', (cart_id, variation_id, ))
    conn.commit()
    return redirect('/cart')

@app.route('/remove/<string:cart_id>/<string:variation_id>/', methods=['POST', 'GET'])
def remove_item(cart_id, variation_id):
    cur.execute("select * from cartitem where cart_id =%s and variation_id=%s", (str(cart_id), str(variation_id)))
    cartitem = cur.fetchone()
    cur.callproc('delete_from_cartitem', (str(cart_id), str(variation_id), cartitem[3]))
    conn.commit()
    return redirect('/cart')

@app.route('/cart/checkout', methods=['GET', 'POST'])
def checkout():
    user = check_user()
    cur.execute("select * from cart where user_id = %s and is_valid = True", (str(user[0]), ))
    cart = cur.fetchone()
    cur.execute("select * from cartitem where cart_id=%s order by created_at DESC", (str(cart[0]), ))
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

        cur.execute("select * from payment where user_id =%s and status=\'delay\'", (user[0], ))
        payment = cur.fetchone()
        if payment:
            cur.execute("update payment set amount_paid = %s where id = %s", (cart[4], str(payment[0]), ))
            conn.commit()
            return redirect('/order/payment')
        else:
            id = generate_random_id(20)
            cur.execute("insert into payment (id, user_id, cart_id, amount_paid, first_name, last_name, phone, email, first_address, second_address, country, state, city) values (%s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s)", (id, str(user[0]), str(cartitems[0][1]), str(cart[4]), str(first_name), str(last_name), str(phone), str(email), str(first_address), str(second_address), str(country), str(state), str(city),))
            conn.commit()

        return redirect('/order/payment')
    
    else:
        product_ids = tuple(item[0] for item in cartitems)
        products=[]
        for product_id in product_ids:
            cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
            product = cur.fetchall()
            products.extend(product)

        variation_ids = tuple(item[2] for item in cartitems)
        variations=[]
        for variation_id in variation_ids:
            cur.execute("select * from variation where id = %s", (variation_id,))
            variation = cur.fetchall()
            variations.extend(variation)
        context = {
            'cartitems': cartitems,
            'variations':variations,
            'products': products,
            'user': user,
            'current_user': current_user,
        }
        return render_template('store/checkout.html', **context)

def create_order_product(cartitems, order_id):
    for cartitem in cartitems:
        cur.execute("select price from product where id = %s", (str(cartitem[0]) ,))
        prod_price = cur.fetchone()
        cur.execute('insert into orderproduct (order_id, prod_id, variation_id, quantity, prod_price) values (%s, %s, %s, %s, %s)', (str(order_id), str(cartitem[0]), str(cartitem[2]), cartitem[3], prod_price[0]))
        conn.commit()

@app.route('/order/payment', methods=['GET', 'POST'])
def place_order():
    user = check_user()
    cur.execute("select * from cart where user_id = %s and is_valid = True", (user[0], ))
    cart = cur.fetchone()

    cur.execute("select * from cartitem where cart_id = %s order by created_at DESC", (str(cart[0]), ))
    cartitems = cur.fetchall()
    cur.execute("select * from payment where user_id =%s and cart_id= %s and status=\'delay\'", (user[0], cart[0]))
    payment = cur.fetchone()
    
    product_ids = tuple(item[0] for item in cartitems)
    products = []
    for product_id in product_ids:
        cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
        product = cur.fetchall()
        products.extend(product)

    variation_ids = tuple(item[2] for item in cartitems)
    cur.execute("select * from variation where id in %s", (variation_ids,))
    variations = cur.fetchall()

    if request.method == 'POST':
        cur.execute('update payment set status = \'success\' where id =%s', (payment[0], ))
        conn.commit()
        id = generate_random_id(20)
        cur.execute("insert into orders (id, user_id, payment_id, total_price) values (%s, %s, %s, %s)", (str(id), str(user[0]), str(payment[0]), str(payment[4]), ))
        conn.commit()
        cur.execute("select * from orders where id = %s", (str(id), ))
        order = cur.fetchone()
        create_order_product(cartitems=cartitems, order_id=id)

        cur.execute("update cart set is_valid = False where id = %s", (cart[0], ))
        conn.commit()
        cur.execute("select * from orderproduct where order_id = %s", (id, ))
        orderproducts = cur.fetchall()
        print(orderproducts)
        context = {
            'products': products,
            'variations': variations,
            'payment': payment,
            'order': order,
            'orderproducts': orderproducts,
            'user': user,
            'current_user': current_user,
        }
        
        return render_template('order/order_complete.html', **context)
    else:
        context = {
            'cartitems': cartitems,
            'variations': variations,
            'products': products,
            'payment': payment,
            'user': user,
            'current_user': current_user,
        }
        return render_template('order/payment.html', **context)
    
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    user = check_user()
    cur.execute("select count(*) from orders where user_id = %s", (str(user[0]), ))
    orders_count = cur.fetchone()
    if request.method=='POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        first_address = request.form['first_address']
        second_address = request.form['second_address']
        country = request.form['country']
        city = request.form['city']
        cur.execute("insert into user_profile (id, first_name, last_name, first_address, second_address, country, city) values (%s,%s,%s, %s,%s,%s,%s)", (str(user[0]), str(first_name), str(last_name), str(first_address), str(second_address), str(country), str(city),))
        conn.commit()
        
        context ={
            'current_user': current_user,
            'user': user,
            'orders_count': orders_count,
            'message': "Profile edited successfully",
        }
        return render_template('account/dashboard.html', **context)
    else:
        context ={
            'current_user': current_user,
            'user': user,
            'orders_count': orders_count,
        }
        return render_template('account/edit_profile.html', **context)

@app.route('/my_orders')
@login_required
def my_orders():
    user = check_user()
    cur.execute("select * from orders where user_id = %s", (str(user[0]), ))
    orders = cur.fetchall()
    context = {
        'orders': orders,
        'current_user': current_user,
        'user': user,
    }
    return render_template('account/my_orders.html', **context)

@app.route('/submit_review/<string:prod_id>', methods=['POST'])
def submit_rating(prod_id):
    user = check_user()
    if request.method == 'POST':
        rating = request.form['rating']
        subject = request.form['subject']
        review = request.form['review']
        id = generate_random_id(20)
        cur.execute("insert into reviewrating (id, user_id, prod_id, subject, review, rate) values (%s, %s, %s, %s,%s, %s)", (str(id), str(user[0]), prod_id, str(subject), str(review), str(rating), ))
        conn.commit()
    return redirect(f"/product/{prod_id}")

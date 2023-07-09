from flask import Flask, render_template, request
import psycopg2
from decouple import config

app = Flask(__name__, static_folder='static')

conn = psycopg2.connect(
    host="localhost",
    database="shopcart",
    user=config('DB_USER'),
    password=config('DB_PASSWORD')
)
cur = conn.cursor()

@app.route('/')
def index():
    cur.execute(open("flask_website/sql/functions/show_prod.sql", "r").read())
    products = cur.fetchall()
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()
    context = {
        'products': products,
        'categories': categories,
    }
    return render_template('home.html', **context)

@app.route('/store/')
def store():
    cur.execute(open("flask_website/sql/functions/show_prod.sql", "r").read())
    products = cur.fetchall()
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()
    context = {
        'products': products,
        'categories': categories,
    }
    return render_template('store/store.html', **context)


@app.route('/category/<string:category_name>/')
def products_by_category(category_name):
    cur.execute("SELECT * FROM product WHERE category_name = %s;", (category_name,))
    products = cur.fetchall()
    cur.execute(open("flask_website/sql/functions/show_category.sql", "r").read())
    categories = cur.fetchall()

    context = {
        'products': products,
        'categories': categories,
    }
    return render_template('store/store.html', **context)

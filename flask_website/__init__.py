from flask import Flask, render_template
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
    context = {
        'products': products,
    }
    return render_template('home.html', **context)


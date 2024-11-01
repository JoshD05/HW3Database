from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="basket_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

@app.route('/api/update_basket_a')
def update_basket_a():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
        conn.commit()
        result = "Success!"
    except psycopg2.Error as e:
        result = f"Error: {e}"
    finally:
        cur.close()
        conn.close()
    return result

@app.route('/api/unique')
def unique_fruits():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT DISTINCT fruit_a AS fruit, 'basket_a' AS source FROM basket_a
            UNION
            SELECT DISTINCT fruit_b AS fruit, 'basket_b' AS source FROM basket_b
            ORDER BY source, fruit;
        """)
        fruits = cur.fetchall()
        return render_template('unique_fruits.html', fruits=fruits)
    except psycopg2.Error as e:
        return f"Error: {e}"
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)


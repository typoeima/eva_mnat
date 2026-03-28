from flask import Flask, jsonify
import psycopg2, os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "mydb"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASS", "pass")
    )

@app.route('/api/items')
def items():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
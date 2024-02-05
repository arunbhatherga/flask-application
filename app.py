from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')
DB_USER = os.getenv('DB_USER', 'arun')
DB_PASS = os.getenv('DB_PASS', 'password')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;",
                (data['name'], data['description']))
    item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': item_id}), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE items SET name = %s, description = %s WHERE id = %s;",
                (data['name'], data['description'], id))
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if updated_rows == 0:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'success': True}), 200

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s;", (id,))
    deleted_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted_rows == 0:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True)


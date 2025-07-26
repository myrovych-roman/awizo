import sqlite3
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db/data.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS avisations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number TEXT NOT NULL,
            driver_name TEXT NOT NULL,
            company_name TEXT,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            type TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    avisations = conn.execute('SELECT * FROM avisations').fetchall()
    conn.close()
    return render_template('list.html', avisations=avisations)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        car_number = request.form['car_number']
        driver_name = request.form['driver_name']
        company_name = request.form['company_name']
        entry_time = request.form['entry_time']
        exit_time = request.form['exit_time']
        type = request.form['type']
        status = request.form['status']

        if not car_number or not driver_name or not entry_time or not type:
            return "Заповніть всі обов'язкові поля", 400

        conn = get_db_connection()
        conn.execute('INSERT INTO avisations (car_number, driver_name, company_name, entry_time, exit_time, type, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (car_number, driver_name, company_name, entry_time, exit_time, type, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    avisation = conn.execute('SELECT * FROM avisations WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        car_number = request.form['car_number']
        driver_name = request.form['driver_name']
        company_name = request.form['company_name']
        entry_time = request.form['entry_time']
        exit_time = request.form['exit_time']
        type = request.form['type']
        status = request.form['status']

        if not car_number or not driver_name or not entry_time or not type:
            return "Заповніть всі обов'язкові поля", 400

        conn.execute('UPDATE avisations SET car_number = ?, driver_name = ?, company_name = ?, entry_time = ?, exit_time = ?, type = ?, status = ? WHERE id = ?',
                     (car_number, driver_name, company_name, entry_time, exit_time, type, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('form.html', avisation=avisation)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM avisations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data['query']
    field = data['field']

    conn = get_db_connection()
    avisations = conn.execute(f"SELECT * FROM avisations WHERE {field} LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in avisations])

@app.route('/<int:id>/status', methods=['POST'])
def update_status(id):
    data = request.get_json()
    status = data['status']

    conn = get_db_connection()
    conn.execute('UPDATE avisations SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

init_db()

if __name__ == '__main__':
    app.run(debug=True)

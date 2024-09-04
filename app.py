import sqlite3
from flask import Flask, jsonify, g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('gallery_roster.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shift Map</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="container">
            <h1>Shift Map</h1>
            <ul id="staff-list" class="staff-list"></ul>
        </div>

        <script>
            fetch('/get_staff')
                .then(response => response.json())
                .then(data => {
                    const staffList = document.getElementById('staff-list');
                    staffList.innerHTML = data.map(staff => 
                        `<li><strong>${staff.name}</strong> - ${staff.role} - ${staff.availability}</li>`
                    ).join('');
                })
                .catch(error => {
                    console.error('Error fetching staff data:', error);
                });
        </script>
    </body>
    </html>
    '''

@app.route('/get_staff')
def get_staff():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Staff")
    staff_data = cursor.fetchall()

    staff_list = [{'id': row['id'], 'name': row['name'], 'role': row['role'], 'availability': row['availability']} for row in staff_data]

    return jsonify(staff_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

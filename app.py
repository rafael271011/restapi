from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cmp210'

mysql = MySQL(app)

@app.route('/')
def home():
    return "✅ Flask + MySQL REST API για χρήστες είναι έτοιμο!"

@app.route('/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password": row[3],
            "created_at": str(row[4])
        })

    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        user = {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password": row[3],
            "created_at": str(row[4])
        }
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User added successfully!"}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    query = "UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s"
    cursor.execute(query, (username, email, password, user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User updated successfully!"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)


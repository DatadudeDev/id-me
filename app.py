from flask import Flask, request, jsonify
import psycopg2
import os
from collections import OrderedDict
import json
from datetime import datetime
import bcrypt

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='gabe',
        password='gabe123')
    return conn

def init_db():
    conn = get_db_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            Username TEXT UNIQUE,
            firstName TEXT,
            lastName TEXT,
            DOB DATE,
            Location TEXT,
            Career TEXT,
            hobbies TEXT[],
            joinDate TIMESTAMP,
            socials JSONB,
            Description TEXT,
            Password TEXT
        )''')
    # Sample data with username and hashed password
    sample_data = [
        ('John', 'Doe', datetime(1990, 4, 15), 'New York', 'Engineer', ['scuba diving', 'basketball'], datetime.now(), json.dumps({"meta": "@meta_user", "twitter": "@twitter_user"}), 'Software developer at XYZ', 'john_doe', bcrypt.hashpw('johnpassword'.encode('utf-8'), bcrypt.gensalt())),
        ('Jane', 'Doe', datetime(1990, 4, 15), 'Los Angeles', 'Doctor', ['knitting', 'chess'], datetime.now(), json.dumps({"instagram": "@insta_user", "linkedin": "@linkedin_user"}), 'Doctor at ABC hospital', 'jane_doe', bcrypt.hashpw('janepassword'.encode('utf-8'), bcrypt.gensalt())),
        # Add more data as needed
    ]
    cursor.executemany('INSERT INTO users (firstName, lastName, DOB, Location, Career, hobbies, joinDate, socials, Description, Username, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', sample_data)
    cursor.close()
    conn.close()

@app.route('/id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user_row = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_row is None:
        return jsonify({'error': 'User not found'}), 404

    # Convert psycopg2.Row to a standard dictionary
    columns = [col[0] for col in cursor.description]
    user = dict(zip(columns, user_row))

    # List of fields to exclude from the response
    exclude_fields = ['id']

    # Filter out the excluded fields
    filtered_user = {k: v for k, v in user.items() if k not in exclude_fields}

    # Re-ordering the dictionary keys alphabetically
    ordered_user = OrderedDict(sorted(filtered_user.items(), key=lambda x: x[0].lower()))

    return jsonify(ordered_user)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(data['Password'].encode('utf-8'), bcrypt.gensalt())

    # SQL for upsert
    upsert_sql = '''
    INSERT INTO users (firstName, lastName, DOB, Location, Career, hobbies, joinDate, socials, Description, Username, Password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (Username)
    DO UPDATE SET
        firstName = EXCLUDED.firstName,
        lastName = EXCLUDED.lastName,
        DOB = EXCLUDED.DOB,
        Location = EXCLUDED.Location,
        Career = EXCLUDED.Career,
        hobbies = EXCLUDED.hobbies,
        joinDate = EXCLUDED.joinDate,
        socials = EXCLUDED.socials,
        Description = EXCLUDED.Description,
        Password = EXCLUDED.Password;
    '''

    # Execute upsert
    cursor.execute(upsert_sql, (data['firstName'], data['lastName'], data['DOB'], data['Location'], data['Career'], data['hobbies'], data['joinDate'], json.dumps(data['socials']), data['Description'], data['Username'], hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Signup complete"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=4546)
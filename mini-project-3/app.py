from flask import Flask, request, render_template, send_from_directory, url_for, redirect, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import datetime

app = Flask(__name__)

# Get the directory of this file
script_directory = os.path.dirname(__file__)

# session security key
app.secret_key = 'secretkey' 

# path for upload folder and DB and storing to app's config object
app.config['UPLOAD_FOLDER'] = os.path.join(script_directory, 'uploads')
app.config['DATABASE'] = os.path.join(script_directory, 'file_storage.db')

# Initialize the database
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                filename TEXT UNIQUE,
                filepath TEXT,
                timestamp TIMESTAMP,
                user_email TEXT,
                FOREIGN KEY (user_email) REFERENCES users (email)
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT
            );
        ''')
        conn.commit()

# Check if the uploads directory exists
def check_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return redirect(url_for('signin'))

@app.route('/files', methods=['GET', 'POST'])
def upload_and_list_files():
    check_upload_folder() 

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            current_timestamp = datetime.datetime.now()

            with sqlite3.connect(app.config['DATABASE']) as conn:
                # Insert data into the 'files' table
                conn.execute('INSERT INTO files (filename, filepath, timestamp, user_email) VALUES (?, ?, ?, ?)',
                 (filename, filepath, current_timestamp, session['user_email']))
                conn.commit()

            return redirect(url_for('upload_and_list_files'))

    signed_user_email = session.get("user_email")

    if signed_user_email:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.execute('SELECT id, filename FROM files WHERE user_email = ?', (session['user_email'],))
            files = cursor.fetchall()

            return render_template('upload.html', files=files)

    else:
        return render_template('signin.html')

# file download route
@app.route('/download/<filename>')
def download_file(filename):
    # download with option as_attachment=True
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/details/<filename>')
def details_file(filename):
    print(filename)
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.execute('SELECT filename, timestamp, filepath FROM files WHERE filename = ?', (filename,))
        file_details = cursor.fetchone()
        print(file_details)

    if file_details:
        filename, timestamp, filepath = file_details
        # Get the size of the file
        size = os.path.getsize(filepath)
        
        # Create a dictionary with file details
        file_info = {
            "filename": filename,
            "timestamp": timestamp,
            "size": size
        }
        
        return jsonify(file_info)
    else:
        return "File not found"


@app.route('/edit/<filename>', methods=["PUT"])
def edit_file(filename):
    new_filename = request.form.get('new_filename')
    new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

    if new_filename:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.execute('UPDATE files SET filename = ?, filepath = ? WHERE filename = ?', (new_filename, new_filepath, filename))
            conn.commit()

        # update file name in storage
        old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        os.rename(old_filepath, new_filepath)

        return jsonify({"filename": filename})


@app.route('/delete/<filename>', methods=["DELETE"])
def delete_file(filename):
    print("Delete route")
    # Delete the file from storage
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)

        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.execute('DELETE FROM files WHERE filename = ?', (filename,))
            conn.commit()

    # Redirect back to the main file listing page
        return jsonify({"message": "File deleted successfully"})
    else:
        return jsonify({"error": "Please provide file name"})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
            conn.commit()

        flash('Signup successful! Please sign in.')
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

            print(user)

            if user and check_password_hash(user[3], password):
                session['user_email'] = user[2]  
                flash('Signin successful!')
                print(("session", dict(session)))
                return redirect(url_for('upload_and_list_files'))
            else:
                # render singin page with flash message
                flash('Invalid email or password. Please try again.')

    return render_template('signin.html')

@app.route('/signout')
def signout():
    # clear session from client and server
    session.clear()
    flash('You have been signed out.')
    return render_template('signin.html')


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=2224, debug=True)


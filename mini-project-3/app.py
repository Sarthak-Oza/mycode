from flask import Flask, request, render_template, send_from_directory, url_for, redirect, jsonify, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import sqlite3
import os
import datetime
import uuid

app = Flask(__name__, static_url_path='/static')

# Get the directory of this file
script_directory = os.path.dirname(__file__)

# load environment variables from .env
load_dotenv()

# session security key
app.secret_key = os.environ.get('SECRET_KEY')

# path for upload folder and DB and storing to app's config object
app.config['UPLOAD_FOLDER'] = os.path.join(script_directory, 'uploads')
app.config['DATABASE'] = os.path.join(script_directory, 'file_storage.db')

# Initialize the database
def init_db():
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            # create files and users table if not exists
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    filename TEXT UNIQUE,
                    filepath TEXT,
                    filesize REAL,
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

    except:
        print("Error with DB!")

# Check if the uploads directory exists
def check_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    # check if there is user loggedin with session and redirect 
    if session:
        return redirect(url_for("upload_and_list_files"))
    else:
        return redirect(url_for('signin'))

# route to display and upload files
@app.route('/files', methods=['GET', 'POST'])
def upload_and_list_files():
    check_upload_folder() 

    if request.method == 'POST':
        file = request.files['file']

        if file:
            # modifying filename to make it unique and keep extension
            filename = ""
            if "." in file.filename:
                file_ext = file.filename.split(".")
                name = file_ext[0]
                ext = file_ext[1]
                filename = secure_filename(f"{name}-{str(uuid.uuid4())[:4]}.{ext}")
            else:
                filename = f"{file.filename}-{str(uuid.uuid4())[:4]}"

            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_email'])
            filepath = os.path.join(user_folder, filename)

            file.save(filepath)

            # converting from Bytes to KB
            file_size = round(os.path.getsize(filepath)/1024, 2)

            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                with sqlite3.connect(app.config['DATABASE']) as conn:
                # Insert file data into DB
                    conn.execute('INSERT INTO files (filename, filepath, filesize, timestamp, user_email) VALUES (?, ?, ?, ?, ?)',
                    (filename, filepath, file_size, current_timestamp, session['user_email']))
                    conn.commit()
            except:
                print("Error while adding file to DB")

                os.remove(filepath)

            return redirect(url_for('upload_and_list_files'))

        else:
            flash("Please choose a file to upload!")

    # GET request 
    signed_user_email = session.get("user_email")

    if signed_user_email:
        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                cursor = conn.execute('SELECT id, filename FROM files WHERE user_email = ?', (session['user_email'],))
                files = cursor.fetchall()
                return render_template('upload.html', files=files)
        except:
            print("Error while getting files from DB!")


    else:
        flash('Please sign in')
        return render_template('signin.html')

# file download route
@app.route('/download/<filename>')
def download_file(filename):
    # check for user if logged in and handle it(GET request)
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_email'])
    filepath = os.path.join(user_folder, filename)
    # download with option as_attachment=True
    return send_from_directory(user_folder, filename, as_attachment=True)

# route to display files details
@app.route('/details/<filename>')
def details_file(filename):
    print(filename)
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.execute('SELECT filename, filepath, filesize, timestamp FROM files WHERE filename = ?', (filename,))
            file_details = cursor.fetchone()
            print(file_details)

        if file_details:
            # unpacking details from file_details
            filename, filepath, filesize, timestamp = file_details
            file_info = {
                "filename": filename, 
                "timestamp": timestamp,
                "size": filesize,
                "filepath": filepath
            }
        
        return jsonify(file_info)

    except:
        print("Error while getting file details from DB!")
    else:
        return "File not found"

# route to edit file name
@app.route('/edit/<filename>', methods=["PUT"])
def edit_file(filename):
    # data from fetch request
    data = request.get_json()
    new_filename = secure_filename(data.get('new_filename'))

    print("New Filename:", new_filename)

    if new_filename:
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                cursor = conn.execute('UPDATE files SET filename = ?, filepath = ? WHERE filename = ?', (new_filename, new_filepath, filename))
                conn.commit()

                # update file name in storage
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_email'])
                old_filepath = os.path.join(user_folder, filename)
                new_filepath = os.path.join(user_folder, new_filename)
                os.rename(old_filepath, new_filepath)

        except:
            print("Error while editing file!")

        return jsonify({"filename": filename})

    else:
        abort(400, "New file name not provided!")

# route to delete file
@app.route('/delete/<filename>', methods=["DELETE"])
def delete_file(filename):
    print("Delete route")
    # Delete the file from storage
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_email'])
    filepath = os.path.join(user_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                conn.execute('DELETE FROM files WHERE filename = ?', (filename,))
                conn.commit()

            # Redirect back to the main file listing page
                return jsonify({"message": "File deleted successfully"})
        except:
            print("Error while deleting the file!")
    else:
        return jsonify({"error": "Please provide file name"})

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # encrypting password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
                conn.commit()

                # Create a directory for the new user
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], email)
                os.makedirs(user_folder)

                flash('Signup successful! Please sign in.')
                return redirect(url_for('signin'))

        except:
            flash('Error, please try with a different email!')

    return render_template('signup.html')

# sign in route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user[3], password):
                    session['user_email'] = user[2]  
                    flash('Signin successful!')
                    return redirect(url_for('upload_and_list_files'))
                else:
                    # render singin page with flash message
                    flash('Invalid email or password. Please try again.')
        except:
            print("Error while signing in the user!")

    return render_template('signin.html')

# signout route
@app.route('/signout')
def signout():
    
    if not session:
        flash('You are not signed in.')
        return render_template('signin.html')

    # Clear session from client and server
    session.clear()
    flash('You have been signed out.')
    return render_template('signin.html')


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=2224, debug=True)


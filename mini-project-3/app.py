from flask import Flask, request, render_template, send_from_directory, url_for, redirect, jsonify
import sqlite3
import os
import datetime

app = Flask(__name__)

# Get the directory of this file
script_directory = os.path.dirname(__file__)

# path for upload folder and DB and storing to app's config object
app.config['UPLOAD_FOLDER'] = os.path.join(script_directory, 'uploads')
app.config['DATABASE'] = os.path.join(script_directory, 'file_storage.db')

# Initialize the database
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.execute('CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, filename TEXT, filepath TEXT, timestamp TIMESTAMP)')
    conn.commit()
    conn.close()

# Check if the uploads directory exists
def check_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_and_list_files():
    check_upload_folder() 

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            current_timestamp = datetime.datetime.now()

            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute('INSERT INTO files (filename, filepath, timestamp) VALUES (?, ?, ?)', (filename, filepath, current_timestamp))
            conn.commit()
            conn.close()

            return redirect(url_for('upload_and_list_files'))

    # GET request
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute('SELECT id, filename FROM files')
    files = cursor.fetchall()
    conn.close()

    return render_template('upload.html', files=files)

# file download route
@app.route('/download/<filename>')
def download_file(filename):
    # download with option as_attachment=True
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/details/<filename>')
def details_file(filename):
    print(filename)
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute('SELECT filename, timestamp, filepath FROM files WHERE filename = ?', (filename,))
    file_details = cursor.fetchone()
    print(file_details)
    conn.close()

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
        # update filename and filepath in DB
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.execute('UPDATE files SET filename = ?, filepath = ? WHERE filename = ?', (new_filename, new_filepath, filename))
        conn.commit()
        conn.close()

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

        # Delete the file entry from the database
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.execute('DELETE FROM files WHERE filename = ?', (filename,))
        conn.commit()
        conn.close()

    # Redirect back to the main file listing page
        return jsonify({"message": "File deleted successfully"})
    else:
        return jsonify({"error": "Please provide file name"})


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=2224, debug=True)


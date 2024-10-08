import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, session, send_from_directory

app = Flask(__name__, static_folder="public")
app.secret_key = "extremdesecret"

# User
users = {
    'walt': '1',
}

UPLOAD_FOLDER = 'public/uploads/'
CATEGORY_FOLDERS = {'nature', 'selfies', 'work', 'vacation'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificarea extensiilor permise
def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

# Atribuie unui fisier un nume de tipul nume_2.jpg in cazul in care este un duplicat
def get_unique_filename(folder, filename):
    base, extension = os.path.splitext(filename)
    cnt = 1
    unique_filename = filename
    
    while os.path.exists(os.path.join(UPLOAD_FOLDER, folder, unique_filename)):
        unique_filename = f"{base}_{cnt}{extension}"
        cnt += 1

    return unique_filename

def create_thumbnail(folder, filename):
    base, extension = os.path.splitext(filename)
    thumb_path = f"{UPLOAD_FOLDER}{folder}/{base}.thumb{extension}"
    big_image_path = f"{UPLOAD_FOLDER}{folder}/{filename}"
    with Image.open(big_image_path) as img:
        img.thumbnail((200, 200))
        img.save(thumb_path)
    return thumb_path

@app.route("/")
def index():
    uploaded_files = {}
    for category in CATEGORY_FOLDERS:
        uploaded_files[category] = []
        category_folder = os.path.join(UPLOAD_FOLDER, category)
        for filename in os.listdir(category_folder):
            if ".thumb" not in filename:
                uploaded_files[category].append(filename)

    return render_template('gallery.html', files=uploaded_files)

@app.route("/about")
def second():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in users:
            if users[username] == password:
                session["authenticated"] = True
                session["username"] = username
                return redirect("/")
            else:
                if password:
                    session['authenticated'] = False
                    error_msg = "Wrong password"
        else:
            if username:
                error_msg = "Username doesn't exist"
    return render_template("login.html", error_msg=error_msg)

@app.route("/logout")
def logout():
    session["authenticated"] = False
    session["username"] = ''
    return redirect("/login")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    msg = ""
    if session.get("authenticated"):
        if request.method == 'POST':
            # Verificăm dacă fișierul este în request
            if 'image' not in request.files:
                msg = "Error"
            else:
                file = request.files['image']
                name = request.form.get('name')
                category = request.form.get('category')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename) # sanitized name
                    if name:
                        base, extension = os.path.splitext(filename)
                        filename = f"{name}{extension}"
                    filename = get_unique_filename(category, filename)
                    file.save(os.path.join(UPLOAD_FOLDER, category, filename))
                    create_thumbnail(category, filename)
                    return redirect("/")
                # Dacă fisierul nu e de tipul permis
                else:
                    msg = "File extension not allowed"
    else:
        msg = "You are not logged in"

    return render_template('upload.html', categories=CATEGORY_FOLDERS , error_msg=msg)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(404)
def error404(code):
    return "HTTP Error 404 - Page Not Found"

# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

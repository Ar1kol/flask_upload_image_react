import os
import urllib.request
from flask import Flask, flash, request, send_from_directory, json
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img_data.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app) 


UPLOAD_FOLDER = 'static/upload/'
STATIC_FOLDER= './static'

app.config["static_folder"] = STATIC_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
CORS(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    image = db.Column(db.String(50))
    title = db.Column(db.String(50))
    content = db.Column(db.String(100))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_image():
    data = request.form
    if 'image' not in request.files:
        flash('No file part')
        return "error - no file"
    file = request.files['image']
    print(file)
    if file.filename == '':
        return "error - no image"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        new_image = Image(title=data['title'], image = filename, content = data['content'])
        db.session.add(new_image)
        db.session.commit()
        return "image upload"
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return "not allowed type"

@app.route('/display')
def display_image():
    res = []
    for img in Image.query.all():
        res.append({"id":img.id, "image":img.image, "title":img.title, "content":img.content})
    return json.dumps(res)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
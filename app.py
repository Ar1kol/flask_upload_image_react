from flask import Flask, send_from_directory

app = Flask(__name__)
STATIC_FOLDER = './static'
UPLOAD_FOLDER = 'static/uploads/'
  
app.secret_key = "secret key"
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route('/show_image/<path:path>')
def send_report(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
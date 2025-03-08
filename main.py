from flask import Flask, request, render_template, send_from_directory
from Utilis import store_image, verify_image, IMAGE_DIR

app = Flask(__name__)

@app.route('/store_image', methods=['POST'])
def store_image_route():
    return store_image(request.files['image'])

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/verify_image', methods=['POST'])
def verify_image_route():
    return verify_image(request.files['image'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

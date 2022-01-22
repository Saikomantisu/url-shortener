from flask import Flask, jsonify, render_template, request, redirect
from tinydb import TinyDB, Query
import shortuuid

db = TinyDB('db\db.json')
table = db.table('short_urls')
app = Flask(__name__)

URL = Query()

# Home
@app.route("/")
def home():
    short_urls = table.all()
    return render_template("home.html", short_urls=short_urls)

# Create short
@app.route("/create_short_url", methods=["POST"])
def create_short_url():
    long_url = request.form.get('longURL')
    code = shortuuid.ShortUUID().random(length=8)
    table.insert({ 'long_url': long_url, 'code': code })
    return redirect('/')

# Redirect
@app.route('/redirect/<string:code>')
def redirect_short(code: str): 
    url = table.search(URL.code == code)
    return redirect(url[0]['long_url'])

# Remove
@app.route('/remove/<string:code>',)
def remove(code: str):
    table.remove(URL.code == code)
    return redirect('/')

# List
@app.route('/list')
def list():
    return jsonify(table.all())

if __name__ == "__main__":
    app.run()
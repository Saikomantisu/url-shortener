from flask import Flask, render_template, request, redirect
from tinydb import TinyDB, Query
import shortuuid

db = TinyDB('db\db.json')
table = db.table('short_urls')
app = Flask(__name__)

@app.route("/")
def home():
    short_urls = table.all()
    return render_template("home.html", short_urls=short_urls)

@app.route("/create_short_url", methods=["POST"])
def create_short_url():
    long_url = request.form.get('longURL')
    short_url = shortuuid.ShortUUID().random(length=8)
    table.insert({ 'long_url': long_url, 'short_url': short_url })
    return redirect('/')

@app.route('/<string:short_url>')
def short(short_url: str): 
    URL = Query()
    url = table.search(URL.short_url == short_url)
    return redirect(url[0]['long_url'])
    

if __name__ == "__main__":
    app.run()
import random
import string
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Links(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long_url = db.Column("long_url", db.String())
    short_url = db.Column("short_url", db.String(4))

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

@app.before_first_request
def create_tables():
    db.create_all()


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        random_letters = random.choices(letters, k=4)
        random_letters = "".join(random_letters)
        short_link = Links.query.filter_by(short_url=random_letters).first()
        if not short_link:
            return random_letters


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_url = request.form['url']
        matched_url = Links.query.filter_by(long_url=input_url).first()
        if matched_url:
            return redirect(url_for("display_short_url", url=matched_url.short_url))
        else:
            short = shorten_url()
            new_url = Links(input_url, short)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short))
    else:
        return render_template('home.html')

@app.route('/display/<url>')
def display_short_url(url):
    print('😊')
    return render_template('shorturl.html', short_url_display=url)

@app.route('/<url>')
def navigate_to(url):
    long_link = Links.query.filter_by(short_url=url).first()
    if long_link:
        return redirect(long_link.long_url)
    else:
        return f"Url desn`t exist"
    
@app.route('/all')
def all():
    return render_template('all.html', urls=Links.query.all())

if __name__ == "__main__":
    app.run(debug=True)
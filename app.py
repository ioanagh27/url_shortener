from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLITE:///links.db'
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




@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
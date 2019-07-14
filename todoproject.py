from flask import Flask, render_template, url_for, flash, request, redirect
from wtforms import StringField, validators
from flask_sqlalchemy import SQLAlchemy
import feedparser
import json
import urllib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post = db.Column(db.String(50), unique=True, nullable=True)

    def __init__(self, post):
        self.post = post

    def __repr__(self):
        return '%s' %self.post
    
@app.route("/", methods=['GET', 'POST'])
def index():
    myPosts = Posts.query.all()
    return render_template('index.html', myPosts=myPosts)

@app.route("/add_post", methods=['POST'])
def add_post():
    post = Posts(post = request.form['post'])
    check = request.form['post']
    if len(check) <= 1:
        flash('You did not add any new job!')
        return redirect( url_for('index'))
    elif len(check) >= 36:
        flash('Your note is too long!')
        return redirect( url_for('index'))
    else:
        db.session.add(post)
        db.session.commit()
        flash('You have a new job to do!')
        return redirect( url_for('index'))

@app.route("/delete_post/<post_id>", methods=['POST'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('You deleted a job!')
    return redirect( url_for('index'))

@app.route("/delete_all", methods=['POST'])
def delete_all():
    db.drop_all()
    db.create_all()
    flash('You deleted everything!')
    return redirect( url_for('index') )

           
if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)

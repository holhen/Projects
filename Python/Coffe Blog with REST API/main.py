from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class BlogPostForm(FlaskForm):
    title = StringField('Blog post title', validators=[DataRequired()])
    subtitle = StringField('Blog post subtitle', validators=[DataRequired()])
    author = StringField('Your name', validators=[DataRequired()])
    img_url = StringField('Blog Image url', validators=[DataRequired()])
    body = CKEditorField('Blog content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add_new_post', methods=['GET', 'POST'])
def add_new_post():
    if request.method == 'GET':
        form = BlogPostForm()
        return render_template("make-post.html", form=form)
    else:
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        img_url = request.form['img_url']
        body = request.form['body']
        date = datetime.now().strftime("%B %d, %Y")

        new_post = BlogPost(
            title = title,
            subtitle = subtitle,
            author = author,
            img_url = img_url,
            body = body,
            date = date,
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

# TODO: edit_post() to change an existing blog post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    requested_post = db.session.get(BlogPost, post_id)
    if request.method == 'GET':
        form = BlogPostForm(
            title = requested_post.title,
            subtitle = requested_post.subtitle,
            author = requested_post.author,
            img_url = requested_post.img_url,
            body = requested_post.body,
        )
        return render_template("make-post.html", form=form, edit_post=True)
    else:
        requested_post.title = request.form['title']
        requested_post.subtitle = request.form['subtitle']
        requested_post.author = request.form['author']
        requested_post.img_url = request.form['img_url']
        requested_post.body = request.form['body']
        db.session.add(requested_post)
        db.session.commit()
        return redirect('/')

# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    requested_post = db.session.get(BlogPost, post_id)
    db.session.delete(requested_post)
    db.session.commit()
    return redirect('/')

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

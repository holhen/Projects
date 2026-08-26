import requests
from flask import Flask, render_template, request

app = Flask(__name__)

posts_response = requests.get('https://api.npoint.io/736b084f4010353d1089')
posts = posts_response.json()


@app.route('/')
def home():
    return render_template("index.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    return render_template("post.html", post=posts[post_id - 1])

@app.post('/form-entry')
def receive_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print(name, email, phone, message)
    return '<h1>Successfully submitted form.</h1>'

if __name__ == "__main__":
    app.run(debug=True)

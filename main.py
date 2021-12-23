from flask import Flask, render_template
import requests

blog_posts = requests.get('https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/').json()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', blog_posts=blog_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<int:index>')
def get_blog(index):
    blog_post = None
    for post in blog_posts:
        if post["id"] == index:
            blog_post = post
            bg_image = post["image"]
    return render_template('post.html', blog_entry=blog_post)

if __name__ == "__main__":
    app.run(debug=True)
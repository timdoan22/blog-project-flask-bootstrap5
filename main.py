from flask import Flask, render_template, request
import requests
import os
import smtplib

MY_EMAIL = os.environ.get("TEST_EMAIL")
EMAIL_PASSWORD = os.environ.get("TEST_EMAIL_PASSWORD")
TEST_EMAIL = os.environ.get("DUMMY_EMAIL")

blog_posts = requests.get('https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/').json()

def send_email(recipient_name, recipient_email, recipient_phone, message):
    recipient_name = recipient_name.capitalize()
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TEST_EMAIL,
            msg=f"Subject:{recipient_name} Has Sent you a Message!\n\nThe following message was sent by:\n\nName: {recipient_name}\nEmail: {recipient_email}\nPhone: {recipient_phone}\nMessage: {message}"
        )

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
    return render_template('post.html', blog_entry=blog_post)

@app.route('/contact', methods=["POST", "GET"])
def receive_data():
    if request.method == 'POST':
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", result=True)
    return render_template("contact.html", result=False)

if __name__ == "__main__":
    app.run(debug=True)
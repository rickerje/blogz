from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        new_blog = Blog(task_name)
        db.session.add(new_blog)
        db.session.commit()



#only run if we are running Python from main.py
if __name__ == '__main__':
    app.run()
from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'Aq0ZrF8r/3fX R~XHH6jmN]L7X/,J?RU'

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer,  db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def get_blog_entries():
    return Blog.query.all()

def get_blog_post(post_id):
    return Blog.query.filter_by(id=post_id)

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        blog_title = request.form['title']
        body = request.form['body']
        
        if blog_title == '' or body == '':
            flash("Don't leave your title or body blank!", 'error')
            return render_template('newpost.html', blog_title=blog_title, body=body)

        new_blog = Blog(title=blog_title, body=body, owner)
        db.session.add(new_blog)
        db.session.commit()
        #redirect user to page displaying blog post they just created
        blog_id = new_blog.id
        url = "/blog?id=" + str(blog_id)
        return redirect(url)
    
    return render_template('newpost.html', title='Build-A-Blog', blog=get_blog_entries())

@app.route('/blog', methods = ['GET', 'POST'])
def display_blog():

    blog_entry_id = request.args.get('id')
    if blog_entry_id: #this means we're using GET and we just want to display a single blog post
        blog_post = get_blog_post(blog_entry_id)
        return render_template('post.html', title = 'Build-A-Blog', blog=blog_post)
    else: #otherwise, we're displaying all posts
        return render_template('blog.html', title = 'Build-A-Blog', blog=get_blog_entries())


#only run if we are running Python from main.py
if __name__ == '__main__':
    app.run()
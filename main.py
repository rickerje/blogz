from flask import Flask, request, redirect, render_template, flash, session
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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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

def get_user_blogs(owner_id):
    return Blog.query.filter_by(owner_id=owner_id).all()
    
def get_blog_entries():
    return Blog.query.all()

def get_blog_post(post_id):
    return Blog.query.filter_by(id=post_id)

def verify_username(username):
    if username == '' or username.strip() == '':
        flash("Please enter a username.", "error")
        return False
    if len(username) <= 2:
        flash("Username must be 3 or more characters", "error")
        return False
    for char in username:
        if char == " ":
            flash("Username cannot have spaces", "error")
            return False
    return True

@app.before_request
def require_login():
    allowed_routes = ['display_blog','login', 'signup', 'index'] #let users see these pages if not logged in
    print(request.endpoint)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/blog', methods = ['GET'])
def display_blog():

        username=request.args.get('user') #someone clicked on a username
        blog_entry_id = request.args.get('id') #someone clicked on a blog title

        if username: #we're displaying all posts by one user
            user = User.query.filter_by(username=username).first()
            userID = user.id
            blogs = Blog.query.filter_by(owner_id=userID).all()
            this_title = "Posts by " + user.username
            return render_template('display_user_posts.html', title = this_title, blog=blogs, user=user)

        elif blog_entry_id: #this means we're using GET and we just want to display a single blog post
            blog_entry_id = int(blog_entry_id)
            print("blog_entry_id = " + str(blog_entry_id))
            blog_post = Blog.query.filter_by(id=blog_entry_id).first()
            print("blog_post.owner_id = " + str(blog_post.owner_id))
            thisUser=User.query.filter_by(id=blog_post.owner_id).first()
            print("User is " + str(thisUser))
            return render_template('post.html', title = blog_post.title, blog=blog_post.body, user=thisUser.username)

        else: #otherwise, we're displaying all posts by all users when someone clicks Display all Posts
            return render_template('blog.html', title='All Blog Posts', blog=get_blog_entries(), users=User.query.all())


@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not verify_username(username):
            return render_template("login.html")
            
        user = User.query.filter_by(username=username).first() #if no user, equals NONE
        #check for user
        if not user:
            flash("Username does not exist.", "error")
            return redirect('/login')
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash("User/password combination not valid", "error")

    
    return render_template('login.html')


@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify-password']
        
        # todo: validate data, use user signup code
        if not verify_username(username):
            return render_template("signup.html")
        
        if password != verify:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")
        # check that user does not already exist:
        existing_user = User.query.filter_by(username=username).first() #if no user, equals NONE
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
        else:
            flash("That user already exists.", "error")

    return render_template('signup.html')

@app.route('/logout', methods = ['POST'])
def logout():
    del session['username']
    return redirect("/")

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        blog_title = request.form['title']
        body = request.form['body']
        
        if blog_title == '' or body == '':
            flash("Don't leave your title or body blank!", 'error')
            return render_template('newpost.html', blog_title=blog_title, body=body)

        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(title=blog_title, body=body, owner=owner)
        db.session.add(new_blog)
        db.session.commit()
        #redirect user to page displaying blog post they just created
        blog_id = new_blog.id
        url = "/blog?id=" + str(blog_id)
        return redirect(url)
    
    return render_template('newpost.html', title='Build-A-Blog', blog=get_blog_entries())

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html', users=User.query.all())

#only run if we are running Python from main.py
if __name__ == '__main__':
    app.run()
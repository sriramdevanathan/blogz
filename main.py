from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sriram@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(350))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=["POST", "GET"])
def index():
    
    title_error = ""
    body_error = ""
    if request.method == "POST":
        blog_title = request.form["title"]
        blog_text = request.form["body"]
        new_blog = Blog(blog_title, blog_text)
        if blog_title == "":
            title_error = "Title Please"
        if blog_text == "":
            body_error = "Oops you forgot the core message"
        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/?q={}'.format(new_blog.id))
        else:
             return render_template('newpost.html', title_error=title_error, body_error=body_error)    
    if request.args.get('q'):
        blogid= request.args.get('q')
        blog = Blog.query.get(blogid)
        return render_template('post.html', title=blog.title, body=blog.body)
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost')
def idx():
    return render_template('newpost.html')

@app.route('/post')
def post():
    blogid= request.args.get('q')
    blog = Blog.query.get(blogid)
    return render_template('post.html', title=blog.title, body=blog.body)

@app.route('/blog')
def indx():
    return redirect('/')



if __name__ == "__main__":
    app.run()
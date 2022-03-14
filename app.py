"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts, Tags, PostTags

app = Flask(__name__)
app.config['SECRET_KEY'] = "bunnyrabbit"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect("users")

@app.route("/users")
def users():
    users = Users.query.all()
    return render_template("base.html", users=users)

@app.route("/users/new")
def new_user():
    return render_template("create_user.html")

@app.route("/users/new", methods=["POST"])
def new_user_post():
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]

    if image == "":
        image = "https://d2cbg94ubxgsnp.cloudfront.net/Pictures/480x270/9/9/3/512993_shutterstock_715962319converted_920340.png"

    new_user = Users(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user(user_id):
    user = Users.query.get(user_id)
    posts = Posts.query.all()
    return render_template("user.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    user = Users.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_post(user_id):
    user = Users.query.get(user_id)
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]

    user.first_name = first
    user.last_name = last
    user.image_url = image

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    Users.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def user_new_post(user_id):
    user = Users.query.get(user_id)
    tags = Tags.query.all()
    return render_template("users_post_new.html", user=user, tags=tags)

@app.route("/users/<int:userid>/posts/new", methods=["POST"])
def user_new_post_post(userid):
    taglist = Tags.query.all()
    tags = request.form.getlist("tag")
    post = Posts(
        title = request.form["title"],
        content = request.form["content"],
        user_id = userid)

    db.session.add(post)
    db.session.commit()

    posts = Posts.query.all()
    postid = 0
    
    for p in posts:
        if p.id > postid:
            postid = p.id
    
    for tag in taglist:
        if tag.name in tags:
            tagid = Tags.query.get(tag.id)
            posttag = PostTags(post_id=postid, tag_id=tagid.id)

            db.session.add(posttag)
            db.session.commit()

    return redirect(f"/users/{userid}")

@app.route("/posts/<int:post_id>")
def post(post_id):
    post = Posts.query.get(post_id)
    user = Users.query.get(post.user_id)
    posttags = PostTags.query.all()
    tags = []

    for p in posttags:
        if p.post_id == post.id:
            tags.append(Tags.query.get(p.tag_id))

    return render_template("post.html", post=post, user=user, tags=tags)

@app.route("/posts/<int:postid>/edit")
def post_edit(postid):
    post = Posts.query.get(postid)
    tags = Tags.query.all()
    posttags = PostTags.query.filter_by(post_id=postid)

    for pt in posttags:
        pt = Tags.query.get(pt.tag_id)
        pt.id = 0

    return render_template("post_edit.html", post=post, tags=tags)

@app.route("/posts/<int:postid>/edit", methods=["POST"])
def post_edit_post(postid):
    post = Posts.query.get(postid)
    posttags = PostTags.query.all()
    tags = request.form.getlist("tag")
    taglist = Tags.query.all()
    
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    for pt in posttags:
        if pt.post_id == post.id:
            db.session.delete(pt)
            db.session.commit()
    
    for tag in taglist:
        if tag.name in tags:
            tagid = Tags.query.get(tag.id)
            posttag = PostTags(post_id=postid, tag_id=tagid.id)

            db.session.add(posttag)
            db.session.commit()

    return redirect(f"/posts/{postid}")

@app.route("/posts/<int:post_id>/delete")
def post_delete(post_id):
    post = Posts.query.get(post_id)
    Posts.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def tags():
    tags= Tags.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tagid>")
def tag(tagid):
    tag = Tags.query.get(tagid)
    posttags = PostTags.query.all()
    posts = []

    for p in posttags:
        if p.tag_id == tag.id:
            posts.append(Posts.query.get(p.post_id))
    
    return render_template("tag.html", tag=tag, posts=posts)

@app.route("/tags/new")
def tags_new():
    return render_template("tag_new.html")

@app.route("/tags/new", methods=["POST"])
def tags_new_post():
    tag = Tags(name = request.form["name"])

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def tags_edit(tag_id):
    tag = Tags.query.get(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tags_edit_post(tag_id):
    tag = Tags.query.get(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    Tags.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")

from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddBlogForm, RegisterForm, ContactUsForm, LoginForm, EditBlogForm
from extensions import app, db
from models import Blog, User




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search/<string:name>")
def search(name):
    blogs = Blog.query.filter(Blog.name.ilike(f"{name}%"))
    return render_template("search_results.html", blogs=blogs)


@app.route("/addyours", methods=["GET", "POST"])
@login_required
def add_blog():
    form = AddBlogForm()

    if form.validate_on_submit():
        file = form.image.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static/img', filename)))

        new_blog = Blog(name=form.name.data, description=form.description.data, image=filename)
        new_blog.create()

        return redirect("/blog")


    return render_template("addyours.html", form=form)


@app.route("/edit_blog/<int:blog_id>", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):

    if current_user.role != "admin":
        return redirect("/")

    blog = Blog.query.get(blog_id)

    form = EditBlogForm(name=blog.name, description=blog.description)

    if form.validate_on_submit():

        file = form.image.data
        if file:
            filename = file.filename
            file.save((path.join(app.root_path, 'static/img', filename)))
            blog.image = filename

        blog.name = form.name.data
        blog.description = form.description.data

        db.session.commit()

        flash("Your Blog has been successfully edited")
        return redirect("/blog")

    return render_template("addyours.html", form=form)


@app.route("/delete_blog/<int:blog_id>")
@login_required
def delete_blog(blog_id):

    if current_user.role != "admin":
        return redirect("/")

    blog = Blog.query.get(blog_id)

    blog.delete()

    flash("Your Blog has been successfully deleted")
    return redirect("/blog")



@app.route("/blog")
def blog():
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)


@app.route("/contact_us", methods=["GET", "POST"])
def contact():
    form = ContactUsForm()

    if form.validate_on_submit():
        print(f"name: {form.name.data}")
        print(f"email: {form.email.data}")
        print(f"subject: {form.subject.data}")
        print(f"yourmessage: {form.yourmessage.data}")

        flash("Your Message Was Successfully sent")

        return redirect("/")

    print(form.errors)
    return render_template("contact_us.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()


    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You Successfully Logged In")
            return redirect("/")


    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You Successfully Logged Out")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("Username already exists")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()

            flash("SUCCESSFUL REGISTRATION")
            return redirect("/")
    print(form.errors)
    return render_template("register.html", form=form)


@app.route("/tour")
def tour():
    return render_template("tour.html")


@app.route("/viewblog/<int:blog_id>")
def viewblog(blog_id):
    blog = Blog.query.get(blog_id)
    return render_template("viewblog.html", blog=blog)



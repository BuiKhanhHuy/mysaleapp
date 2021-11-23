import hashlib

from app import app, login
from flask import render_template, request, url_for, redirect
from flask_login import login_user, logout_user
from app import untils
from app.admin import *


@app.route('/')
def index():
    category_id = request.args.get("category_id")
    keyword = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    categories = untils.load_categories()
    products = untils.load_products(category_id, keyword, from_price, to_price)
    return render_template("index.html", categories=categories, products=products)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    categories = untils.load_categories()
    product = untils.get_product_by_id(product_id)
    return render_template("product-detail.html", categories=categories, product=product)


@login.user_loader
def load_user(user_id):
    return untils.get_user_by_id(user_id)


@app.route("/admin/login", methods=["post", "get"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("pswd", "")
        user = untils.check_user(username, password)
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route("/user/login", methods=["post", "get"])
def user_login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("pswd", "")
        user = untils.check_user(username, password)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/user-register", methods=["get", "post"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        confirm = hashlib.md5(confirm.strip().encode("utf-8")).hexdigest()
        avatar = ""
        if password == confirm:
            untils.add_user(fullname, username, email, password, avatar)
            return redirect(url_for('user_login'))
    return render_template("register.html")


@app.route("/user-logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


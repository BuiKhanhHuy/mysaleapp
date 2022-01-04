import cloudinary.uploader
from flask import render_template, request, url_for, redirect, flash, session, jsonify
from flask_login import login_user, logout_user, login_required
from app import app, login
from app import untils
from app.admin import *
import math


@app.route('/')
def index():
    category_id = request.args.get("category_id")
    keyword = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    page = int(request.args.get("page", 1))

    products = untils.load_products(
        category_id, keyword, from_price, to_price, page)
    number_of_page = math.ceil(
        untils.count_product() / app.config["PAGE_SIZE"])
    return render_template("index.html", products=products, number_of_page=number_of_page)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = untils.get_product_by_id(product_id)
    return render_template("product-detail.html", product=product)


@login.user_loader
def load_user(user_id):
    return untils.get_user_by_id(user_id)


@app.route("/admin/login", methods=["post", "get"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("pswd", "")
        user = untils.check_user(username, password, user_role=UserRole.ADMIN)
        if user:
            login_user(user=user)
        else:
            flash("Tên đăng nhập hoặc mật khẩu của quản trị viên không chính xác.")
    return redirect("/admin")


@app.route("/user/login", methods=["post", "get"])
def user_login():
    error = ""
    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("pswd", "")
        user = untils.check_user(username, password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'index')
            return redirect(url_for(next))
        else:
            error = "Tên đăng nhập hoặc mật khẩu không chính xác."
    return render_template("login.html", error=error)


@app.route("/user-register", methods=["get", "post"])
def register():
    error = ""
    if request.method == "POST":
        try:
            fullname = request.form.get("fname")
            username = request.form.get("uname")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            file = request.files.get("avatar")
            if file:
                upload_result = cloudinary.uploader.upload(
                    file, folder="Avatars/")
                avatar = upload_result.get("secure_url")
            else:
                avatar = None
            if password.__eq__(confirm):
                error = untils.add_user(
                    fullname, username, email, password, avatar)
                if error is None:
                    return redirect(url_for('user_login'))
            else:
                error = "Mật khẩu xác nhận không khớp!"
        except Exception as err:
            error = err
    return render_template("register.html", error=error)


@app.route("/user-logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user-edit", methods=["get", "post"])
def user_edit_profile():
    error = ""
    user = None
    user_id = int(request.args.get("user_id"))
    if not request.args.get("change_password"):
        user = User.query.get(user_id)

    if request.method == "POST":
        change_password = None
        if request.args.get("change_password"):
            change_password = int(request.args["change_password"])
        if change_password and change_password == 1:
            # doi mat khau
            oldpassword = request.form.get("oldpassword")
            newpassword = request.form.get("newpassword")
            confirm = request.form.get("confirm")
            if not untils.check_password(user_id, oldpassword):
                error = "Mật khẩu cũ không chính xác."
            else:
                if newpassword.strip().__eq__(confirm.strip()):
                    if not untils.change_password(user_id, newpassword):
                        error = "Thay đổi mật khẩu không thành công"
                    logout_user()
                    return redirect(url_for('user_login'))
                else:
                    error = "Mật khẩu xác nhận không khớp."
        else:
            password = request.form.get("password")
            if untils.check_password(user_id, password):
                fullname = request.form.get("fname")
                username = request.form.get("uname")
                email = request.form.get("email")
                avatar = request.form.get("avatar")
                error = untils.change_user(
                    user_id, fullname=fullname, username=username, email=email, avatar=avatar)
            else:
                error = "Mật khẩu xác nhận không đúng."

    return render_template("edit-profile.html", user_id=user_id, user=user, error=error)


@app.route("/api/cart", methods=["post"])
def add_to_cart():
    if "cart" not in session:
        session["cart"] = {}
    cart = session["cart"]
    data = request.json

    id = str(data.get("id"))
    name = data.get("name")
    description = data.get("description")
    image = data.get("image")
    price = data.get("price")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "description": description,
            "image": image,
            "price": price,
            "quantity": 1
        }
    session['cart'] = cart
    total_quantity, total_price = untils.total_quantity_and_price(cart)

    return jsonify({
        "total_quantity": total_quantity,
        "total_price": total_price
    })


@app.route("/cart")
def cart():
    total_quantity, total_price = untils.total_quantity_and_price(
        session.get("cart"))
    return render_template("payment.html", total_quantity=total_quantity, total_price=total_price)


@app.route("/api/pay", methods=["post"])
@login_required
def pay():
    try:
        untils.add_receipt(session.get('cart'))
        del session['cart']
        return jsonify({"code": 200})
    except:
        return jsonify({"code": 400})


@app.route("/api/delete-cart", methods=["delete"])
def delete_cart():
    if 'cart' in session:
        cart = session.get('cart')
        data = request.json
        product_id = str(data.get('id'))
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart
            total_quantity, total_price = untils.total_quantity_and_price(
                session.get("cart"))
            return jsonify({'error': 'Xóa sản phẩm thành công.', 'code': 200,
                            'total_quantity': total_quantity, 'total_price': total_price})
    return jsonify({'error': 'Xóa sản phẩm không thành công.', 'code': 500})


@app.route("/api/update-cart", methods=["put"])
def update_cart():
    if 'cart' in session:
        cart = session.get('cart')
        data = request.json
        product_id = str(data.get('id'))
        if product_id in cart:
            cart[product_id]['quantity'] = data.get('quantity')
            session['cart'] = cart
            total_quantity, total_price = untils.total_quantity_and_price(
                session.get("cart"))
            return jsonify({'error': 'update thành công!', 'code': 200,
                            'total_quantity': total_quantity, 'total_price': total_price})
    return jsonify({'error': 'update không thành công!', 'code': 500})


@app.context_processor
def common_response():
    return {
        "categories": untils.load_categories(),
        'total_cart': untils.total_quantity_and_price(session.get('cart'))
    }


if __name__ == "__main__":
    app.run(debug=True)

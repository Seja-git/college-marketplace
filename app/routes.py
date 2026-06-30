# app/routes.py
import os
import uuid

from werkzeug.utils import secure_filename

from flask import current_app

from flask import render_template, request, redirect, flash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import db
from app.models import User, Item,Wishlist
from app.forms import CATEGORIES

import re


def register_routes(app):

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            username = request.form["username"].strip()
            email = request.form["email"].strip()
            college = request.form["college"]
            password = request.form["password"]

            if len(username) < 3:
                flash("Username must be at least 3 characters long", "danger")
                return render_template("register.html")

            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

            if not re.match(email_pattern, email):
                flash("Please enter a valid email address", "danger")
                return render_template("register.html")

            if len(password) < 6:
                flash("Password must be at least 6 characters long", "danger")
                return render_template("register.html")

            existing_user = User.query.filter_by(
                username=username
            ).first()

            if existing_user:
                flash("Username already exists", "danger")
                return render_template("register.html")

            existing_email = User.query.filter_by(
                email=email
            ).first()

            if existing_email:
                flash("Email already registered", "danger")
                return render_template("register.html")

            hashed_password = generate_password_hash(password)

            user = User(
                username=username,
                email=email,
                college=college,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()

            flash("Registration successful! Please login.", "success")

            return redirect("/login")

        return render_template("register.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"].strip()
            password = request.form["password"]

            user = User.query.filter_by(
                email=email
            ).first()

            if user and check_password_hash(
                user.password,
                password
            ):

                login_user(user)

                flash("Login successful!", "success")

                return redirect("/items")

            flash("Invalid Email or Password", "danger")

        return render_template("login.html")


    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash("You have been logged out.", "success")

        return redirect("/")


    @app.route("/")
    @app.route("/items")
    @login_required
    def items():

      query = Item.query

      search = request.args.get("search")
      category = request.args.get("category")
      min_price = request.args.get("min_price")
      max_price = request.args.get("max_price")

      if search:
        query = query.filter(
        Item.title.ilike(f"%{search}%")
        )

      if category:
        query = query.filter_by(
        category=category
        )

      if min_price:
         query = query.filter(
        Item.price >= int(min_price)
        )

      if max_price:
        query = query.filter(
         Item.price <= int(max_price)
        )

      items = query.all()

      categories = [
      category[0]
      for category in db.session.query(Item.category).distinct().all()
       ]




      wishlist_ids = []

      if current_user.is_authenticated:
        wishlist_ids = [
            wish.item_id
            for wish in Wishlist.query.filter_by(user_id=current_user.id).all()
        ]

      return render_template(
        "items.html",
        items=items,
        wishlist_ids=wishlist_ids,
        categories=categories
       )


    @app.route("/item/<int:item_id>")
    def item_detail(item_id):

        item = Item.query.get_or_404(item_id)
        wishlist_ids = []

        if current_user.is_authenticated:
           wishlist_ids = [
           wish.item_id
        for wish in Wishlist.query.filter_by(user_id=current_user.id).all()
    ]

        return render_template(
            "item_detail.html",
            item=item,
            wishlist_ids=wishlist_ids
            
        )
    


    @app.route("/create", methods=["GET", "POST"])
    @login_required
    def create_item():

        if request.method == "POST":

            title = request.form["title"]
            description = request.form["description"]
            price = request.form["price"]
            category = request.form["category"]
            image = request.files["image"]

            filename = None

            if image and image.filename != "":

               extension = os.path.splitext(image.filename)[1]

               filename = f"{uuid.uuid4().hex}{extension}"

               image.save(
               os.path.join(
               current_app.config["UPLOAD_FOLDER"],
               filename
               )
               )

            item = Item(
                title=title,
                description=description,
                price=price,
                category=category,
                image=filename,
                user_id=current_user.id
            )

            db.session.add(item)
            db.session.commit()

            return redirect("/items")

        return render_template(
            "add_item.html",
            categories=CATEGORIES
        )


    @app.route("/edit/<int:item_id>", methods=["GET", "POST"])
    @login_required
    def edit_item(item_id):

        item = Item.query.get_or_404(item_id)

        if item.user_id != current_user.id:
            flash("You cannot edit this listing", "danger")
            return redirect("/items")

        if request.method == "POST":

            item.title = request.form["title"]
            item.description = request.form["description"]
            item.price = request.form["price"]
            item.category = request.form["category"]

            db.session.commit()

            return redirect(f"/item/{item.id}")

        return render_template(
            "edit_item.html",
            item=item,
            categories=CATEGORIES
        )


    @app.route("/delete/<int:item_id>")
    @login_required
    def delete_item(item_id):

        item = Item.query.get_or_404(item_id)

        if item.user_id != current_user.id:
            flash("You cannot delete this listing", "danger")
            return redirect("/items")

        db.session.delete(item)
        db.session.commit()

        return redirect("/items")


    
    @app.route("/profile")
    @login_required
    def profile():

      my_items = Item.query.filter_by(
        user_id=current_user.id
      ).all()

      wishlist = Wishlist.query.filter_by(
        user_id=current_user.id
      ).all()

      return render_template(
        "profile.html",
        items=my_items,
        wishlist=wishlist
      )
    

    @app.route("/wishlist/<int:item_id>")
    @login_required
    def add_to_wishlist(item_id):
        item = Item.query.get_or_404(item_id)

    # Prevent adding your own item
        if item.user_id == current_user.id:
          flash("You can't add your own listing to your wishlist.", "warning")
          return redirect("/items")

        existing = Wishlist.query.filter_by(
           user_id=current_user.id,
           item_id=item_id
        ).first()

        if existing:
          flash("Already in wishlist.", "warning")
          return redirect("/items")

        wish = Wishlist(
           user_id=current_user.id,
           item_id=item_id
        )

        db.session.add(wish)
        db.session.commit()

        flash("Added to wishlist!", "success")

        return redirect("/items")
    

    @app.route("/wishlist/remove/<int:item_id>")
    @login_required
    def remove_wishlist(item_id):

       wish = Wishlist.query.filter_by(
        user_id=current_user.id,
        item_id=item_id
        ).first()

       if wish:
        db.session.delete(wish)
        db.session.commit()

        flash("Removed from wishlist.", "success")

       return redirect(("/items"))

    
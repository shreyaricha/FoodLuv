import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///info.db")

@app.route("/")
@login_required
def index():
    num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
    name = db.execute("SELECT username FROM record WHERE id=:id",id=session["user_id"])
    return render_template("index.html", name=name[0]["username"],num=num[0]['SUM(foodnum)'])


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == 'GET':
        return render_template("register.html")

    else:

        username = request.form.get("username")
        password = request.form.get("password")
        address = request.form.get("address")
        address2 = request.form.get("address2")
        city = request.form.get("city")

        if not username or not password or not address or not address2 or not city:
            return apology("Enter the form correctly" , 400)

        new_user_id=db.execute("INSERT INTO record(username,password,address1,address2,city) VALUES(:username,:password,:address,:address2,:city);",username=username,password=password,address=address,address2=address2,city=city)
        session["user_id"] = new_user_id
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    if request.method == 'GET':
        return render_template("login.html")
    else:
        row=db.execute("SELECT id,username,password FROM record WHERE username=:username", username=request.form.get("username"))
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Fill the form correctly", 400)
        if len(row)!=1 or request.form.get("password") != row[0]["password"]:
            return apology("Invalid username or password" , 400)
        session["user_id"] = row[0]["id"]
        return redirect("/")

@app.route("/coffee" , methods=["GET","POST"])
@login_required
def coffee():
    if request.method == 'GET':
        num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
        return render_template("coffee.html",num=num[0]['SUM(foodnum)'])

@app.route("/indian" , methods=["GET","POST"])
@login_required
def indian():
    if request.method == 'GET':
        num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
        return render_template("indian.html",num=num[0]['SUM(foodnum)'])

@app.route("/fastfood" , methods=["GET","POST"])
@login_required
def fastfood():
    if request.method == 'GET':
        num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
        return render_template("fastfood.html",num=num[0]['SUM(foodnum)'])

@app.route("/chinese" , methods=["GET","POST"])
@login_required
def chinese():
    if request.method == 'GET':
        num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
        return render_template("chinese.html",num=num[0]['SUM(foodnum)'])

@app.route("/drinks" , methods=["GET","POST"])
@login_required
def drinks():
    if request.method == 'GET':
        num=db.execute("SELECT SUM(foodnum) FROM cart WHERE id=:id",id=session["user_id"])
        return render_template("drinks.html",num=num[0]['SUM(foodnum)'])

@app.route("/cart" , methods=["GET","POST"])
@login_required
def cart():
    if request.method == 'GET':
        carts=db.execute("SELECT foodname,foodnum,total,afterdis FROM cart WHERE id=:id",id=session["user_id"])
        total=db.execute("SELECT SUM(afterdis) FROM cart WHERE id=:id;",id=session["user_id"])
        return render_template("cart.html",carts=carts,total=total[0]['SUM(afterdis)'])


@app.route("/history")
@login_required
def history():
    hists = db.execute("SELECT * FROM history WHERE id =:id",id = session["user_id"])
    return render_template("history.html",hists=hists)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/kbc")
@login_required
def kbc():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Kung Bao Chicken')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Kung Bao Chicken',1,2,1.6,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Kung Bao Chicken';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Kung Bao Chicken';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.6 WHERE id=:id AND foodname='Kung Bao Chicken';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/cm")
@login_required
def cm():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Chow Mein')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Chow Mein',1,1.2,0.96,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Chow Mein';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.2 WHERE id=:id AND foodname='Chow Mein';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.96 WHERE id=:id AND foodname='Chow Mein';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/fr")
@login_required
def fr():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Fried Rice')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Fried Rice',1,1.5,1.2,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Fried Rice';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.5 WHERE id=:id AND foodname='Fried Rice';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.2 WHERE id=:id AND foodname='Fried Rice';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/pasta")
@login_required
def pasta():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Pasta')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Pasta',1,1.4,1.16,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Patsa';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.4 WHERE id=:id AND foodname='Pasta';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.16 WHERE id=:id AND foodname='Pasta';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/eg")
@login_required
def eg():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Egg Roll')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Egg Roll',1,1,0.8,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Egg Roll';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1 WHERE id=:id AND foodname='Egg Roll';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.8 WHERE id=:id AND foodname='Egg Roll';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/momo")
@login_required
def momo():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Momos')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Momos',1,1.4,1.16,:id);",id=session["user_id"])
        return redirect("/chinese")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Momos';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.4 WHERE id=:id AND foodname='Momos';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.16 WHERE id=:id AND foodname='Momos';",id=session["user_id"])
        return redirect("/chinese")

@app.route("/biryani")
@login_required
def biryani():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Biryani')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Biryani',1,2,1.7,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Biryani';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Biryani';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.7 WHERE id=:id AND foodname='Biryani';",id=session["user_id"])
        return redirect("/indian")

@app.route("/bpaneer")
@login_required
def bpaneer():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Butter Paneer')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Butter Paneer',1,1.8,1.53,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Butter Paneer';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.8 WHERE id=:id AND foodname='Butter Paneer';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.53 WHERE id=:id AND foodname='Butter Paneer';",id=session["user_id"])
        return redirect("/indian")

@app.route("/dm")
@login_required
def dm():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Dal Makhni')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Dal Makhni',1,1.2,1.02,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Dal Makhni';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.2 WHERE id=:id AND foodname='Dal Makhni';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.02 WHERE id=:id AND foodname='Dal Makhni';",id=session["user_id"])
        return redirect("/indian")

@app.route("/kpaneer")
@login_required
def kpaneer():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Kadahi Paneer')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Kadahi Paneer',1,1.7,1.445,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Kadahi Paneer';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.7 WHERE id=:id AND foodname='Kadahi Paneer';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.445 WHERE id=:id AND foodname='Kadahi Paneer';",id=session["user_id"])
        return redirect("/indian")
@app.route("/rice")
@login_required
def rice():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Rice')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Rice',1,0.8,0.68,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Rice';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+.8 WHERE id=:id AND foodname='Rice';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+.68 WHERE id=:id AND foodname='Rice';",id=session["user_id"])
        return redirect("/indian")

@app.route("/tr")
@login_required
def tr():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Tandoori Roti')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Tandoori Roti',1,0.2,0.17,:id);",id=session["user_id"])
        return redirect("/indian")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Tandoori Roti';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+0.2 WHERE id=:id AND foodname='Tandoori Roti';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.17 WHERE id=:id AND foodname='Tandoori Roti';",id=session["user_id"])
        return redirect("/indian")

@app.route("/sup")
@login_required
def sup():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='7 UP')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('7 UP',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='7 UP';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='7 UP';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='7 UP';",id=session["user_id"])
        return redirect("/drinks")

@app.route("/dew")
@login_required
def dew():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Mountain Dew')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Mountain Dew',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Mountain Dew';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Mountain Dew';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='Mountain Dew';",id=session["user_id"])
        return redirect("/drinks")

@app.route("/Fanta")
@login_required
def Fanta():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Fanta')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Fanta',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Fanta';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Fanta';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='Fanta';",id=session["user_id"])
        return redirect("/drinks")


@app.route("/Pepsi")
@login_required
def Pepsi():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Pepsi')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Pepsi',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Pepsi';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Pepsi';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='Pepsi';",id=session["user_id"])
        return redirect("/drinks")


@app.route("/Sprite")
@login_required
def Sprite():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Sprite')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Sprite',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Sprite';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Sprite';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='Sprite';",id=session["user_id"])
        return redirect("/drinks")

@app.route("/cocacola")
@login_required
def cocacola():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Coca Cola')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Coca Cola',1,2,2,:id);",id=session["user_id"])
        return redirect("/drinks")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Coca Cola';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Coca Cola';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2 WHERE id=:id AND foodname='Coca Cola';",id=session["user_id"])
        return redirect("/drinks")

@app.route("/latte")
@login_required
def latte():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Latte')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Latte',1,3,2.7,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Latte';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+3 WHERE id=:id AND foodname='Latte';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2.7 WHERE id=:id AND foodname='Latte';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Cappuccino")
@login_required
def Cappuccino():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Cappuccino')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Cappuccino',1,2.9,2.46,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Cappuccino';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2.9 WHERE id=:id AND foodname='Cappuccino';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2.46 WHERE id=:id AND foodname='Cappuccino';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Espresso")
@login_required
def Espresso():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Espresso')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Espresso',1,2,1.8,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Espresso';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2 WHERE id=:id AND foodname='Espresso';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.8 WHERE id=:id AND foodname='Espresso';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Americano")
@login_required
def Americano():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Americano')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Americano',1,2.2,1.87,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Americano';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2.2 WHERE id=:id AND foodname='Americano';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.87 WHERE id=:id AND foodname='Americano';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Mocha")
@login_required
def Mocha():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Mocha')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Mocha',1,2.5,2.125,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Mocha';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2.5 WHERE id=:id AND foodname='Mocha';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2.125 WHERE id=:id AND foodname='Mocha';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Machhiato")
@login_required
def Machhiato():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Machhiato')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Machhiato',1,2.6,2.21,:id);",id=session["user_id"])
        return redirect("/coffee")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Machhiato';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2.6 WHERE id=:id AND foodname='Machhiato';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2.21 WHERE id=:id AND foodname='Machhiato';",id=session["user_id"])
        return redirect("/coffee")

@app.route("/Burger")
@login_required
def Burger():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Burger')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Burger',1,1.5,1.35,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Burger';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.5 WHERE id=:id AND foodname='Burger';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.35 WHERE id=:id AND foodname='Burger';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/chb")
@login_required
def chhb():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Chhola Bhatura')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Chhola Bhatura',1,1.2,1.08,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Chhola Bhatura';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.2 WHERE id=:id AND foodname='Chhola Bhatura';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+1.08 WHERE id=:id AND foodname='Chhola Bhatura';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/Dosa")
@login_required
def Dosa():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Dosa')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Dosa',1,1.1,0.99,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Dosa';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1.1 WHERE id=:id AND foodname='Dosa';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.99 WHERE id=:id AND foodname='Dosa';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/idli")
@login_required
def idli():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Idli Sambhar')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Idli Sambharr',1,1,0.9,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Idli Sambharr';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+1 WHERE id=:id AND foodname='Idli Sambharr';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.9 WHERE id=:id AND foodname='Idli Sambharr';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/Pizza")
@login_required
def Pizza():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Pizza')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Pizza',1,2.6,2.21,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Pizza';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+2.6 WHERE id=:id AND foodname='Pizza';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+2.21 WHERE id=:id AND foodname='Pizza';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/Samosa")
@login_required
def Samosa():
    cart = db.execute("SELECT foodname,foodnum FROM cart WHERE id =:id AND foodname=:foodname;",id=session["user_id"],foodname='Samosa')
    if not cart:
        db.execute("INSERT INTO cart(foodname,foodnum,total,afterdis,id) VALUES('Samosa',1,0.1,0.09,:id);",id=session["user_id"])
        return redirect("/fastfood")

    else:
        db.execute("UPDATE cart SET foodnum = foodnum + 1 WHERE id=:id AND foodname='Samosa';",id=session["user_id"])
        db.execute("UPDATE cart SET total=total+0.1 WHERE id=:id AND foodname='Samosa';",id=session["user_id"])
        db.execute("UPDATE cart SET afterdis=afterdis+0.09 WHERE id=:id AND foodname='Samosa';",id=session["user_id"])
        return redirect("/fastfood")

@app.route("/order")
@login_required
def order():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    money=db.execute("SELECT SUM(afterdis) FROM cart WHERE id=:id;",id=session["user_id"])
    rows=db.execute("SELECT foodname,foodnum FROM cart WHERE id=:id;",id=session["user_id"])
    for row in rows:
        db.execute("INSERT INTO history(foodname,foodnum,dateandtime,id) VALUES(:foodname,:foodnum,:date,:id);",foodname=row['foodname'],foodnum=row['foodnum'],date=now,id=session["user_id"])
    db.execute("DELETE FROM cart WHERE id=:id",id=session["user_id"])
    if money[0]['SUM(afterdis)'] == None:
        return render_template("fail.html")
    else:
        return render_template("success.html",money=usd(money[0]['SUM(afterdis)']))





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
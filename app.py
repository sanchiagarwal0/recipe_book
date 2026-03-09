from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# -----------------------------
# Recipes dictionary
# -----------------------------
recipes = {
    "PANCAKE": ["flour", "sugar", "milk", "egg"],
    "POHA": ["flattened rice", "onion", "peanuts", "spices"],
    "sandwich": ["bread", "cucumber", "tomato", "butter"],

    "Spaghetti": ["spaghetti pasta", "tomato sauce", "garlic", "olive oil"],
    "FriedRice": ["rice", "mixed vegetables", "soy sauce", "garlic"],
    "VegetablePasta": ["pasta", "vegetables", "tomato sauce", "cheese"],

    "Biryani": ["basmati rice", "vegetables", "yogurt", "biryani masala"],
    "PaneerButterMasala": ["paneer", "tomato", "butter", "cream"],
    "DalTadka": ["lentils", "onion", "tomato", "garlic"],

    "ChocolateCake": ["flour", "sugar", "cocoa powder", "eggs"],
    "IceCreamSundae": ["ice cream", "chocolate syrup", "nuts", "cherry"],
    "ChocolateBrownie": ["chocolate", "flour", "sugar", "eggs"]
}

# -----------------------------
# Ingredient prices
# -----------------------------
prices = {
    "flour": 20,
    "sugar": 15,
    "milk": 30,
    "egg": 10,
    "flattened rice": 25,
    "onion": 10,
    "peanuts": 20,
    "spices": 15,
    "bread": 25,
    "cucumber": 10,
    "tomato": 10,
    "butter": 40,
    "spaghetti pasta": 60,
    "tomato sauce": 35,
    "garlic": 10,
    "olive oil": 80,
    "rice": 40,
    "mixed vegetables": 30,
    "soy sauce": 20,
    "pasta": 50,
    "vegetables": 30,
    "cheese": 60,
    "basmati rice": 70,
    "yogurt": 30,
    "biryani masala": 25,
    "paneer": 80,
    "cream": 40,
    "lentils": 50,
    "chocolate": 50,
    "cocoa powder": 35,
    "ice cream": 60,
    "chocolate syrup": 25,
    "nuts": 40,
    "cherry": 10,
    "eggs": 12
}

# -----------------------------
# App Data
# -----------------------------
cart = {}
past_orders = []

# Login credentials
current_username = "admin"
current_password = "1234"

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return redirect("/login")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    global current_username, current_password

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == current_username and password == current_password:
            return redirect("/index")
        else:
            return "Invalid Login"

    return render_template("login.html")

# -----------------------------
# Main Page
# -----------------------------
@app.route("/index")
def index():
    return render_template("index.html")

# -----------------------------
# Add Recipe Ingredients to Cart
# -----------------------------
@app.route("/add_to_cart/<dish>")
def add_to_cart(dish):

    ingredients = recipes.get(dish, [])

    for item in ingredients:

        if item in cart:
            cart[item]["qty"] += 1
        else:
            cart[item] = {
                "price": prices.get(item, 20),
                "qty": 1
            }

    return redirect("/index")

# -----------------------------
# Cart Page
# -----------------------------
@app.route("/cart")
def show_cart():

    total = 0

    for item in cart:
        total += cart[item]["price"] * cart[item]["qty"]

    return render_template("cart.html", cart=cart, total=total)

# -----------------------------
# Increase Quantity
# -----------------------------
@app.route("/increase/<item>")
def increase(item):

    if item in cart:
        cart[item]["qty"] += 1

    return redirect("/cart")

# -----------------------------
# Decrease Quantity
# -----------------------------
@app.route("/decrease/<item>")
def decrease(item):

    if item in cart:

        cart[item]["qty"] -= 1

        if cart[item]["qty"] <= 0:
            del cart[item]

    return redirect("/cart")

# -----------------------------
# Remove Item
# -----------------------------
@app.route("/remove/<item>")
def remove(item):

    if item in cart:
        del cart[item]

    return redirect("/cart")

# -----------------------------
# Checkout → Move to Past Orders
# -----------------------------
from datetime import datetime

@app.route("/checkout")
def checkout():

    if not cart:
        return redirect("/cart")

    order_items = []
    subtotal = 0

    for item in cart:
        price = cart[item]["price"]
        qty = cart[item]["qty"]

        item_total = price * qty
        subtotal += item_total

        order_items.append({
            "name": item,
            "price": price,
            "qty": qty,
            "subtotal": item_total
        })

        past_orders.append({
            "item": item,
            "price": price,
            "qty": qty
        })

    gst = round(subtotal * 0.18, 2)
    grand_total = subtotal + gst

    now = datetime.now()
    date = now.strftime("%d %B %Y")
    time = now.strftime("%I:%M %p")

    cart.clear()

    return render_template(
        "bill.html",
        items=order_items,
        subtotal=subtotal,
        gst=gst,
        total=grand_total,
        date=date,
        time=time
    )


# -----------------------------
# Past Orders Page
# -----------------------------
@app.route("/orders")
def orders():
    return render_template("orders.html", orders=past_orders)

# -----------------------------
# Profile Page
# -----------------------------
@app.route("/profile", methods=["GET","POST"])
def profile():

    global current_username, current_password

    if request.method == "POST":

        current_username = request.form["username"]
        current_password = request.form["password"]

    return render_template(
        "profile.html",
        username=current_username,
        password=current_password
    )

# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    return redirect("/login")

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
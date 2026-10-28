import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, redirect, url_for
  
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def index():
    cart = session.get('cart', {})
    selected_addons = session.get('selected_addons', {})
    flowers, addons = load_data()
    total = calculate_total(cart, selected_addons)
    return render_template("index.html", flowers=flowers, addons=addons, cart=cart, selected_addons=selected_addons, total=total)

# Calculate total cost based on cart contents and selected addons
def calculate_total(cart, selected_addons):
    total = sum(item['price'] * item['quantity'] for item in cart.values()) 
    # total = total + sum(item['price'] for item in selected_addons.values()) 
    # total= total + sum(select_addons.values)
    return total  

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/checkout")
def checkout():
    return render_template("invoice.html")

def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
    with open('data/addons.json') as file:    
        addons=json.load(file)

    return flowers, addons

# Add selected flower to the shopping cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower']  # get slected flower name
    quantity = int(request.form['quantity']) # convert quantity to a number
    flowers, addons = load_data()  # get flower data from file, ignore addon data
    cart = session.get('cart', {})  # get cart from session or start fresh

    if flower not in flowers:
        flash("Invalid flower selected.")
        return redirect(url_for('home'))

    if flower in cart:
        cart[flower]['quantity'] += quantity  # add existing quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }     

    session['cart'] = cart  # update session
    session.modified = True  # force Flask to save it
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))


@app.route('/select_addons', methods=['POST'])
def select_addons():
    flash(f"function named select_addons works")
    return redirect(url_for('index'))

# Remove an item from the shopping cart
@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})

    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"{item} remove from cart.")
    else:
        flash("Item not found in cart")


    return redirect(url_for('index'))


  
  
# Add selected addons to the session
@app.route('/select_addon', methods=['POST'])  
def select_addon():
    selected_addons = {}
    _,   addons = load_data()  # we only need addons 
    
    # Reading back the andons selected in the index.html
    selected_keys = request.form.getlist('addons') 

    for addon in selected_keys:
        if addon in addons:
            selected_addons[addon] = float(addons[addon]['price']) 

    session['selected_addons'] = selected_addons
    session.modified = True
    return redirect(url_for('index')) 

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    flash(f"function named select_addons works")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

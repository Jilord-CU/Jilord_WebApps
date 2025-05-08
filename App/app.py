from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
Bootstrap(app)

# Product data
technologies = [
    { "number": "0", "image": "/static/metro.jpg", "name": "Metro Rimless Close Coupled Modern Toilet", "price": 189.95, "description": "Modern Toilet with sleek design." },
    { "number": "1", "image": "/static/bidet.jpg", "name": "Back to Wall Smart Bidet Japanese Toilet", "price": 599.97, "description": "Smart bidet with advanced features." },
    { "number": "2", "image": "/static/gold-toilet.jpg", "name": "Court Art Style Luxury Bathroom Toilet", "price": 1781.99, "description": "Luxury gold-plated toilet." },
    { "number": "3", "image": "/static/concrete-toilet.jpg", "name": "Nipomo in Ash", "price": 721.00, "description": "Concrete bathroom sink." },
    { "number": "4", "image": "/static/washbasin.jpg", "name": "Furniture Washbasin", "price": 179.99, "description": "Spacious design washbasin." },
    { "number": "5", "image": "/static/rectangle-sink.jpg", "name": "Ceramic Washbasin", "price": 224.99, "description": "Durable ceramic washbasin." }
]

# Forms
class PaymentForm(FlaskForm):
    name = StringField('Name on Card', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Submit Payment')

# Routes
@app.route('/')
def galleryPage():
    return render_template('index.html', technologies=technologies)

@app.route('/tech/<string:techId>', methods=['GET', 'POST'])
def singleProductPage(techId):
    product = next((t for t in technologies if t["number"] == techId), None)
    if product is None:
        return redirect(url_for('galleryPage'))

    opinion = session.get('opinions', {}).get(techId, '')

    if request.method == 'POST':
        opinion = request.form.get('opinion')
        session.setdefault('opinions', {})[techId] = opinion
        session.modified = True

    return render_template('SingleTech.html', technology=product, opinion=opinion)

@app.route('/add_to_basket/<string:techId>', methods=['POST'])
def add_to_basket(techId):
    product = next((t for t in technologies if t["number"] == techId), None)
    if product is None:
        return redirect(url_for('galleryPage'))

    quantity = request.form.get('quantity', type=int, default=1)
    session.setdefault('basket', {})

    if techId in session['basket']:
        session['basket'][techId]['quantity'] += quantity
    else:
        session['basket'][techId] = {
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'image': product['image']
        }

    session.modified = True
    return redirect(url_for('view_basket'))

@app.route('/basket')
def view_basket():
    if 'basket' not in session or not session['basket']:
        return render_template('empty_basket.html')

    total_price = round(sum(item['price'] * item['quantity'] for item in session['basket'].values()), 2)

    # Optional: round each item total
    for item in session['basket'].values():
        item['total'] = round(item['price'] * item['quantity'], 2)

    return render_template('basket.html', basket=session['basket'], total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = PaymentForm()
    if form.validate_on_submit():
        # Store order summary
        session['last_order'] = {
            'items': session.get('basket', {}),
            'total': round(sum(item['price'] * item['quantity'] for item in session['basket'].values()), 2),
            'card_name': form.name.data
        }
        session.pop('basket', None)
        return redirect(url_for('payment_success'))
    return render_template('checkout.html', form=form)

@app.route('/payment_success')
def payment_success():
    order = session.get('last_order')
    return render_template('payment_success.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)
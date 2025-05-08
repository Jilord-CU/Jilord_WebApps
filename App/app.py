from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
Bootstrap(app)

technologies = [
    { "number": "0", "image": "/static/metro.jpg", "name": "Metro Rimless Close Coupled Modern Toilet", "price": "189.95", "description": "To give your bathroom an up-to-the-minute look opt for this Modern Toilet from Metro. It's a close coupled toilet, meaning the cistern is attached to the bowl as a single unit. The sleek pan is easy to keep clean. With a projection of 650mm, this neat and compact piece won't hog space in smaller bathrooms. It's supplied with a wrap-over seat that has soft-close hinges great for preserving your peaceful bathroom ambience. Its rimless design, with no hidden areas for germs to linger, makes it a more hygienic choice. Estimated Carbon Footprint: Approximately 50 to 100 kg CO₂e per unit. Standard ceramic toilets typically have a higher environmental impact due to energy-intensive manufacturing processes, including the firing of ceramics at high temperatures." },
    { "number": "1", "image": "/static/bidet.jpg", "name": "Back to Wall Smart Bidet Japanese Toilet", "price": "599.97", "description": "Experience the future of comfort and hygiene with the Back-to-Wall Smart Bidet Japanese Toilet. Designed for sleek sophistication, this toilet seamlessly fits against your wall, creating a modern, clean look while maximizing space. Equipped with advanced features, including a heated seat, adjustable water temperature, and a built-in bidet for a gentle, soothing cleanse, it offers unparalleled convenience. The intelligent, touchless controls allow for a personalized experience, while the self-cleaning system ensures long-lasting freshness. Estimated Carbon Footprint: Approximately 100 to 200 kg CO₂e per unit. Smart bidets often incorporate advanced technologies that may increase energy consumption. However, features like water-saving flush mechanisms and energy-efficient heating can help mitigate their environmental impact." },
    { "number": "2", "image": "/static/gold-toilet.jpg", "name": "Court Art Style Luxury Bathroom Toilet Seat Golden Split Piece Toilet", "price": "1781.99", "description": "Transform your bathroom into a palace with the Golden Toilet. Featuring a stunning gold-plated finish, this luxurious toilet combines elegance and advanced flushing technology. Its sleek design offers both comfort and efficiency, while the durable gold coating resists stains and tarnish. Perfect for those who want to add a touch of opulence to their space. Estimated Carbon Footprint: Approximately 150 to 300 kg CO₂e per unit. Luxury items with gold-plated finishes may have a higher environmental impact due to the energy-intensive processes involved in gold plating and the use of precious metals." },
    { "number": "3", "image": "/static/concrete-toilet.jpg", "name": "Nipomo in Ash", "price": "721", "description": "Adaptable? Check. Resourceful? Absolutely. Stunning? See for yourself! This concrete bathroom sink is perfect for clean design styles, in oh-so-many ways. Install as an apron-front sink, undermount sink or vessel sink; its soft rectangular shape shows off the organic beauty of NativeStone concrete, at a much lighter weight and with no-fuss maintenance. Estimated Carbon Footprint: Approximately 70 to 150 kg CO₂e per unit. Manufactured using locally sourced recycled sands and aggregates, this sink boasts 80 percent recycled content. The production process is low-energy, and the product is fully recyclable at the end of its life." },
    { "number": "4", "image": "/static/washbasin.jpg", "name": "Furniture Washbasin", "price": "179.99", "description": "This furniture washbasin has an especially spacious design, providing enough room for your most important accessories. The furniture washbasin can be combined with washbasin countertops or furniture in any style of bath making it the right choice to create a comfortable atmosphere in your bathroom. Estimated Carbon Footprint: Approximately 50 to 120 kg CO₂e per unit. The environmental impact varies depending on the materials used. Ceramic basins typically have a higher footprint due to energy-intensive manufacturing processes." },
    { "number": "5", "image": "/static/rectangle-sink.jpg", "name": "Ceramic Washbasin", "price": "224.99", "description": "A ceramic washbasin combines elegance and durability, offering a smooth, glossy surface that resists stains and scratches. Its timeless design fits seamlessly into any bathroom or powder room, providing both style and functionality for everyday use. Ideal for creating a clean, modern aesthetic, this washbasin is easy to maintain and built to last. Estimated Carbon Footprint: Approximately 60 to 130 kg CO₂e per unit. Ceramic basins are durable and long-lasting but are energy-intensive to produce, especially when fired at high temperatures." }
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
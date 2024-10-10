from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Regexp
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Shirt(db.Model):
    __tablename__ = 'retro_shirts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False) 
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    environmental_impact = db.Column(db.String(20), nullable=False)
    environmental_explanation = db.Column(db.Text, nullable=False)

class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shirt_id = db.Column(db.Integer, db.ForeignKey('retro_shirts.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    shirt = db.relationship('Shirt', backref=db.backref('basket_items', lazy=True))

class BasketForm(FlaskForm):
    quantity = SelectField('Quantity', choices=[(str(i), str(i)) for i in range(1, 4)])
    submit = SubmitField('Add to Basket')

class PaymentForm(FlaskForm):
    credit_card_number = StringField('Credit Card Number', validators=[DataRequired(), Regexp(r'^(\d{4}[- ]?){3}\d{4}$', message='Invalid credit card number format')])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired(), Regexp(r'^\d{2}/\d{2}$', message='Invalid expiry date format')])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Submit Payment')

@app.route('/')
def galleryPage():
    sort_by = request.args.get('sort_by')
    search_query = request.args.get('search', '').lower()
    
    shirts = Shirt.query.all()
    
    if search_query:
        shirts = [shirt for shirt in shirts if search_query in shirt.name.lower()]
    
    if sort_by == 'name':
        shirts.sort(key=lambda x: x.name)
    elif sort_by == 'price':
        shirts.sort(key=lambda x: x.price)
    elif sort_by == 'environmental_impact':
        impact_order = {"Low": 1, "Moderate": 2, "High": 3}
        shirts.sort(key=lambda x: impact_order.get(x.environmental_impact, 0))
    
    form = BasketForm()
    return render_template('index.html', retro_shirts=shirts, form=form)

@app.route('/shirt/<int:shirtID>', methods=['GET', 'POST'])
def singleProductPage(shirtID):
    index = shirtID 
    
    form = BasketForm()
    shirt = Shirt.query.get_or_404(index)
    if form.validate_on_submit():
        quantity = int(form.quantity.data)
        item = BasketItem.query.filter_by(shirt_id=index).first()
        if item:
            item.quantity += quantity
        else:
            item = BasketItem(shirt_id=index, quantity=quantity)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for('basketPage'))
    return render_template('SingleShirt.html', retro_shirt=shirt, form=form)

@app.route('/basket')
def basketPage():
    basket_item_ids = session.get('basket', [])
    basket_items = BasketItem.query.filter(BasketItem.id.in_(basket_item_ids)).all()
    total_price = sum(item.quantity * item.shirt.price for item in basket_items)
    return render_template('basket.html', basket_items=basket_items, total_price=total_price)

@app.route('/delete/<int:itemID>', methods=['POST'])
def deleteItem(itemID):
    item = BasketItem.query.get_or_404(itemID)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('basketPage'))

@app.route('/add-to-basket/<int:shirtID>', methods=['POST'])
def addToBasket(shirtID):
    form = BasketForm()
    shirt = Shirt.query.get_or_404(shirtID)
    if form.validate_on_submit():
        quantity = int(form.quantity.data)
        item = BasketItem.query.filter_by(shirt_id=shirtID).first()
        if item:
            item.quantity += quantity
        else:
            item = BasketItem(shirt_id=shirtID, quantity=quantity)
            db.session.add(item)
        db.session.commit()
        flash('Item added to basket', 'success')
        
        session['basket'] = [item.id for item in BasketItem.query.all()]
        
        return redirect(url_for('basketPage'))
    return redirect(url_for('galleryPage'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutPage():
    form = PaymentForm()
    if form.validate_on_submit():
        db.session.query(BasketItem).delete()  
        db.session.commit()
        return render_template('checkout_success.html')
    return render_template('checkout.html', form=form)

@app.route('/get-description/<int:shirtID>')
def get_description(shirtID):
    shirt = Shirt.query.get_or_404(shirtID)
    return shirt.description

if __name__ == '__main__':

    app.run(debug=True, port=5050)

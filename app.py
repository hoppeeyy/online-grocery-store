from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Change this for production!

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    image = db.Column(db.String(100), default='default-product.jpg')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

# Initialize Database with Sample Data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Add sample products if none exist
        if not Product.query.first():
            sample_products = [
                Product(name="Apple", price=1.20, stock=100, category="Fruits", image="/static/image/apple.jpg"),
                Product(name="Banana", price=0.50, stock=150, category="Fruits", image="/static/image/banana.jpg"),
                Product(name="Milk (1L)", price=2.50, stock=50, category="Dairy", image="/static/image/milk.jpg"),
                Product(name="Eggs (12)", price=3.00, stock=40, category="Dairy", image="/static/image/eggs.jpg"),
                Product(name="Bread", price=1.80, stock=30, category="Bakery", image="/static/image/bread.jpg"),
                Product(name="Tomato", price=0.80, stock=70, category="Vegetables", image="/static/image/tomato.jpg")
            ]
            db.session.add_all(sample_products)
            
            # Create admin user
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                email="admin@store.com"
            )
            db.session.add(admin)
            
            db.session.commit()
            print("✅ Database initialized with sample data!")

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    
    # Check if already in cart
    cart_item = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_id=session['user_id'],
            product_id=product_id
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'Added {product.name} to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)
@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])  # Changed to POST
def remove_from_cart(item_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Get the cart item or return 404
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify the item belongs to the current user
    if cart_item.user_id != session['user_id']:
        flash('Invalid request', 'danger')
        return redirect(url_for('cart'))
    
    # Delete the item
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
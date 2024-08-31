from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a strong key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

db.create_all()

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id="your_google_client_id",
    client_secret="your_google_client_secret",
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Facebook OAuth setup
facebook_bp = make_facebook_blueprint(
    client_id="your_facebook_app_id",
    client_secret="your_facebook_app_secret",
    redirect_to="facebook_login"
)
app.register_blueprint(facebook_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index2():
    return render_template('index2.html')

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    info = resp.json()
    
    user = User.query.filter_by(email=info["email"]).first()
    if user is None:
        user = User(username=info["name"], email=info["email"])
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('profile'))

@app.route('/login/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    
    resp = facebook.get("/me?fields=id,name,email")
    assert resp.ok, resp.text
    info = resp.json()
    
    user = User.query.filter_by(email=info["email"]).first()
    if user is None:
        user = User(username=info["name"], email=info["email"])
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    return f"Hello, {current_user.username}! This is your profile page."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

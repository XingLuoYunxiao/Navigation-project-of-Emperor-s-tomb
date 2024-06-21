from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class TangLing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    dynasty = db.Column(db.String(255))
    image = db.Column(db.String(255))
    latitude = db.Column(db.Float)  # 添加纬度字段
    longitude = db.Column(db.Float)  # 添加经度字段
    website = db.Column(db.String(255))
    spots = db.relationship('Spot', backref='tang_ling', lazy=True)  # 添加对景点的关系

class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    tang_ling_id = db.Column(db.Integer, db.ForeignKey('tang_ling.id'), nullable=False)
    
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tang_ling_id = db.Column(db.Integer, db.ForeignKey('tang_ling.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref('itineraries', lazy=True))
    tang_ling = db.relationship('TangLing', backref=db.backref('itineraries', lazy=True))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tang_ling_id = db.Column(db.Integer, db.ForeignKey('tang_ling.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    tang_ling = db.relationship('TangLing', backref=db.backref('reviews', lazy=True))
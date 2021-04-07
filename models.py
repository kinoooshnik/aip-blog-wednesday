from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password})"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), unique=False, nullable=False)
    body = db.Column(db.Text, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('articles', lazy=True))
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Article({self.id}, {self.title}, {self.body})"

from datetime import datetime
from . import db

# Association table for likes (many-to-many relationship between users and posts/comments)
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id'), nullable=True),  # Foreign key to blog_posts
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), nullable=True),  # Foreign key to comments
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)  # Store Google OAuth ID
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    liked_posts = db.relationship(
        'BlogPost',
        secondary=likes,
        primaryjoin="and_(User.id == likes.c.user_id, likes.c.post_id != None)",
        secondaryjoin="BlogPost.id == likes.c.post_id",
        backref='likers'
    )

    liked_comments = db.relationship(
        'Comment',
        secondary=likes,
        primaryjoin="and_(User.id == likes.c.user_id, likes.c.comment_id != None)",
        secondaryjoin="Comment.id == likes.c.comment_id",
        backref='likers'
    )

    def __repr__(self):
        return f'<User {self.name}>'

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment by User {self.author_id} on Post {self.post_id}>'
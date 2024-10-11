from flask import Blueprint, request, jsonify, session
from app.models import db, BlogPost, User
from app.utils.decorators import require_auth, admin_required

# Define the blueprint for posts
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    """
    Get all blog posts.
    Accessible to all users.
    """
    posts = BlogPost.query.all()
    posts_list = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id
        }
        for post in posts
    ]
    return jsonify(posts_list), 200

@posts_bp.route('/', methods=['POST'])
@require_auth
@admin_required
def create_post():
    """
    Create a new blog post.
    Accessible only to admin users.
    """
    title = request.json.get("title")
    content = request.json.get("content")
    author_id = session.get("user_id")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    new_post = BlogPost(title=title, content=content, author_id=author_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully!"}), 201

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@require_auth
@admin_required
def update_post(post_id):
    """
    Update an existing blog post.
    Accessible only to admin users.
    """
    post = BlogPost.query.get_or_404(post_id)
    post.title = request.json.get("title", post.title)
    post.content = request.json.get("content", post.content)
    db.session.commit()
    return jsonify({"message": "Post updated successfully!"}), 200

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@require_auth
@admin_required
def delete_post(post_id):
    """
    Delete a blog post.
    Accessible only to admin users.
    """
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"}), 200
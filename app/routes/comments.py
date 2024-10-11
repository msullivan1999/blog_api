from flask import Blueprint, request, jsonify, session
from app.models import db, Comment, BlogPost
from app.utils.decorators import require_auth

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_list = [{"id": comment.id, "content": comment.content, "author_id": comment.author_id} for comment in comments]
    return jsonify(comments_list), 200

@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@require_auth
def add_comment(post_id):
    post = BlogPost.query.get_or_404(post_id)
    content = request.json.get("content")
    author_id = session.get("user_id")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    new_comment = Comment(content=content, author_id=author_id, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201
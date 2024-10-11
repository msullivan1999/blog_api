from flask import Blueprint, request, jsonify, session
from app.models import db, BlogPost, Comment, likes
from app.utils.decorators import require_auth

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@require_auth
def like_post(post_id):
    user_id = session.get("user_id")
    post = BlogPost.query.get_or_404(post_id)

    if post.likers.filter_by(id=user_id).first():
        return jsonify({"message": "You already liked this post"}), 400

    db.session.execute(likes.insert().values(user_id=user_id, target_id=post.id, target_type='post'))
    db.session.commit()
    return jsonify({"message": "Post liked successfully!"}), 200

@likes_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
@require_auth
def like_comment(comment_id):
    user_id = session.get("user_id")
    comment = Comment.query.get_or_404(comment_id)

    if comment.likers.filter_by(id=user_id).first():
        return jsonify({"message": "You already liked this comment"}), 400

    db.session.execute(likes.insert().values(user_id=user_id, target_id=comment.id, target_type='comment'))
    db.session.commit()
    return jsonify({"message": "Comment liked successfully!"}), 200
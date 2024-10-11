from flask import request, session
from flask_restx import Namespace, Resource
from app.models import db, BlogPost, Comment, likes
from app.utils.decorators import require_auth

# Set up the Namespace for likes
api = Namespace('likes', description='Operations related to liking posts and comments')

@api.route('/posts/<int:post_id>/like')
@api.param('post_id', 'The identifier of the post')
class LikePost(Resource):
    @api.doc('like_post')
    @require_auth
    def post(self, post_id):
        """
        Like a blog post.
        Accessible only to authenticated users.
        """
        user_id = session.get("user_id")
        post = BlogPost.query.get_or_404(post_id)

        if post.likers.filter_by(id=user_id).first():
            return {"message": "You already liked this post"}, 400

        db.session.execute(
            likes.insert().values(user_id=user_id, post_id=post.id)
        )
        db.session.commit()
        return {"message": "Post liked successfully!"}, 200

@api.route('/comments/<int:comment_id>/like')
@api.param('comment_id', 'The identifier of the comment')
class LikeComment(Resource):
    @api.doc('like_comment')
    @require_auth
    def post(self, comment_id):
        """
        Like a comment.
        Accessible only to authenticated users.
        """
        user_id = session.get("user_id")
        comment = Comment.query.get_or_404(comment_id)

        if comment.likers.filter_by(id=user_id).first():
            return {"message": "You already liked this comment"}, 400

        db.session.execute(
            likes.insert().values(user_id=user_id, comment_id=comment.id)
        )
        db.session.commit()
        return {"message": "Comment liked successfully!"}, 200
from flask import request, session
from flask_restx import Namespace, Resource, fields
from app.models import db, Comment, BlogPost
from app.utils.decorators import require_auth

# Set up the Namespace for comments
api = Namespace('comments', description='Operations related to comments on blog posts')

# Define a model for the comment using Flask-RESTx
comment_model = api.model('Comment', {
    'id': fields.Integer(readonly=True, description='The comment identifier'),
    'content': fields.String(required=True, description='The content of the comment'),
    'author_id': fields.Integer(readonly=True, description='The ID of the comment author'),
    'post_id': fields.Integer(readonly=True, description='The ID of the post')
})

@api.route('/posts/<int:post_id>/comments')
@api.param('post_id', 'The identifier of the post')
class PostComments(Resource):
    @api.doc('get_comments')
    @api.marshal_list_with(comment_model)
    def get(self, post_id):
        """
        Get all comments for a specific blog post.
        Accessible to all users.
        """
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments, 200

    @api.doc('add_comment')
    @api.expect(comment_model, validate=True)
    @require_auth
    def post(self, post_id):
        """
        Add a new comment to a specific blog post.
        Accessible only to authenticated users.
        """
        post = BlogPost.query.get_or_404(post_id)
        data = request.json
        content = data.get("content")
        author_id = session.get("user_id")

        if not content:
            return {"error": "Content is required"}, 400

        new_comment = Comment(content=content, author_id=author_id, post_id=post.id)
        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment added successfully!"}, 201
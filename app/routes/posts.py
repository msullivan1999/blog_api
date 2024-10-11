from flask import request, session
from flask_restx import Namespace, Resource, fields
from app.models import db, BlogPost
from app.utils.decorators import require_auth, admin_required

# Set up the Namespace for posts
api = Namespace('posts', description='Blog post related operations')

# Define a model for the blog post using Flask-RESTx
post_model = api.model('BlogPost', {
    'id': fields.Integer(readonly=True, description='The post identifier'),
    'title': fields.String(required=True, description='The post title'),
    'content': fields.String(required=True, description='The post content'),
    'author_id': fields.Integer(readonly=True, description='The ID of the post author')
})

@api.route('/')
class PostList(Resource):
    @api.doc('list_posts')
    @api.marshal_list_with(post_model)
    def get(self):
        """
        Get all blog posts.
        Accessible to all users.
        """
        posts = BlogPost.query.all()
        return posts, 200

    @api.doc('create_post')
    @api.expect(post_model)
    @require_auth
    @admin_required
    def post(self):
        """
        Create a new blog post.
        Accessible only to admin users.
        """
        data = request.json
        title = data.get("title")
        content = data.get("content")
        author_id = session.get("user_id")

        if not title or not content:
            return {"error": "Title and content are required"}, 400

        new_post = BlogPost(title=title, content=content, author_id=author_id)
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post created successfully!"}, 201

@api.route('/<int:post_id>')
@api.param('post_id', 'The post identifier')
class PostResource(Resource):
    @api.doc('get_post')
    @api.marshal_with(post_model)
    def get(self, post_id):
        """
        Get a single blog post based on its ID.
        Accessible to all users.
        """
        post = BlogPost.query.get_or_404(post_id)
        return post, 200

    @api.doc('update_post')
    @api.expect(post_model)
    @require_auth
    @admin_required
    def put(self, post_id):
        """
        Update an existing blog post.
        Accessible only to admin users.
        """
        post = BlogPost.query.get_or_404(post_id)
        data = request.json
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        db.session.commit()
        return {"message": "Post updated successfully!"}, 200

    @api.doc('delete_post')
    @require_auth
    @admin_required
    def delete(self, post_id):
        """
        Delete a blog post.
        Accessible only to admin users.
        """
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully!"}, 200
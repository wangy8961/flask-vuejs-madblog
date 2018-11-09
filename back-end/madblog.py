from app import create_app
from app.extensions import db
from app.models import User, Post
from config import Config


app = create_app(Config)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post}

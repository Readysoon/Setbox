from flask_login import LoginManager
from app.extensions.database.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

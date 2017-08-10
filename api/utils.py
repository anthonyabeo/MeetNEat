from api.models import User


def verify_credentials(username_or_token, password):
    # first try to authenticate by token
    user = User.confirm_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    return True, user

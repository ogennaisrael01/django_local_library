from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    User = get_user_model()

    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = self.User.objects.get(email=username)
            if user.check_password(password):
                return user
            
            else:
                return None
        except self.User.DoesNotExist as e:
            return f"Error: {e}"
        
    def get_user(self, user_id):
        try:
            user = self.User.objects.get(id=user_id)
            return user
        except Exception as e:
            return e 
        
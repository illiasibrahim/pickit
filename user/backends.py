from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel

class CustomModelBackend(ModelBackend):
    def authenticate(self,request,username = None,password=None,**kwargs):
        UserModel = get_user_model()
        if password is None:
            if username is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)
            try:
                case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
                user = UserModel._default_manager.get(**{case_insensitive_username_field : username})
            except UserModel.DoesNotExist:
                return None
            else:
                if self.user_can_authenticate(user):
                    return user

        else:
            if username is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)

            try:
                case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
                user = UserModel._default_manager.get(**{case_insensitive_username_field : username})
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user



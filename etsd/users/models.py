from django.contrib.auth.models import AbstractUser


# Use custom user model by default as per
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass

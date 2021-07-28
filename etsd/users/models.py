from django.contrib.auth.models import AbstractUser


# Use custom user model by default as per
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    def __str__(self):
        return '{0} ({1})'.format(self.get_full_name(), self.username)

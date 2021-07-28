import django.contrib.auth.backends


class NoLoginModelBackend(django.contrib.auth.backends.ModelBackend):
    """
    Don't allow login for model-based users - please be careful this
    is needed to allow using django permissions!
    """

    def authenticate(self, username=None, password=None):
        return None

from . import models

def get_authority_users(authority):
    return models.User.objects.filter(authorities=authority)

def get_authority_users_emails(authority):
    return [usr.email for usr in get_authority_users(authority)]

def get_admin_emails():
    return [usr.email for usr in models.User.objects.filter(is_staff=1)]
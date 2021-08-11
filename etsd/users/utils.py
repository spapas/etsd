from . import models

def get_authority_users(authority):
    return models.User.objects.filter(authorities=authority)

def get_authority_users_emails(authority):
    return [usr.email for usr in get_authority_users(authority)]
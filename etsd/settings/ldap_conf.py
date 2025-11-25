import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion


AUTH_LDAP_BIND_DN = "uid=admin,ou=system"
AUTH_LDAP_BIND_PASSWORD = "secret"
AUTH_LDAP_SERVER_URI = "ldap://localhost:10389"

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("ou=users,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
)
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "cn",
    "last_name": "sn",
    "email": "mail",
}
AUTH_LDAP_PROFILE_ATTR_MAP = {}
AUTH_LDAP_ALWAYS_UPDATE_USER = True

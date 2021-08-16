from django.template.loader import get_template


def send_mail_body(template_path, email_ctx):
    email_template = get_template(template_path)
    return email_template.render(email_ctx)


def authority_str(au):
    return "{0} {1}".format(au.kind.name, au.name)


def authority_kind_str(ak):
    return ak.name

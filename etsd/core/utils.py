from django.template.loader import get_template

def send_mail_body(template_path, email_ctx):
    email_template = get_template(template_path)
    return email_template.render(email_ctx)

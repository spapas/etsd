from django.conf import settings


def default_cp(request):
    return {"site_id": settings.SITE_ID}

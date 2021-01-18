from django.conf import settings


def site(request):
    vars = {
        'site': settings.SITE_NAME,
        'url': settings.SITE_URL,
        'email': settings.EMAIL_HOST_USER,
    }
    return {
        'vars': vars
    }

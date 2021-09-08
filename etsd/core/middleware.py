from django.conf import settings


def cors_debug_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if settings.DEBUG:
            response["Access-Control-Allow-Origin"] = "*"
            response[
                "Access-Control-Allow-Methods"
            ] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response

    return middleware

from django.conf import settings

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


def add_security_schemes(result, generator, request, public):
    """
    Postprocessing hook to ensure securitySchemes are included in the schema
    """
    if 'components' not in result:
        result['components'] = {}

    if 'securitySchemes' not in result['components']:
        result['components']['securitySchemes'] = {}

    # Add BearerAuth security scheme
    result['components']['securitySchemes']['BearerAuth'] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT Bearer token authentication. Format: Bearer <jwt_token>"
    }

    return result


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.JWTAuthentication"
    name = "BearerAuth"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token authentication. Format: Bearer <jwt_token>"
        }

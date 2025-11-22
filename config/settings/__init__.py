"""
Django settings for config project.

This file determines which environment settings to load based on the
DJANGO_ENV environment variable.

- development: config.settings.dev
- production: config.settings.prod
- Default: development settings
"""

import os

# Determine which environment settings to use
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")

if DJANGO_ENV == "production":
    from .prod import *
else:
    # Default to development settings
    from .dev import *

# Allow environment-specific overrides
locals().update(globals())

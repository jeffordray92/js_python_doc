"""

The **jumpstart.context_processors.py** file add the site name and domain variables into the contexts of every template.

"""

from django.conf import settings

def site_settings(request):
    """Includes site settings variable into the contexts of the project's templates

    **Arguments:**
        * request: a Web request

    **Attributes:**
        * SITE_NAME: The general name of the site
        * SITE_DOMAIN: The general domain for the site

    **Returns:**
        * ctx: The context containing the SITE_NAME and SITE_DOMAIN information

    """

    ctx = {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
    }
    return ctx

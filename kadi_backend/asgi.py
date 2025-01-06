"""
ASGI config for kadi_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kadi_backend.settings')
from channels.routing import ProtocolTypeRouter
# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # WebSocket handling will be added here later
})
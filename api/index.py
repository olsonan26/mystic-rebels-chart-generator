"""Vercel ASGI entrypoint; identical calculation service to local development."""
from mystic_rebels.api import app as chart_app
from site_access import SitePasswordGate

app = SitePasswordGate(chart_app)

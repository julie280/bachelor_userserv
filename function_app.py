from azure.functions import AsgiFunctionApp, AuthLevel
from api import app as fastapi_app

app = AsgiFunctionApp(
    app=fastapi_app,

    http_auth_level=AuthLevel.ANONYMOUS
)

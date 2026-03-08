from azure.functions import AsgiFunctionApp, AuthLevel
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk._logs import LoggingHandler
from api import app as fastapi_app

configure_azure_monitor(connection_string="InstrumentationKey=47218f74-4d43-4f0f-8f49-c960351da91c;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/;ApplicationId=d6a2da06-ee7d-4b7d-9855-739d1d1d6cd4")

app = AsgiFunctionApp(
    app=fastapi_app,

    http_auth_level=AuthLevel.ANONYMOUS
)

from opentelemetry import trace
from opentelemetry.trace import SpanKind
import logging
from opentelemetry.sdk._logs import LoggingHandler

from Models.models import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = LoggingHandler()
logger.addHandler(handler)


def log_new_user(user_db: User):
    logger.info("New User registered", extra={"user_id": str(user_db.user_id)})
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("HTTP Request", kind=SpanKind.SERVER) as span:
        span.set_attribute("custom_dimension", str(user_db.user_id))
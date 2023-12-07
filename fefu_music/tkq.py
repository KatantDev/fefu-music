import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker

from fefu_music.settings import settings

broker = ZeroMQBroker()

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()  # type: ignore

taskiq_fastapi.init(
    broker,
    "fefu_music.web.application:get_app",
)

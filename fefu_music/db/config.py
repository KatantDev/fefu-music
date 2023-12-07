from typing import List

from fefu_music.settings import settings

MODELS_MODULES: List[str] = [
    "fefu_music.db.models.user_model",
    "fefu_music.db.models.refresh_token_model",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}

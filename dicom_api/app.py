import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2
from aiohttp import web

from dicom_api.common import init_config
from dicom_api.constants import PROJECT_PATH
from dicom_api.handler import ApiHandler
from dicom_api.storage import InMemoryStorage

logger = logging.getLogger(__name__)


def create_api_v1_app():
    api_v1_app = web.Application()
    api_v1_handler = ApiHandler(app=api_v1_app)
    api_v1_handler.register(api_v1_app)
    return api_v1_app


def init_jinja2(app: web.Application) -> None:
    """
    Initialize jinja2 template for application.
    """
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(PROJECT_PATH / "templates"))
    )


async def start_background_tasks(app):
    app["background_pooling"] = app.loop.create_task(app["storage"].update_records())


async def cleanup_background_tasks(app):
    logger.info("cleanup background tasks...")
    app["background_pooling"].cancel()
    await app["background_pooling"]


async def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = create_api_v1_app()
    aiohttp_debugtoolbar.setup(app, check_host=False)
    init_config(app, config=config)
    app["storage"] = await InMemoryStorage.create(
        storage_config=app["config"]["storage"]
    )
    init_jinja2(app)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.router.add_static("/static/", path=(PROJECT_PATH / "static"), name="static")
    return app


async def create_app() -> web.Application:
    app = await init_app()
    return app

import asyncio
import logging

from aiohttp import web

from .app import create_app


def init_logging():
    logging.basicConfig(
        # TODO (A Danshyn 06/01/18): expose in the Config
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    init_logging()
    loop = asyncio.get_event_loop()

    app = loop.run_until_complete(create_app())

    logging.info("Loaded app config: %r", app["config"])

    app_settings = app["config"]["app"]
    web.run_app(app, host=app_settings["host"], port=app_settings["port"])


if __name__ == "__main__":
    main()

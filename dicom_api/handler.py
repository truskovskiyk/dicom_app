from typing import Any, Dict

import aiohttp_jinja2
from aiohttp import web

from dicom_api.storage import InMemoryStorage


class ApiHandler:
    def __init__(self, *, app: web.Application):
        self._app = app

    @property
    def _storage(self) -> InMemoryStorage:
        return self._app["storage"]

    def register(self, app):
        app.add_routes(
            [
                web.get("/ping", self.handle_ping),
                web.get("/records_logs", self.records, name="records_logs"),
                web.get("/", self.handle_index),
            ]
        )

    async def handle_ping(self, request):
        return web.json_response("pong")

    @aiohttp_jinja2.template("index.html")
    async def handle_index(self, request) -> Dict[str, Any]:
        return {"test": "test"}

    async def records(self, request):
        records = self._storage.get_records_as_json()
        data = {"tags": records}
        return web.json_response(data)

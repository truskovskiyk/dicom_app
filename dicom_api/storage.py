import asyncio
import itertools
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Set

import matplotlib.pyplot as plt
import pydicom
from dataclasses import dataclass
from pydicom.filereader import read_dicomdir

from dicom_api.constants import PROJECT_PATH

logger = logging.getLogger(__name__)


class Storage(ABC):
    @abstractmethod
    def update_records(self):
        pass


@dataclass
class Record:
    name: str
    dataset: pydicom.Dataset


class InMemoryStorage(Storage):
    @classmethod
    async def create(cls, storage_config: Dict[str, str]):
        inst = cls(storage_path=Path(storage_config["path"]))
        await inst._update_records()
        return inst

    _records: List[Record]
    _records_set: Set[str]

    def __init__(self, *, storage_path: Path):
        self._path = storage_path
        self._records = []
        self._records_set = set()

    @property
    def static_path(self) -> Path:
        return Path(f"{PROJECT_PATH}/static/images")

    async def get_record(self, file_name: Path) -> Record:
        # TODO blocking function
        record = Record(name=file_name.name, dataset=pydicom.dcmread(str(file_name)))
        # TODO do not use matplotlib
        plt.imshow(record.dataset.pixel_array, cmap=plt.cm.bone)
        image_path = f"{self.static_path}/{file_name.name}.svg"
        plt.savefig(image_path)
        return record

    async def _send_email(self, record: Record):
        # TODO check record and send email
        # if and only if the DICOM transfer has more than 30 slices
        pass

    async def _update_records(self):
        # TODO remove hardcode "CT"
        index_name = "CT"

        files = [x for x in self._path.iterdir() if x.name.startswith(index_name)]
        for x in files:
            if x.name not in self._records_set:
                logger.info(f"new file {x}")
                r = await self.get_record(x)
                self._records.append(r)
                self._records_set.add(r.name)
                await self._send_email(r)

    async def update_records(self):
        # TODO move running logic to separate object
        # TODO expose configuration
        time_out = 1
        logger.info("update_records")
        while True:
            await asyncio.sleep(time_out)
            logger.info(f"start update_records: now {len(self._records)}")
            await self._update_records()
            logger.info(f"done update_records: now {len(self._records)}")

    def get_records_as_json(self) -> List[Dict[str, str]]:
        records_as_json = []
        for record in self._records:
            x_dics = {}
            for k in record.dataset.keys():
                key = str(record.dataset[k].name)
                if key != "Pixel Data":
                    value = str(record.dataset[k].value)
                    x_dics[key] = value
            image_path = f"{record.name}.svg"
            x_dics["image_url"] = image_path
            records_as_json.append(x_dics)
        return records_as_json

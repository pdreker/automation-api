from importlib import metadata

from fastapi import FastAPI

from .api import hello, tasmota_switch
from .internal import admin, health

app = FastAPI()
app.include_router(hello.router)
app.include_router(tasmota_switch.router)
app.include_router(admin.router)
app.include_router(health.router)


try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = "develop"
finally:
    del metadata

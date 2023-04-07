from fastapi import APIRouter

from ..mqtt import MQTTClient

router = APIRouter(prefix="/hello", tags=["hello"])


@router.get("/")
async def hello_world():
    return "Hello, World!"


@router.get("/mqtt")
def mqtt_hello():
    # Use the MQTT client connection in the endpoint function
    client = MQTTClient()
    client.publish("my/topic", "Hello, world!")
    return {"message": "Message sent"}


# @router.get("/{who}")
# async def hello_someone(who: str):
#     return f"Hello, {who}!"

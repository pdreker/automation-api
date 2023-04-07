from fastapi import APIRouter

from ..mqtt import MQTTClient

router = APIRouter(prefix="/tasmota/switch", tags=["tasmota", "switch"])


@router.get("/{name}")
async def get_switch_state(name: str):
    return {"name": name, "state": "not implemented"}


@router.put("/{name}")
async def set_switch_state(name: str, state: bool):
    client = MQTTClient()
    client.publish(f"tasmota/cmnd/{name}/POWER", "ON" if state else "OFF")
    return {"name": name, "state": state, "message": "Message sent"}

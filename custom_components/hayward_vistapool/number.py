from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VistaPoolCoordinator

NUMBER_DEFINITIONS = {
    "orp_setpoint": {
        "path": "modules.rx.status.value",
        "name": "ORP Setpoint",
        "min": 0,
        "max": 1000,
        "step": 1,
        "unit": "mV",
        "field_type": "integer",
    },
    "ph_low_setpoint": {
        "path": "modules.ph.status.low_value",
        "name": "pH Low Setpoint",
        "min": 6.0,
        "max": 8.5,
        "step": 0.1,
        "unit": "pH",
        "field_type": "string_ph_hundredths",
    },
    "ph_high_setpoint": {
        "path": "modules.ph.status.high_value",
        "name": "pH High Setpoint",
        "min": 6.0,
        "max": 8.5,
        "step": 0.1,
        "unit": "pH",
        "field_type": "string_ph_hundredths",
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: VistaPoolCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [VistaPoolNumber(coordinator, sensor_id, definition) for sensor_id, definition in NUMBER_DEFINITIONS.items()]
    async_add_entities(entities)


class VistaPoolNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, sensor_id: str, definition: dict):
        super().__init__(coordinator)
        self._id = sensor_id
        self._definition = definition
        self._attr_name = f"VistaPool {definition['name']}"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_number"
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_native_unit_of_measurement = definition["unit"]
        self._attr_mode = "box"

    @property
    def native_value(self):
        raw = self.coordinator.data
        value = raw.get(self._definition["path"].replace(".", "_"))
        if value is None:
            return None
        field_type = self._definition["field_type"]
        if field_type == "integer":
            return float(value)
        if field_type == "string_ph_hundredths":
            return round(float(value) / 100.0, 2)
        return float(value)

    async def async_set_native_value(self, value: float) -> None:
        field_type = self._definition["field_type"]
        if field_type == "integer":
            payload = int(round(value))
            await self.coordinator.async_write_field(self._definition["path"], payload, "integer")
            return
        if field_type == "string_ph_hundredths":
            payload = str(int(round(value * 100)))
            await self.coordinator.async_write_field(self._definition["path"], payload, "string")
            return
        await self.coordinator.async_write_field(self._definition["path"], value, "integer")

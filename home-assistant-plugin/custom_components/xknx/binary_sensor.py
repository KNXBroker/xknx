"""Support for KNX/IP binary sensors."""
from typing import Any, Dict, Optional

from xknx.devices import BinarySensor as XknxBinarySensor

from homeassistant.components.binary_sensor import DEVICE_CLASSES, BinarySensorEntity
from homeassistant.core import HomeAssistant
from .const import ATTR_COUNTER, DOMAIN
from .knx_entity import KnxEntity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up binary sensor(s) for KNX platform."""
    entities = []
    for device in hass.data[DOMAIN].xknx.devices:
        if isinstance(device, XknxBinarySensor):
            entities.append(KNXBinarySensor(device, hass))
    async_add_entities(entities)


class KNXBinarySensor(KnxEntity, BinarySensorEntity):
    """Representation of a KNX binary sensor."""

    def __init__(self, device: XknxBinarySensor, hass: HomeAssistant):
        """Initialize of KNX binary sensor."""
        if device.value_template is not None:
            device.value_template.hass = hass
        super().__init__(device)

    @property
    def device_class(self):
        """Return the class of this sensor."""
        if self._device.device_class in DEVICE_CLASSES:
            return self._device.device_class
        return None

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        state = self._device.is_on()
        template = self._device.value_template
        if template is not None and state is not None:
            state = template.async_render_with_possible_json_value(state)
        return state

    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return device specific state attributes."""
        return {ATTR_COUNTER: self._device.counter}

    @property
    def force_update(self) -> bool:
        """
        Return True if state updates should be forced.

        If True, a state change will be triggered anytime the state property is
        updated, not just when the value changes.
        """
        return self._device.ignore_internal_state

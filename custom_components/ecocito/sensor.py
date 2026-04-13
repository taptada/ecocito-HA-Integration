from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
  CONF_SELECTED_SENSORS,
  DEFAULT_SELECTED_SENSORS,
  DOMAIN,
  SENSOR_DEFINITIONS,
)
from .coordinator import EcocitoCoordinator


@dataclass(frozen=True)
class EcocitoSensorDescription:
  key: str
  name: str
  icon: str
  unit: str


async def async_setup_entry(
  hass: HomeAssistant,
  entry: ConfigEntry,
  async_add_entities: AddEntitiesCallback,
) -> None:
  coordinator: EcocitoCoordinator = hass.data[DOMAIN][entry.entry_id]

  selected_sensors: list[str] = entry.options.get(
    CONF_SELECTED_SENSORS,
    DEFAULT_SELECTED_SENSORS,
  )

  entities = []
  for key in selected_sensors:
    definition = SENSOR_DEFINITIONS[key]
    description = EcocitoSensorDescription(
      key=key,
      name=definition["name"],
      icon=definition["icon"],
      unit=definition["unit"],
    )
    entities.append(EcocitoSensor(coordinator, entry, description))

  async_add_entities(entities)


class EcocitoSensor(CoordinatorEntity[EcocitoCoordinator], SensorEntity):
  """Representation of an Ecocito sensor."""

  _attr_has_entity_name = True
  _attr_state_class = SensorStateClass.MEASUREMENT

  def __init__(
    self,
    coordinator: EcocitoCoordinator,
    entry: ConfigEntry,
    description: EcocitoSensorDescription,
  ) -> None:
    super().__init__(coordinator)
    self.entity_description = description
    self._attr_translation_key = description.key
    self._attr_unique_id = f"{entry.entry_id}_{description.key}"
    self._attr_name = description.name
    self._attr_icon = description.icon
    self._attr_native_unit_of_measurement = description.unit

  @property
  def native_value(self) -> int | None:
    if self.coordinator.data is None:
      return None
    return self.coordinator.data.get(self.entity_description.key)
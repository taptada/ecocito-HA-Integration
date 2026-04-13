from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
  SensorEntity,
  SensorEntityDescription,
  SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
  CONF_SELECTED_SENSORS,
  DEFAULT_SELECTED_SENSORS,
  DOMAIN,
  SENSOR_DEFINITIONS,
)
from .coordinator import EcocitoCoordinator


@dataclass(frozen=True, kw_only=True)
class EcocitoSensorDescription(SensorEntityDescription):
  """Description d'un capteur Ecocito."""


async def async_setup_entry(
  hass: HomeAssistant,
  entry: ConfigEntry,
  async_add_entities: AddEntitiesCallback,
) -> None:
  """Set up Ecocito sensors from a config entry."""
  coordinator: EcocitoCoordinator = hass.data[DOMAIN][entry.entry_id]

  selected_sensors: list[str] = entry.options.get(
    CONF_SELECTED_SENSORS,
    DEFAULT_SELECTED_SENSORS,
  )

  entities: list[EcocitoSensor] = []
  for key in selected_sensors:
    definition = SENSOR_DEFINITIONS[key]

    description = EcocitoSensorDescription(
      key=key,
      translation_key=key,
      icon=definition["icon"],
      native_unit_of_measurement=definition["unit"],
      state_class=SensorStateClass.TOTAL,
      device_class=None,
    )

    entities.append(EcocitoSensor(coordinator, entry, description))

  async_add_entities(entities)


class EcocitoSensor(CoordinatorEntity[EcocitoCoordinator], SensorEntity):
  """Representation of an Ecocito sensor."""

  entity_description: EcocitoSensorDescription
  _attr_has_entity_name = True
  _attr_suggested_display_precision = 0

  def __init__(
    self,
    coordinator: EcocitoCoordinator,
    entry: ConfigEntry,
    description: EcocitoSensorDescription,
  ) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator)

    self.entity_description = description
    self._entry = entry

    self._attr_unique_id = f"{entry.entry_id}_{description.key}"

  @property
  def native_value(self) -> int | None:
    """Return the current sensor value."""
    if self.coordinator.data is None:
      return None

    value = self.coordinator.data.get(self.entity_description.key)
    if value is None:
      return None

    return int(value)

  @property
  def last_reset(self):
    """Return the start of the current yearly counter cycle.

    Ecocito returns a cumulative value over the current year only,
    so the counter effectively resets on January 1st.
    """
    now = dt_util.now()
    return now.replace(
      month=1,
      day=1,
      hour=0,
      minute=0,
      second=0,
      microsecond=0,
    )
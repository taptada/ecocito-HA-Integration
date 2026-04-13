from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import EcocitoCoordinator

type EcocitoConfigEntry = ConfigEntry


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
  """Set up Ecocito integration."""
  return True


async def async_setup_entry(hass: HomeAssistant, entry: EcocitoConfigEntry) -> bool:
  """Set up Ecocito from a config entry."""
  coordinator = EcocitoCoordinator(hass, entry)
  await coordinator.async_config_entry_first_refresh()

  hass.data.setdefault(DOMAIN, {})
  hass.data[DOMAIN][entry.entry_id] = coordinator

  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  return True


async def async_unload_entry(hass: HomeAssistant, entry: EcocitoConfigEntry) -> bool:
  """Unload a config entry."""
  unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
  if unload_ok:
    hass.data[DOMAIN].pop(entry.entry_id, None)
  return unload_ok
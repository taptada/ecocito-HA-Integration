from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

import requests
from requests import Session
from requests.exceptions import RequestException

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
  BASE_URL,
  CONF_CC,
  CONF_SELECTED_SENSORS,
  DEFAULT_SCAN_INTERVAL,
  DEFAULT_SELECTED_SENSORS,
  LOGIN_PATH,
  SENSOR_DEFINITIONS,
)

_LOGGER = logging.getLogger(__name__)


class EcocitoApi:
  """Simple Ecocito API client."""

  def __init__(
    self,
    cc: str,
    user: str,
    password: str,
    selected_sensors: list[str],
  ) -> None:
    self._cc = cc
    self._user = user
    self._password = password
    self._selected_sensors = selected_sensors

  @property
  def _login_url(self) -> str:
    return f"https://{self._cc}.ecocito.com{LOGIN_PATH}"

  def _build_url(self, service: str, year: int, type_matiere: int) -> str:
    return BASE_URL.format(
      cc=self._cc,
      service=service,
      year=year,
      type_matiere=type_matiere,
    )

  def _login(self, session: Session) -> None:
    payload = {
      "Identifiant": self._user,
      "MotDePasse": self._password,
      "MaintenirConnexion": "false",
      "FranceConnectActif": "False",
    }

    response = session.post(self._login_url, data=payload, timeout=30)
    response.raise_for_status()

  @staticmethod
  def _get_year_total(data: list[dict[str, Any]]) -> int:
    return sum(int(elem.get("Nombre", 0)) for elem in data)

  def test_connection(self) -> None:
    with requests.Session() as session:
      self._login(session)

      year = datetime.now().year
      first_key = self._selected_sensors[0]
      definition = SENSOR_DEFINITIONS[first_key]

      response = session.get(
        self._build_url(
          definition["service"],
          year,
          definition["matiere"],
        ),
        timeout=30,
      )
      response.raise_for_status()
      response.json()

  def fetch_stats(self) -> dict[str, int]:
    year = datetime.now().year
    results: dict[str, int] = {}

    try:
      with requests.Session() as session:
        self._login(session)

        for key in self._selected_sensors:
          definition = SENSOR_DEFINITIONS[key]
          response = session.get(
            self._build_url(
              definition["service"],
              year,
              definition["matiere"],
            ),
            timeout=30,
          )
          response.raise_for_status()
          results[key] = self._get_year_total(response.json())

    except RequestException as err:
      raise UpdateFailed(f"HTTP error while fetching Ecocito data: {err}") from err
    except ValueError as err:
      raise UpdateFailed(f"Invalid JSON returned by Ecocito: {err}") from err

    return results


class EcocitoCoordinator(DataUpdateCoordinator[dict[str, int]]):
  """Ecocito data coordinator."""

  def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
    self.entry = entry

    selected_sensors: list[str] = entry.options.get(
      CONF_SELECTED_SENSORS,
      DEFAULT_SELECTED_SENSORS,
    )

    self.api = EcocitoApi(
      cc=entry.data[CONF_CC],
      user=entry.data[CONF_USERNAME],
      password=entry.data[CONF_PASSWORD],
      selected_sensors=selected_sensors,
    )

    super().__init__(
      hass,
      _LOGGER,
      name="Ecocito",
      update_interval=DEFAULT_SCAN_INTERVAL,
    )

  async def _async_update_data(self) -> dict[str, int]:
    return await self.hass.async_add_executor_job(self.api.fetch_stats)
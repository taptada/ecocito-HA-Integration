from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, OptionsFlowWithReload
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
  CONF_CC,
  CONF_SELECTED_SENSORS,
  DEFAULT_SELECTED_SENSORS,
  DOMAIN,
  SENSOR_DEFINITIONS,
)
from .coordinator import EcocitoApi


def _sensor_choices() -> dict[str, str]:
  return {key: value["name"] for key, value in SENSOR_DEFINITIONS.items()}


class EcocitoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  """Handle a config flow for Ecocito."""

  VERSION = 1

  async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
    errors: dict[str, str] = {}

    if user_input is not None:
      if not user_input[CONF_SELECTED_SENSORS]:
        errors["base"] = "no_sensor_selected"
      else:
        api = EcocitoApi(
          cc=user_input[CONF_CC],
          user=user_input[CONF_USERNAME],
          password=user_input[CONF_PASSWORD],
          selected_sensors=user_input[CONF_SELECTED_SENSORS],
        )

        try:
          await self.hass.async_add_executor_job(api.test_connection)
        except Exception:
          errors["base"] = "cannot_connect"
        else:
          await self.async_set_unique_id(
            f"{user_input[CONF_CC]}::{user_input[CONF_USERNAME]}"
          )
          self._abort_if_unique_id_configured()

          return self.async_create_entry(
            title=f"Ecocito {user_input[CONF_CC]}",
            data={
              CONF_CC: user_input[CONF_CC],
              CONF_USERNAME: user_input[CONF_USERNAME],
              CONF_PASSWORD: user_input[CONF_PASSWORD],
            },
            options={
              CONF_SELECTED_SENSORS: user_input[CONF_SELECTED_SENSORS],
            },
          )

    schema = vol.Schema(
      {
        vol.Required(CONF_CC): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(
          CONF_SELECTED_SENSORS,
          default=DEFAULT_SELECTED_SENSORS,
        ): cv.multi_select(_sensor_choices()),
      }
    )

    return self.async_show_form(
      step_id="user",
      data_schema=schema,
      errors=errors,
    )

  async def async_step_reconfigure(
    self, user_input: dict[str, Any] | None = None
  ) -> FlowResult:
    """Handle a reconfiguration flow."""
    errors: dict[str, str] = {}
    entry = self._get_reconfigure_entry()

    if user_input is not None:
      api = EcocitoApi(
        cc=user_input[CONF_CC],
        user=user_input[CONF_USERNAME],
        password=user_input[CONF_PASSWORD],
        selected_sensors=entry.options.get(
          CONF_SELECTED_SENSORS,
          DEFAULT_SELECTED_SENSORS,
        ),
      )

      try:
        await self.hass.async_add_executor_job(api.test_connection)
      except Exception:
        errors["base"] = "cannot_connect"
      else:
        await self.async_set_unique_id(
          f"{user_input[CONF_CC]}::{user_input[CONF_USERNAME]}"
        )
        self._abort_if_unique_id_mismatch()

        return self.async_update_reload_and_abort(
          entry,
          data_updates={
            CONF_CC: user_input[CONF_CC],
            CONF_USERNAME: user_input[CONF_USERNAME],
            CONF_PASSWORD: user_input[CONF_PASSWORD],
          },
        )

    schema = vol.Schema(
      {
        vol.Required(CONF_CC, default=entry.data[CONF_CC]): str,
        vol.Required(CONF_USERNAME, default=entry.data[CONF_USERNAME]): str,
        vol.Required(CONF_PASSWORD, default=entry.data[CONF_PASSWORD]): str,
      }
    )

    return self.async_show_form(
      step_id="reconfigure",
      data_schema=schema,
      errors=errors,
    )

  @staticmethod
  @callback
  def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowWithReload:
    return EcocitoOptionsFlow()


class EcocitoOptionsFlow(OptionsFlowWithReload):
  """Handle Ecocito options."""

  async def async_step_init(
    self, user_input: dict[str, Any] | None = None
  ) -> FlowResult:
    if user_input is not None:
      if not user_input[CONF_SELECTED_SENSORS]:
        return self.async_show_form(
          step_id="init",
          data_schema=self.add_suggested_values_to_schema(
            vol.Schema(
              {
                vol.Required(CONF_SELECTED_SENSORS): cv.multi_select(
                  _sensor_choices()
                ),
              }
            ),
            user_input,
          ),
          errors={"base": "no_sensor_selected"},
        )

      return self.async_create_entry(data=user_input)

    schema = vol.Schema(
      {
        vol.Required(CONF_SELECTED_SENSORS): cv.multi_select(_sensor_choices()),
      }
    )

    return self.async_show_form(
      step_id="init",
      data_schema=self.add_suggested_values_to_schema(
        schema,
        {
          CONF_SELECTED_SENSORS: self.config_entry.options.get(
            CONF_SELECTED_SENSORS,
            DEFAULT_SELECTED_SENSORS,
          )
        },
      ),
    )
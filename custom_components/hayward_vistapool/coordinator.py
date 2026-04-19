from __future__ import annotations

import logging
from datetime import timedelta

from aiohttp import ClientSession
from urllib.parse import urlencode
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import DOMAIN, FIREBASE_LOGIN_URL, FIRESTORE_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

BROWSER_HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://hayward.vistapool.es",
    "referer": "https://hayward.vistapool.es/",
    "x-client-version": "Chrome/JsCore/5.5.0/FirebaseCore-web",
    "x-firebase-locale": "de-DE",
    "x-browser-channel": "stable",
    "x-browser-year": "2026",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
}


class VistaPoolCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, email: str, password: str, pool_id: str,
                 scan_interval: int = DEFAULT_SCAN_INTERVAL, enable_debug: bool = False):
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{pool_id}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.email = email
        self.password = password
        self.pool_id = pool_id
        self._id_token: str | None = None
        self.enable_debug = enable_debug

    async def _async_update_data(self):
        try:
            if not self._id_token:
                await self._async_login()

            headers = {"Authorization": f"Bearer {self._id_token}"}
            url = FIRESTORE_URL.format(pool_id=self.pool_id)

            async with ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()
                    if resp.status != 200 or "fields" not in data:
                        raise UpdateFailed(f"VistaPool[{self.pool_id}]: bad response {resp.status} → {data}")

                    parsed = self._parse_data(data)
                    if self.enable_debug:
                        _LOGGER.debug("VistaPool[%s]: Parsed data %s", self.pool_id, parsed)
                    return parsed
        except Exception as err:
            _LOGGER.exception("VistaPool[%s]: update failed (%s)", self.pool_id, err)
            raise UpdateFailed(f"VistaPool update failed: {err}") from err

    async def _async_login(self):
        async with ClientSession(headers=BROWSER_HEADERS) as session:
            payload = {"email": self.email, "password": self.password, "returnSecureToken": True}
            async with session.post(FIREBASE_LOGIN_URL, json=payload) as resp:
                login_data = await resp.json()
                if resp.status != 200 or "idToken" not in login_data:
                    raise UpdateFailed(f"VistaPool login failed {resp.status} → {login_data}")
                self._id_token = login_data["idToken"]
                _LOGGER.info("VistaPool[%s]: login successful", self.pool_id)

    async def async_write_field(self, field_path: str, value, field_type: str = "integer"):
        if not self._id_token:
            await self._async_login()

        query = urlencode({"updateMask.fieldPaths": field_path})
        url = FIRESTORE_URL.format(pool_id=self.pool_id) + f"?{query}"

        leaf_key = "integerValue" if field_type == "integer" else "stringValue"
        encoded_value = str(int(value)) if field_type == "integer" else str(value)
        parts = field_path.split('.')
        nested = {leaf_key: encoded_value}
        for part in reversed(parts):
            nested = {"mapValue": {"fields": {part: nested}}}
        payload = {"fields": nested["mapValue"]["fields"]}

        try:
            async with ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self._id_token}",
                    "Content-Type": "application/json",
                }
                async with session.patch(url, headers=headers, json=payload) as resp:
                    data = await resp.json()
                    if resp.status == 401:
                        self._id_token = None
                        await self._async_login()
                        return await self.async_write_field(field_path, value, field_type)
                    if resp.status != 200:
                        raise UpdateFailed(f"VistaPool write failed {resp.status} → {data}")
            await self.async_request_refresh()
        except Exception as err:
            _LOGGER.exception("VistaPool[%s]: write failed for %s=%s (%s)", self.pool_id, field_path, value, err)
            raise UpdateFailed(f"VistaPool write failed: {err}") from err

    def _parse_data(self, data: dict) -> dict:
        fields = data.get("fields")
        if not fields:
            raise UpdateFailed("VistaPool: missing fields in response")

        parsed = {}
        for key, val in fields.items():
            parsed.update(self._flatten(key, val))
        return parsed

    def _flatten(self, key: str, value: dict) -> dict:
        if "stringValue" in value:
            return {key: value["stringValue"]}
        if "integerValue" in value:
            return {key: int(value["integerValue"])}
        if "doubleValue" in value:
            return {key: float(value["doubleValue"])}
        if "booleanValue" in value:
            return {key: bool(value["booleanValue"])}
        if "mapValue" in value:
            result = {}
            for sub_key, sub_val in value["mapValue"].get("fields", {}).items():
                result.update(self._flatten(f"{key}_{sub_key}", sub_val))
            return result
        return {}

from typing import Any, Dict, List, Optional

import requests


class PurpleAirAPIError(Exception):
    """Custom exception for errors interacting with PurpleAir API."""
    pass

class PurpleAirClient:
    BASE_URL = "https://api.purpleair.com/v1"

    def __init__(self, api_key: str, timeout: float = 10.0):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    def _request(self, method: str, path: str,
                 params: Optional[Dict[str, Any]] = None,
                 json_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{path}"
        resp = requests.request(method, url,
                                headers=self.headers,
                                params=params,
                                json=json_body,
                                timeout=self.timeout)
        if resp.status_code < 200 or resp.status_code >= 300:
            try:
                err = resp.json()
            except ValueError:
                err = resp.text
            raise PurpleAirAPIError(f"Error {resp.status_code} {method} {url}: {err}")
        try:
            return resp.json()
        except ValueError as e:
            raise PurpleAirAPIError(f"Non-JSON response {method} {url}: {e}")

    # ----- Organization endpoints -----
    #
    # Documentation is lighter here; adjust if your account has more operations.

    def get_organization(self) -> Dict[str, Any]:
        """
        GET /v1/organization
        Retrieve details of the organization to which your API key belongs.
        """
        path = "/organization"
        return self._request("GET", path)


    # ----- Sensor endpoints -----

    def get_sensor(self, sensor_index: int, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        GET /v1/sensors/{sensor_index}
        Retrieve real-time (or latest) data for a specific sensor.
        :param sensor_index: sensor’s unique index
        :param fields: list of fields to include (optional)
        """
        path = f"/sensors/{sensor_index}"
        params: Dict[str, Any] = {}
        if fields:
            params["fields"] = ",".join(fields)
        return self._request("GET", path, params=params)

    def get_sensors(self, sensor_indices: List[int], fields: Optional[List[str]] = None,
                    show_only: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        GET /v1/sensors
        Retrieve real-time data for multiple sensors.
        :param sensor_indices: list of sensor_index values
        :param fields: list of fields to include
        :param show_only: optional filter to show only certain sensor indices
        """
        path = "/sensors"
        params: Dict[str, Any] = {}
        if sensor_indices:
            params["sensor_index"] = ",".join(str(i) for i in sensor_indices)
        if show_only:
            params["show_only"] = ",".join(str(i) for i in show_only)
        if fields:
            params["fields"] = ",".join(fields)
        return self._request("GET", path, params=params)

    def get_sensor_history(self, sensor_index: int,
                            start_timestamp: int,
                            end_timestamp: int,
                            average: Optional[str] = None,
                            fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        GET /v1/sensors/{sensor_index}/history
        Retrieve historical data for a given sensor, between given timestamps.
        Requires that your key/account has access to history endpoints.
        :param sensor_index: sensor index
        :param start_timestamp: UNIX epoch (seconds) or as required by API
        :param end_timestamp: UNIX epoch
        :param average: averaging interval (e.g. “1h”, “24h”, etc.), if supported
        :param fields: which fields to return
        """
        path = f"/sensors/{sensor_index}/history"
        params: Dict[str, Any] = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp
        }
        if average:
            params["average"] = average
        if fields:
            params["fields"] = ",".join(fields)
        return self._request("GET", path, params=params)

    # ----- Group endpoints -----

    def create_group(self, name: str) -> Dict[str, Any]:
        """
        POST /v1/groups
        Create a new group given a name. Returns group metadata.
        Requires WRITE access.
        """
        path = "/groups"
        body = {"name": name}
        return self._request("POST", path, json_body=body)

    def get_groups(self) -> Dict[str, Any]:
        """
        GET /v1/groups
        List all groups you own.
        """
        path = "/groups"
        return self._request("GET", path)

    def get_group_detail(self, group_id: int) -> Dict[str, Any]:
        """
        GET /v1/groups/{group_id}
        Get detail of a specific group, including its members.
        """
        path = f"/groups/{group_id}"
        return self._request("GET", path)

    def update_group(self, group_id: int, name: Optional[str] = None) -> Dict[str, Any]:
        """
        PUT /v1/groups/{group_id}
        Update metadata for a group (e.g. rename).
        """
        path = f"/groups/{group_id}"
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if not body:
            raise ValueError("No fields to update for group.")
        return self._request("PUT", path, json_body=body)

    def delete_group(self, group_id: int) -> Dict[str, Any]:
        """
        DELETE /v1/groups/{group_id}
        Delete the specified group.
        """
        path = f"/groups/{group_id}"
        return self._request("DELETE", path)

    def add_member_to_group(self, group_id: int, sensor_index: int) -> Dict[str, Any]:
        """
        POST /v1/groups/{group_id}/members
        Add a sensor (by sensor_index) to a group.
        """
        path = f"/groups/{group_id}/members"
        body = {"sensor_index": sensor_index}
        return self._request("POST", path, json_body=body)

    def remove_member_from_group(self, group_id: int, member_id: int) -> Dict[str, Any]:
        """
        DELETE /v1/groups/{group_id}/members/{member_id}
        Remove a member (sensor) from the group.
        """
        path = f"/groups/{group_id}/members/{member_id}"
        return self._request("DELETE", path)

    def get_members_data(self, group_id: int, fields: Optional[List[str]] = None,
                         modified_since: Optional[int] = None) -> Dict[str, Any]:
        """
        GET /v1/groups/{group_id}/members/data
        Get real-time data for all members in a group.
        :param fields: which data fields to include
        :param modified_since: only sensors modified since this timestamp
        """
        path = f"/groups/{group_id}/members/data"
        params: Dict[str, Any] = {}
        if fields:
            params["fields"] = ",".join(fields)
        if modified_since is not None:
            params["modified_since"] = modified_since
        return self._request("GET", path, params=params)

    def get_member_data(self, group_id: int, member_id: int, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        GET /v1/groups/{group_id}/members/{member_id}/data
        Get data for a specific member in a group.
        """
        path = f"/groups/{group_id}/members/{member_id}/data"
        params: Dict[str, Any] = {}
        if fields:
            params["fields"] = ",".join(fields)
        return self._request("GET", path, params=params)

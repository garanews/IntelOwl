# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import requests

from api_app.exceptions import AnalyzerRunException
from api_app.analyzers_manager import classes

from tests.mock_utils import if_mock_connections, patch, MockResponse


class CRXcavator(classes.ObservableAnalyzer):
    name: str = "CRXcavator"
    base_url: str = "https://api.crxcavator.io/v1/report/"

    def run(self):
        try:
            response = requests.get(self.base_url + self.observable_name)
            response.raise_for_status()
        except requests.RequestException as e:
            raise AnalyzerRunException(e)

        result = response.json()
        return result

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "requests.get",
                    return_value=MockResponse({}, 200),
                ),
            )
        ]
        return super()._monkeypatch(patches=patches)

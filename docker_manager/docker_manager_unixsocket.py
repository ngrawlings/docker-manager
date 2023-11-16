import requests
import requests_unixsocket
from typing import Dict, Optional

from docker_manager import os_utils
from docker_manager import DockerManager 

class UnixSocketDockerManager(DockerManager):
    def __init__(self):
        super().__init__()
        self.session = requests_unixsocket.Session()
        self.base_url = "http+unix://%2Fvar%2Frun%2Fdocker.sock"

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_active_containers(self):
        response = self._request('GET', '/containers/json?status=running')
        return [container['Names'][0].strip('/') for container in response]

    def get_exited_containers(self):
        response = self._request('GET', '/containers/json?status=exited')
        return [container['Names'][0].strip('/') for container in response]

    def clean_exited_containers(self):
        containers = self.get_exited_containers()
        for container in containers:
            self._request('DELETE', f'/containers/{container}?force=true')

    def is_docker_running(self):
        try:
            self._request('GET', '/containers/json')
            return True
        except requests.exceptions.RequestException:
            return False

    def stop_active_containers(self):
        containers = self.get_active_containers()
        for container in containers:
            self._request('POST', f'/containers/{container}/stop')

    def stop_container(self, container_name):
        self._request('POST', f'/containers/{container_name}/stop')

    def start_container(self, container_name):
        self._request('POST', f'/containers/{container_name}/start')

    def remove_container(self, container_name):
        self._request('DELETE', f'/containers/{container_name}?force=true')



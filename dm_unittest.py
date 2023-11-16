import unittest
from unittest.mock import patch, MagicMock
from docker_manager import DockerManager
import subprocess
import docker
from docker.errors import NotFound

class TestDockerManager(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()
        cmd = "docker ps"
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            self.skipTest("Docker is not running")
            
    def test_is_docker_running(self):
        result = DockerManager.is_docker_running()
        self.assertTrue(result)

    def test_broker_exists(self):
        container_name = "hummingbot-broker"
        try:
            container = self.client.containers.get(container_name)
        except NotFound:
            self.fail(f"Container {container_name} does not exist")

    def test_container_exists(self):
        container_name = "data_downloader"
        try:
            container = self.client.containers.get(container_name)
        except NotFound:
            self.fail(f"Container {container_name} does not exist")

    def test_container_exists(self):
        container_name = "hummingbot-broker"
        try:
            container = self.client.containers.get(container_name)
        except NotFound:
            self.fail(f"Container {container_name} does not exist")

    def test_get_active_containers(self):
        result = DockerManager.get_active_containers()
        self.assertEqual(result, ['data_downloader', 'hummingbot-broker'])

if __name__ == '__main__':
    unittest.main()
import requests
from utils.logger import logger


class ModelHealthChecker:
    """Performs health checks for registered models"""

    @staticmethod
    def check_endpoint(endpoint: str) -> bool:
        try:
            response = requests.get(endpoint)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Health check failed for endpoint {endpoint}: {e}")
            return False

    @staticmethod
    def check(base_url: str) -> bool:
        base_url = base_url.replace("v1", "")
        health_endpoints = [
            base_url + "health",
            base_url + "status-0123456789abcdef",
        ]
        for endpoint in health_endpoints:
            if ModelHealthChecker.check_endpoint(endpoint):
                logger.info(f"Health check passed at {endpoint}")
                return True

        logger.error(f"Health check failed for {base_url}.")
        return False

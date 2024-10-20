import pytest
import requests


@pytest.fixture(scope="function", autouse=True)
def session():
    session = requests.Session()
    return session

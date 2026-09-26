import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


@pytest.fixture
def mock_provider():
    from app.providers.sports import get_sports_provider

    return get_sports_provider()

import pytest
from hier_conf.hier_conf import (
    create_config,
    lock_config
)


@pytest.fixture(autouse=True, scope="function")
def my_config():
    return create_config()

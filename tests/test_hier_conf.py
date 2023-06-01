import pytest

from hier_conf.hier_conf import (
    create_config,
    lock_config
)

########################################################################################################################


def test_set_value(my_config):
    my_config.banana.color = 'yellow'
    assert my_config.banana.color == 'yellow'


def test_long_value(my_config):
    my_config.very.very.bloody.hell.long.way.to.particular.value = 'banana'
    assert my_config.very.very.bloody.hell.long.way.to.particular.value == 'banana'


def test_overwrite_value(my_config):
    my_config.banana.color = 'yellow'
    with pytest.raises(AttributeError):
        my_config.banana = 123


def test_lock_config(my_config):
    lock_config(my_config)
    with pytest.raises(AttributeError):
        my_config.random_number = 7

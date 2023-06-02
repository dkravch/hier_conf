import pytest

from hier_conf.hier_conf import (
    create_config,
    lock_config,
    unlock_config,
    make_config_item
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


def test_unlock_config(my_config):
    my_config.banana.color = 'yellow'
    lock_config(my_config)
    try:
        my_config.random_number = 7
    except AttributeError:
        pass

    unlock_config(my_config)
    my_config.random_number = 7

    assert my_config.random_number == 7


def test_make_config_item(my_config):
    make_config_item(my_config,
                     '.make.config.item',
                     789)
    make_config_item(my_config,
                     'make.another.config.item',  # Starting dot does not matter
                     123)
    assert my_config.make.config.item == 789
    assert my_config.make.another.config.item == 123

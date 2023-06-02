import pprint

# TODO Type hints

########################################################################################################################


class ConfigItem:

    def __init__(self, name=None):

        self._locked = False
        self._fullname = name if name else ''

    def __getattr__(self, item):
        if not self._locked:
            obj = ConfigItem()
            setattr(self, item, obj)
            obj._fullname = f"{self._fullname}.{item}"
            return obj
        else:
            err_msg = f"Config file does not contain attribute {item}"
            raise AttributeError(err_msg)

    def __setattr__(self, name: str, value) -> None:

        current_value = self.__dict__.get(name, None)
        if isinstance(current_value, ConfigItem):
            raise AttributeError('Rewriting of item having descendants is not allowed, '
                                 'for not to lost them!')
        if name != '_locked' and self._locked:  # Order matters (to avoid endless loop for _locked)!
            raise AttributeError('Current config has been locked!')
        else:
            self.__dict__[name] = value

########################################################################################################################


def _lock(config_obj: ConfigItem, state: bool) -> None:
    setattr(config_obj, '_locked', bool(state))
    for obj_name in config_obj.__dict__:
        if isinstance(config_obj.__dict__[obj_name], ConfigItem):
            setattr(config_obj.__dict__[obj_name], '_locked', state)
            _lock(config_obj.__dict__[obj_name], state)


def lock_config(config_obj: ConfigItem) -> None:
    _lock(config_obj, True)


def unlock_config(config_obj: ConfigItem) -> None:
    _lock(config_obj, False)


def create_config() -> ConfigItem:
    return ConfigItem()


def _get_all_values_as_dict(current_item: ConfigItem, current_result: list) -> dict:
    for key, value in current_item.__dict__.items():
        if key == '_fullname':
            continue
        if isinstance(value, ConfigItem):
            _get_all_values_as_dict(value, current_result)
        else:
            if key != '_locked':
                current_result.append((f"{current_item._fullname}.{key}", value))
    return dict(current_result)


def get_config_as_dict(config_obj: ConfigItem) -> dict:
    result = []
    return _get_all_values_as_dict(current_item=config_obj, current_result=result)


def make_config_item(config_obj: ConfigItem, line: str, value) -> None:
    obj = config_obj
    names = line.lstrip('.').split('.')
    for name in names[:-1]:
        obj = getattr(obj, name)
    setattr(obj, names[-1], value)


########################################################################################################################


if __name__ == '__main__':

    my_config = create_config()

    my_config.banana.color = 'yellow'
    my_config.banana.taste = 'sweet'

    my_config.car.color = 'red'
    my_config.car.engine.type = 'electric'
    my_config.car.vendor = 'Tesla'
    my_config.car.weight = 1000
    # config_obj.car.weight.units = 1000  # AttributeError: 'int' object has no attribute 'units'

    lock_config(my_config)
    # my_config.random_number = 7  # AttributeError: Current config has been locked!
    # my_config.skate.color = 'grey'
    unlock_config(my_config)
    my_config.random_number = 7
    my_config.random_number = 777

    print(my_config.banana.color)
    # my_config.banana = 9 # AttributeError, for not to lost sub-items

    my_config.bloody.hell.long.windly.too.random_number = 777

    print(my_config.car.color)
    print(my_config.car)

    def print_color(conf_obj):
        print(conf_obj.color)

    print_color(my_config.car)
    print_color(my_config.banana)

    my_config.car.seats = 5
    my_config.car.seats = 5
    my_config.car = 5
    try:
        my_config.car.seats = 5
    except AttributeError as e:
        print(e)



    pprint.pprint(get_config_as_dict(my_config))

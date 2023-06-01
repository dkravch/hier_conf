import pprint

# TODO Type hints

########################################################################################################################


class ConfigItem:

    # _locked = False

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

    def __setattr__(self, name, value):

        current_value = self.__dict__.get(name, None)
        if isinstance(current_value, ConfigItem):
            raise AttributeError('Rewriting of already assigned attributes is '  # TODO Rephrase
                                 'not permitted see ConfigItem class '
                                 'docstring explanation')
        if name != '_locked' and self._locked:  # Order matters (to avoid endless loop for _locked)!
            raise AttributeError('Current config has been locked!')
        else:
            self.__dict__[name] = value

    def get_all_values_as_dict(self, item=None, result=None):
        if result is None:
            result = []
        if item is None:
            item = self

        for key, value in item.__dict__.items():
            if key == '_fullname':
                continue
            if isinstance(value, ConfigItem):
                self.get_all_values_as_dict(value, result)
            else:
                result.append((f"{item._fullname}.{key}", value))
        return dict(result)

    def make_item(self, line, value):
        obj = self
        names = line.split('.')
        for name in names[:-1]:
            obj = getattr(obj, name)
        setattr(obj, names[-1], value)


########################################################################################################################

def _lock(config_obj, state):
    setattr(config_obj, '_locked', state)
    for obj_name in config_obj.__dict__:
        if isinstance(config_obj.__dict__[obj_name], ConfigItem):
            setattr(config_obj.__dict__[obj_name], '_locked', state)
            _lock(config_obj.__dict__[obj_name], state)


def lock_config(config_obj):
    _lock(config_obj, True)


def unlock_config(config_obj):
    _lock(config_obj, False)


def create_config():
    return ConfigItem()


def _get_all_values_as_dict(current_item, current_result):
    for key, value in current_item.__dict__.items():
        if key == '_fullname':
            continue
        if isinstance(value, ConfigItem):
            _get_all_values_as_dict(value, current_result)
        else:
            if key != '_locked':
                current_result.append((f"{current_item._fullname}.{key}", value))
    return dict(current_result)


def get_config_as_dict(config_obj):
    result = []
    return _get_all_values_as_dict(current_item=config_obj, current_result=result)


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

    try:
        my_config.car.seats = 5
    except AttributeError as e:
        print(e)

    print(my_config.get_all_values_as_dict())
    pprint.pprint(get_config_as_dict(my_config))

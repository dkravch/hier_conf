from typing import Any, Dict, List, Optional, Tuple

########################################################################################################################


class ConfigItem:
    def __init__(self: ConfigItem, name: Optional[str] = None) -> None:  # noqa: F821

        self._locked = False
        self._fullname = name if name else ""

    def __getattr__(self: ConfigItem, item: str) -> ConfigItem:  # noqa: F821
        if not self._locked:
            obj = ConfigItem()
            setattr(self, item, obj)
            obj._fullname = f"{self._fullname}.{item}"
            return obj
        else:
            err_msg = f"Config object does not contain attribute {item}"
            raise AttributeError(err_msg)

    def __setattr__(self: ConfigItem, name: str, value: Any) -> None:  # noqa: F821

        current_value = self.__dict__.get(name, None)
        if isinstance(current_value, ConfigItem):
            raise AttributeError(
                "Rewriting of item having descendants is not allowed, "
                "for not to lost them!"
            )
        if (
            name != "_locked" and self._locked
        ):  # Order matters (to avoid endless loop for _locked)!
            raise AttributeError("Current config has been locked!")
        else:
            self.__dict__[name] = value

    def __repr__(self: ConfigItem) -> str:  # noqa: F821
        return f"ConfigItem('{self._fullname}')"


########################################################################################################################


def _lock(config_obj: ConfigItem, state: bool) -> None:
    setattr(config_obj, "_locked", bool(state))
    for obj_name in config_obj.__dict__:
        if isinstance(config_obj.__dict__[obj_name], ConfigItem):
            setattr(config_obj.__dict__[obj_name], "_locked", state)
            _lock(config_obj.__dict__[obj_name], state)


def lock_config(config_obj: ConfigItem) -> None:
    _lock(config_obj, True)


def unlock_config(config_obj: ConfigItem) -> None:
    _lock(config_obj, False)


def create_config() -> ConfigItem:
    return ConfigItem()


def _get_all_values_as_dict(
    current_item: ConfigItem, current_result: List[Tuple[str, Any]]
) -> Dict[str, Any]:
    for key, value in current_item.__dict__.items():
        if key == "_fullname":
            continue
        if isinstance(value, ConfigItem):
            _get_all_values_as_dict(value, current_result)
        else:
            if key != "_locked":
                current_result.append((f"{current_item._fullname}.{key}", value))
    return dict(current_result)


def get_config_as_dict(config_obj: ConfigItem) -> Dict[str, Any]:
    result: List[Tuple[str, Any]] = []
    return _get_all_values_as_dict(current_item=config_obj, current_result=result)


def make_config_item(config_obj: ConfigItem, line: str, value: Any) -> None:
    obj = config_obj
    names = line.lstrip(".").split(".")
    for name in names[:-1]:
        obj = getattr(obj, name)
    setattr(obj, names[-1], value)


########################################################################################################################


if __name__ == "__main__":
    my_config = create_config()
    my_config.banana.color = "yellow"

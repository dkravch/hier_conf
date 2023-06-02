# Hierarchical config objects with lightweight syntax


```python
import pprint

from hier_conf.hier_conf import (
    create_config,
    lock_config,
    unlock_config,
    make_config_item,
    get_config_as_dict
)

my_config = create_config()

my_config.banana.color = 'yellow'
my_config.banana.taste = 'sweet'

my_config.car.color = 'red'
my_config.car.engine.type = 'electric'
my_config.car.vendor = 'Tesla'
my_config.car.weight = 1000

pprint.pprint(get_config_as_dict(my_config))

print(my_config.car)
pprint.pprint(get_config_as_dict(my_config.car))
print(my_config.car.weight)
```
Got:
```
{'.banana.color': 'yellow',
 '.banana.taste': 'sweet',
 '.car.color': 'red',
 '.car.engine.type': 'electric',
 '.car.seats': 5,
 '.car.vendor': 'Tesla',
 '.car.weight': 1000,
 '.random_number': 777}
 
ConfigItem('.car')

{'.car.color': 'red',
 '.car.engine.type': 'electric',
 '.car.seats': 5,
 '.car.vendor': 'Tesla',
 '.car.weight': 1000}

1000
```

Notes:
- It is not possible to override something in the middle of chain, for not to lost its descendants
- Once config is formed, it should be explicitly locked. It needs to avoid situations where typo causes new ConfigItem will be returned instead of desired one's value
- No names that contradict python variable naming is allowed, like _my.123smth.value_ or _my.black.and.white_ (_and_ is reserved word) 


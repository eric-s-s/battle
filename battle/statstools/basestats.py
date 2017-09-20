from functools import partial
from typing import Tuple, Any

ParamsTuple = Tuple[str, Any, bool]


class BaseStats(object):
    def __eq__(self, other):
        if not isinstance(other, BaseStats):
            return False
        return self.__class__.__name__ == other.__class__.__name__ and self.__dict__ == other.__dict__

    def update(self, state, new_val):
        private_attr = '_{}'.format(state)
        current_attr = 'current_{}'.format(state)
        if private_attr not in self.__dict__:
            raise AttributeError('No state: {}'.format(state))

        new_dict = self.__dict__.copy()
        new_dict[private_attr] = new_val
        if current_attr in new_dict:
            new_dict[current_attr] = new_val

        new_obj = self.__class__.__new__(self.__class__)
        new_obj.__dict__ = new_dict
        return new_obj


def stats_factory(class_name: str, *params_tuples: ParamsTuple):
    """

    :param class_name: duhhhh
    :param params_tuples: (property_name, default_value, needs_current_value)
    :return:
    """
    class_dict = {}
    for param_vals in params_tuples:
        property_name = param_vals[0]
        private_key = '_{}'.format(property_name)

        def getter(self, val_to_get):
            return self.__getattribute__(val_to_get)

        the_getter = partial(getter, val_to_get=private_key)
        class_dict[property_name] = property(the_getter)

    def __init__(self, *args, **kwargs):
        max_args_index = len(args) - 1
        for index, params in enumerate(params_tuples):
            param_name, default_value, needs_current_value = params

            attr_name = '_{}'.format(param_name)

            if index <= max_args_index:
                attr_value = args[index]
            elif param_name in kwargs:
                attr_value = kwargs[param_name]
            elif default_value is not None:
                attr_value = default_value
            else:
                raise AttributeError('You got a bad init. Bad boy.')

            self.__setattr__(attr_name, attr_value)
            if needs_current_value:
                self.__setattr__('current_{}'.format(param_name), attr_value)

    class_dict['__init__'] = __init__

    return type(class_name, (BaseStats,), class_dict)

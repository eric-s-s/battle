from functools import partial
from typing import Tuple, Any, List

ParamsTuple = Tuple[str, Any, bool]


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

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return all(self.__dict__[key] == other.__dict__[key] for key in self.__dict__)

    class_dict['__eq__'] = __eq__

    def update(self, state, new_val):
        new_dict = self.__dict__.copy()
        new_dict['_{}'.format(state)] = new_val
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.__dict__ = new_dict
        return new_obj

    class_dict['update'] = update

    return type(class_name, (object,), class_dict)

"""
Use dataclasses without variable annotations.

See the typeless() docstring for details.

"""
import dataclasses
import inspect
from typing import Any
from typing import ClassVar


__version__ = '0.1.dev1'


def typeless(cls):
    """Add default annotations to the attributes of a class,
    allowing the class to be used with dataclasses.

    Must be applied before the @dataclass decorator.

    Class attributes that are instances of dataclasses.Field
    become instance attributes of type Any;
    all others remain class attributes of type Any.

    This:

    >>> from dataclasses import dataclass, field
    >>>
    >>> @dataclass
    ... @typeless
    ... class Data:
    ...     one = field()
    ...     two = field(default=2)
    ...     three = 3
    ...
    >>> Data(1)
    Data(one=1, two=2)

    is equivalent to this:

    >>> from typing import Any, ClassVar
    >>>
    >>> @dataclass
    ... class Data:
    ...     one: Any
    ...     two: Any = 2
    ...     three: ClassVar[Any] = 3
    ...
    >>> Data(1)
    Data(one=1, two=2)

    """
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = {}

    for name, thing in cls.__dict__.items():
        if name.startswith('__') and name.endswith('__'):
            continue
        if not _isattribute(thing):
            continue

        if isinstance(thing, dataclasses.Field):
            annotation = Any
        else:
            annotation = ClassVar[Any]

        cls.__annotations__.setdefault(name, annotation)

    return cls


def _isattribute(thing):
    return not any(
        p(thing)
        for p in [
            inspect.isroutine,
            inspect.ismethoddescriptor,
            inspect.isdatadescriptor,
        ]
    )

import dataclasses
import inspect
import typing


def typeless(cls):
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = {}

    for name, thing in cls.__dict__.items():
        if name.startswith('__') and name.endswith('__'):
            continue
        if not isattribute(thing):
            continue

        if isinstance(thing, dataclasses.Field):
            annotation = typing.Any
        else:
            annotation = typing.ClassVar[typing.Any]

        cls.__annotations__.setdefault(name, annotation)

    return cls


def isattribute(thing):
    return not any(
        p(thing)
        for p in [
            inspect.isroutine,
            inspect.ismethoddescriptor,
            inspect.isdatadescriptor,
        ]
    )

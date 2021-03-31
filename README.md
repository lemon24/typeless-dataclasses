**typeless-dataclasses**: use dataclasses without variable annotations


[![build](https://github.com/lemon24/typeless-dataclasses/actions/workflows/build.yaml/badge.svg)](https://github.com/lemon24/typeless-dataclasses/actions/workflows/build.yaml) [![codecov](https://codecov.io/gh/lemon24/typeless-dataclasses/branch/master/graph/badge.svg?token=691LYGEIR4)](https://codecov.io/gh/lemon24/typeless-dataclasses) [![PyPI](https://img.shields.io/pypi/v/typeless-dataclasses)](https://pypi.org/project/typeless-dataclasses/) [![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Have you ever wanted to use dataclasses, but don't like type annotations?

```python
@dataclass
class Data:
    one: Any
    two: Any = 2
```

... and don't want to resort to any [ugly hacks][] like this one?

```python
@dataclass
class Data:
    one: ...
    two: ... = 2
```


With the power of **typeless-dataclasses**, now you can!

```python
@dataclass
@typeless
class Data:
    one = field()
    two = field(default=2)
```


Compare with [attrs][]:

```python
@attr.s
class Data:
    one = attr.ib()
    two = attr.ib(default=2)
```


[ugly hacks]: https://death.andgravity.com/dataclasses#if-not-type-hints-then-what
[attrs]: https://www.attrs.org/


## Installing

Install and update using [pip][]:

```console
$ pip install --upgrade typeless-dataclasses
```

**typeless-dataclasses** offers a type-annotation-free experience for Python 3.6* and newer, and PyPy.

(On 3.6, you also need to install the dataclasses [backport][].)


[pip]: https://pip.pypa.io/en/stable/quickstart/
[backport]: https://pypi.org/project/dataclasses/


## A Simple Example

Using **typeless-dataclasses** is easy!

Just add @typeless to your class before [@dataclass][], and use [field()][] as you normally would; [field()][] attributes become instance variables, and all others remain class variables.

```python
>>> from dataclasses import dataclass, field
>>> from typeless_dataclasses import typeless
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
```

[@dataclass]: https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass
[field()]: https://docs.python.org/3/library/dataclasses.html#dataclasses.field


## Links

* Documentation: https://github.com/lemon24/typeless-dataclasses/blob/master/README.md
* Changes: https://github.com/lemon24/typeless-dataclasses/blob/master/CHANGES.md
* PyPI Releases: https://pypi.org/project/typeless-dataclasses/
* Source Code: https://github.com/lemon24/typeless-dataclasses
* Issue Tracker: https://github.com/lemon24/typeless-dataclasses/issues

**typeless-dataclasses**: use dataclasses without variable annotations.

Have you ever wanted to use dataclasses, but don't like type annotations:

```python
@dataclass
class Data:
    one: Any
    two: Any = 2
```

... and also don't want to resort to any [ugly hacks][] like this one:

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

[any ugly hacks]: https://death.andgravity.com/dataclasses#if-not-type-hints-then-what
[attrs]: https://www.attrs.org/



## Installing

Install and update using [pip][]:

```console
$ pip install --upgrade typeless-dataclasses
```

*typeless-dataclasses* offers a type-annotation-free experience for Python 3.6[^1] and newer, and PyPy.

[^1]: Dataclasses were added to the standard library in Python 3.7; on 3.6, you need to install the [backport][] from PyPI.


[pip]: https://pip.pypa.io/en/stable/quickstart/
[backport]: https://pypi.org/project/dataclasses/


## A Simple Example

Using *typeless-dataclasses* is easy!

Just add @typeless to your class before the [@dataclass][] decorator, and use [field()][] as you normally would; [field()][] attributes become instance variables, and all other attributes remain class variables.

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
[fields()]: https://docs.python.org/3/library/dataclasses.html#dataclasses.field


## Links

* Documentation: https://github.com/lemon24/typeless-dataclasses/blob/master/README.md
* Changes: https://github.com/lemon24/typeless-dataclasses/blob/master/CHANGES.md
* PyPI Releases: https://pypi.org/project/typeless-dataclasses/
* Source Code: https://github.com/lemon24/typeless-dataclasses
* Issue Tracker: https://github.com/lemon24/typeless-dataclasses/issues

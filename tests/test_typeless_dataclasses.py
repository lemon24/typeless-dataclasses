from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import Any
from typing import ClassVar

import pytest
from typeless_dataclasses import typeless


@dataclass
class Typed:
    one: Any
    two: Any = 2
    three: ClassVar[Any] = 3
    four = 4

    @property
    def property(self):
        return self.one * self.two

    def method(self):
        return self.one / self.two

    @classmethod
    def class_method(cls):
        return cls.three + cls.four

    @staticmethod
    def static_method():
        return 0


@dataclass
@typeless
class Typeless:
    one = field()
    two = field(default=2)
    three = 3
    four = 4

    @property
    def property(self):
        return self.one * self.two

    def method(self):
        return self.one / self.two

    @classmethod
    def class_method(cls):
        return cls.three + cls.four

    @staticmethod
    def static_method():
        return 0


@pytest.mark.parametrize('cls', [Typed, Typeless])
def test_class_behaves_normally(cls):
    data = cls(1)

    assert vars(data) == {'one': 1, 'two': 2}
    assert data.three == 3
    assert data.four == 4

    assert data.property == 2
    assert data.method() == 0.5
    assert data.class_method() == 7
    assert data.static_method() == 0

    with pytest.raises(AttributeError):
        cls.one
    assert cls.two == 2
    assert cls.three == 3
    assert cls.four == 4
    assert cls.class_method() == 7
    assert cls.static_method() == 0


def field_data(cls):
    return [
        {name: getattr(field, name) for name in dir(field) if not name.startswith('_')}
        for field in fields(cls)
    ]


def test_fields():
    assert field_data(Typed) == field_data(Typeless)
    assert field_data(Typed(1)) == field_data(Typeless(1))

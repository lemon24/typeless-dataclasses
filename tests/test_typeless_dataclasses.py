from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import Any
from typing import ClassVar

import pytest
from typeless_dataclasses import typeless


def make_typed():
    @dataclass
    class Data:
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

    return Data


def make_typeless():
    @dataclass
    @typeless
    class Data:
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

    return Data


@pytest.mark.parametrize('cls_factory', [make_typed, make_typeless])
def test_class_behaves_normally(cls_factory):
    cls = cls_factory()
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
    Typed = make_typed()
    Typeless = make_typeless()
    assert field_data(Typed) == field_data(Typeless)
    assert field_data(Typed(1)) == field_data(Typeless(1))


def test_annotations_are_the_same():
    Typed = make_typed()
    Typeless = make_typeless()

    common = Typed.__annotations__.keys() & Typeless.__annotations__.keys()
    assert len(common) >= 3

    typed_annotations = {k: Typed.__annotations__[k] for k in common}
    typeless_annotations = {k: Typeless.__annotations__[k] for k in common}
    assert typed_annotations == typeless_annotations


def test_existing_annotations_are_preserved():
    @dataclass
    @typeless
    class Typeless:
        one: int = field()
        two = field(default=2)

    @dataclass
    @typeless
    class Typed:
        one: int
        two: Any = 2

    assert Typed.__annotations__ == Typeless.__annotations__

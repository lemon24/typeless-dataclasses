from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import ClassVar

from typeless_dataclasses import typeless


@dataclass
@typeless
class Data:
    one = field()
    two = field(default=2)
    three = 3


d = Data(1, '')

# reveal_type(Data.__init__)
# reveal_type(d.one)
# reveal_type(d.two)
# reveal_type(d.three)

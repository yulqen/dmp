from dataclasses import dataclass, field


# models
@dataclass
class Inspector:
    id: int = field(init=False)
    name: str

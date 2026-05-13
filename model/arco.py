from dataclasses import dataclass


@dataclass
class Arco:
    nodo1: int
    nodo2: int
    peso: int

    def __lt__(self, other):
        return self.peso<other.peso


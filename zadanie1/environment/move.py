from dataclasses import dataclass, field

@dataclass
class Move:
    startRow: int
    startCol: int
    endRow: int
    endCol: int

    movedPiece: str | None = field(default=None, compare=False)
    capturedPiece: str | None = field(default=None, compare=False)
    promotionPiece: str | None = None
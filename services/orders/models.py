from dataclasses import dataclass, field


@dataclass
class OrderItem:
    item_id: int
    quantity: int

    def to_dict(self):
        return {
            "itemId": self.item_id,
            "quantity": self.quantity
        }


@dataclass
class Order:
    id: int
    student_id: int
    items: list[OrderItem]
    status: str = "placed"

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.student_id,
            "items": [item.to_dict() for item in self.items],
            "status": self.status
        }


@dataclass
class Cart:
    student_id: int
    items: list[OrderItem] = field(default_factory=list)

    def to_dict(self):
        return {
            "studentId": self.student_id,
            "items": [item.to_dict() for item in self.items]
        }
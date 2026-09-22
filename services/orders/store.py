from models import Order, OrderItem, Cart


class Store:
    def __init__(self):
        self.orders = {}
        self.carts = {}
        self.next_order_id = 1

    def create_order(self, student_id, items):
        order = Order(
            id=self.next_order_id,
            student_id=student_id,
            items=items
        )

        self.orders[order.id] = order
        self.next_order_id += 1

        return order

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def list_orders(self, student_id):
        return [
            order for order in self.orders.values()
            if order.student_id == student_id
        ]

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)

        if order:
            order.status = "cancelled"

        return order

    def replace_order(self, order_id, student_id, items):
        """Replace the editable representation of an existing order."""
        order = self.orders.get(order_id)

        if order:
            order.student_id = student_id
            order.items = items

        return order

    def add_cart_item(self, student_id, item_id, quantity):
        if student_id not in self.carts:
            self.carts[student_id] = Cart(student_id)

        cart = self.carts[student_id]

        for item in cart.items:
            if item.item_id == item_id:
                item.quantity += quantity
                return cart

        cart.items.append(OrderItem(item_id, quantity))

        return cart

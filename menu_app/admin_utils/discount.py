from uuid import UUID

from menu_app.admin_utils.parser import form_data


class Discount():
    def __init__(self) -> None:
        self.data = form_data()

    def calculate(self, dish_id: UUID) -> str | None:
        for dish in self.data['dishes']:
            if dish['id'] == str(dish_id):
                if dish['discount']:
                    discount_multiplier = (100 - dish['discount']) / 100
                    result = str(round((dish['price'] * discount_multiplier), 2))
                    return result
        return None

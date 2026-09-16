import unittest

from app.services.cart_service import add_item_to_cart


class CartServiceTests(unittest.TestCase):
    def test_cart_service_is_available(self):
        self.assertTrue(callable(add_item_to_cart))


if __name__ == "__main__":
    unittest.main()

import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:

    def setup_method(self):
        self.burger = Burger()

    def test_set_buns(self):
        bun_mock = Mock()

        self.burger.set_buns(bun_mock)

        assert self.burger.bun == bun_mock

    def test_add_ingredient(self):
        ingredient_mock = Mock()

        self.burger.add_ingredient(ingredient_mock)

        assert len(self.burger.ingredients) == 1 and self.burger.ingredients[0] == ingredient_mock

    def test_remove_ingredient(self):
        ingredient_mock = Mock()

        self.burger.add_ingredient(ingredient_mock)

        self.burger.remove_ingredient(0)

        assert len(self.burger.ingredients) == 0

    def test_move_ingredient_from_last_to_first(self):
        ingredient1_mock = Mock()
        ingredient2_mock = Mock()
        ingredient3_mock = Mock()

        self.burger.add_ingredient(ingredient1_mock)
        self.burger.add_ingredient(ingredient2_mock)
        self.burger.add_ingredient(ingredient3_mock)

        self.burger.move_ingredient(2, 0)

        assert self.burger.ingredients[0] == ingredient3_mock
        assert self.burger.ingredients[1] == ingredient1_mock
        assert self.burger.ingredients[2] == ingredient2_mock

    @pytest.mark.parametrize("bun_price, ingredients_prices, expected_result", [
        (100, [], 200),
        (100, [22], 222),
        (100, [22, 33, 44], 299)
    ])
    def test_get_price(self, bun_price, ingredients_prices, expected_result):
        bun_mock = Mock()
        bun_mock.get_price.return_value = bun_price

        self.burger.set_buns(bun_mock)

        for ingredient_price in ingredients_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = ingredient_price
            self.burger.add_ingredient(mock_ingredient)

        price = self.burger.get_price()

        assert price == expected_result

    @pytest.mark.parametrize("bun_name, bun_price, ingredients_data, expected_result", [
        (
            "black bun", 100,
            [],
            "(==== black bun ====)\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 200"
        ),
        (
            "red bun", 300,
            [("SAUCE", "hot sauce", 100)],
            "(==== red bun ====)\n"
            "= sauce hot sauce =\n"
            "(==== red bun ====)\n"
            "\n"
            "Price: 700"
        ),
        (
            "white bun", 200,
            [("SAUCE", "chili sauce", 300), ("FILLING", "cutlet", 100)],
            "(==== white bun ====)\n"
            "= sauce chili sauce =\n"
            "= filling cutlet =\n"
            "(==== white bun ====)\n"
            "\n"
            "Price: 800"
        ),
        (
            "black bun", 100,
            [
                ("SAUCE", "hot sauce", 100),
                ("SAUCE", "sour cream", 200),
                ("FILLING", "cutlet", 100),
                ("FILLING", "dinosaur", 200),
            ],
            "(==== black bun ====)\n"
            "= sauce hot sauce =\n"
            "= sauce sour cream =\n"
            "= filling cutlet =\n"
            "= filling dinosaur =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 800"
        )
    ])
    def test_get_receipt(self, bun_name, bun_price, ingredients_data, expected_result):
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price
        self.burger.set_buns(mock_bun)

        for i_type, i_name, i_price in ingredients_data:
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = i_type
            mock_ingredient.get_name.return_value = i_name
            mock_ingredient.get_price.return_value = i_price
            self.burger.add_ingredient(mock_ingredient)

        assert self.burger.get_receipt() == expected_result

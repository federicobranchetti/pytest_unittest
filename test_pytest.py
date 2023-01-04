from tester import ShoppingCart
import pytest
from item_database import ItemDatabase
from unittest.mock import MagicMock



#fixture ti permette di creare una sorta di routine riutilizzabile all'interno del test
#non tiutilizza cart
@pytest.fixture
def cart():
    return ShoppingCart(5)

#il mocking è un comportamento simulato e serve per triggerare degli errori

def test_can_add_item_to_cart(cart):
    cart.add("apple")
    #assert si usa per assicurarsi che sia giusti
    #se assert non va fa un'exception e se sale l'exception il test non passa
    assert cart.size() == 1

def test_item_in_cart(cart):
    cart.add("apple")
    assert "apple" in cart.get_items()

#questo test è fatto al contrario, deve fallire e se fallisce va bene
#se esce  Error va bene
def test_over_max_items(cart):
    for _ in range (5):
            cart.add("apple")
    with pytest.raises(OverflowError):
        cart.add("apple")

def test_can_get_total_price(cart):
    print("Testing can get price")
    cart.add("apple")
    cart.add("orange")

    price_map = {
        "apple" : 1.0,
        "orange": 2.0
    }
    assert cart.get_total_price(price_map) == 3.0

#questa direttamente dall'item database con il mock
#unittest.mock 
def test_can_get_total_price_database(cart):
    cart.add("apple") 
    cart.add("orange")
    item_database = ItemDatabase()
    item_database.get = MagicMock(return_value  = 1.0)

    assert cart.get_total_price(item_database) == 2.0

#questa direttamente dall'item database con il mock
#unittest.mock uso il SIDE EFFECT
def test_can_get_total_price_database_side(cart):
    cart.add("apple") 
    cart.add("orange")
    item_database = ItemDatabase()

    def mock_get_item(item:str):
        if item == "apple":
            return 1.0
        if item == "orange":
            return 2.0

    item_database.get = MagicMock(side_effect  = mock_get_item)

    assert cart.get_total_price(item_database) == 3.0



#per andare tutti i test devi fare pytest nel terminale
#per un test standalone  pytest test_pytest.py::test_can_get_total_price
#se metti pytest test_pytest.py::test_can_get_total_price -s fa vedere i print
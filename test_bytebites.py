import pytest
from models import Customer, FoodItem, Menu, Order


# ============================================================================
# ORDER TOTAL TESTS
# ============================================================================

def test_calculate_total_with_multiple_items():
    """Verify that total cost is the sum of all item prices."""
    burger = FoodItem("Burger", 12.99, "Burgers", 4.5)
    soda = FoodItem("Soda", 3.50, "Drinks", 4.2)

    customer = Customer("Alice")
    order = Order(customer, [burger, soda])

    expected_total = 12.99 + 3.50
    assert order.compute_total() == pytest.approx(expected_total, abs=0.01)


def test_order_total_is_zero_when_empty():
    """Verify that an order with no items totals $0."""
    customer = Customer("Bob")
    order = Order(customer)

    assert order.compute_total() == 0


def test_order_total_with_duplicate_items():
    """Verify that adding the same item multiple times sums correctly."""
    burger = FoodItem("Burger", 10.00, "Burgers", 4.5)

    customer = Customer("Charlie")
    order = Order(customer, [burger, burger, burger])

    expected_total = 30.00
    assert order.compute_total() == expected_total


# ============================================================================
# MENU FILTERING TESTS
# ============================================================================

def test_filter_by_category_returns_matching_items():
    """Verify that filtering 'Drinks' returns only drink items."""
    menu = Menu()
    burger = FoodItem("Burger", 10.00, "Burgers", 4.5)
    soda = FoodItem("Soda", 3.50, "Drinks", 4.2)
    sprite = FoodItem("Sprite", 2.99, "Drinks", 4.1)

    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(sprite)

    drinks = menu.filter_by_category("Drinks")

    assert len(drinks) == 2
    assert all(item.category == "Drinks" for item in drinks)


def test_filter_by_category_returns_empty_for_nonexistent_category():
    """Verify that filtering a non-existent category returns an empty list."""
    menu = Menu()
    burger = FoodItem("Burger", 10.00, "Burgers", 4.5)
    soda = FoodItem("Soda", 3.50, "Drinks", 4.2)

    menu.add_item(burger)
    menu.add_item(soda)

    desserts = menu.filter_by_category("Desserts")

    assert len(desserts) == 0


def test_filter_does_not_modify_original_menu():
    """Verify that filtering returns a new list and doesn't modify the menu."""
    menu = Menu()
    burger = FoodItem("Burger", 10.00, "Burgers", 4.5)
    soda = FoodItem("Soda", 3.50, "Drinks", 4.2)

    menu.add_item(burger)
    menu.add_item(soda)

    original_count = len(menu.items)
    drinks = menu.filter_by_category("Drinks")

    assert len(menu.items) == original_count


# ============================================================================
# CUSTOMER VERIFICATION TESTS
# ============================================================================

def test_customer_is_verified_with_purchase_history():
    """Verify that a customer with past orders is a verified user."""
    customer = Customer("Diana")
    burger = FoodItem("Burger", 10.00, "Burgers", 4.5)
    order = Order(customer, [burger])

    customer.purchase_history.append(order)

    assert customer.verify_user() is True


def test_new_customer_is_not_verified():
    """Verify that a new customer with no orders is not verified."""
    customer = Customer("Eve")

    assert customer.verify_user() is False


# ============================================================================
# INTEGRATION TEST
# ============================================================================

def test_full_order_workflow():
    """Verify the complete workflow: menu → filter → order → total → verify."""
    # Setup menu
    menu = Menu()
    burger = FoodItem("Spicy Burger", 12.99, "Burgers", 4.8)
    soda = FoodItem("Large Soda", 3.50, "Drinks", 4.2)
    dessert = FoodItem("Ice Cream", 5.00, "Desserts", 4.7)

    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(dessert)

    # Filter menu
    burgers = menu.filter_by_category("Burgers")
    assert len(burgers) == 1

    # Create customer and order
    customer = Customer("Frank")
    assert customer.verify_user() is False

    order = Order(customer, [burger, soda])
    expected_total = 12.99 + 3.50

    assert order.compute_total() == pytest.approx(expected_total, abs=0.01)

    # Complete purchase
    customer.purchase_history.append(order)
    assert customer.verify_user() is True

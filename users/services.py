import stripe

from config import settings


def create_product(product):
    """ Создание продукта в stripe """

    stripe.api_key = settings.API_KEY
    prod = stripe.Product.create(name=product)
    return prod


def create_price(amount, product):
    """ Создание цены продукта в stripe """

    stripe.api_key = settings.API_KEY
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount,
        product_data={"name": product.get("id")},
    )
    return price

def create_checkout_session(price):
    """ Создание сессии на оплату продукта в stripe """

    stripe.api_key = settings.API_KEY
    session = stripe.checkout.Session.create(
        success_url="https://localhost:8000",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

def retrieve_checkout_session(session_id):
    stripe.api_key = settings.API_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    return session.get("payment_status"), session.get("url")
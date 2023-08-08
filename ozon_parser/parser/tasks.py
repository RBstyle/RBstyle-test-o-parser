from celery import shared_task
from ozon_parser.settings import BASE_DIR
import os

from .utils import get_products, save_product

driver_path = os.path.join(BASE_DIR, "drivers/chromedriver")


@shared_task
def create_product(num_of_products):
    products = get_products(num_of_products=num_of_products)
    save_product(products=products, num_of_products=num_of_products)

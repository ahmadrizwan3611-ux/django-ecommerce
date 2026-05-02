from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = "Seed sample products"

    def handle(self, *args, **kwargs):
        products = [
            {
                "name": "Goat",
                "description": "Healthy goat you buy",
                "price": 35000,
                "stock": 10,
                "category": "eat",
            },
            {
                "name": "Baloon",
                "description": "Air baloon you buy",
                "price": 45000,
                "stock": 5,
                "category": "adventure",
            },
            {
                "name": "Coffee",
                "description": "Good coffee",
                "price": 1000,
                "stock": 20,
                "category": "drink",
            },
        ]

        for item in products:
            Product.objects.get_or_create(
                name=item["name"],
                defaults=item,
            )

        self.stdout.write(self.style.SUCCESS("Products seeded successfully!"))
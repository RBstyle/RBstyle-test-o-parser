from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField(max_length=600)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

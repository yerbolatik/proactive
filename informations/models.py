from django.db import models

# для информаций на сайте через админ-панель


class DeliveryInformation(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ReturnInformation(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField()

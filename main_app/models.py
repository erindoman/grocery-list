from django.db import models
from django.urls import reverse

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores_details', kwargs={'pk': self.id})

class Item(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    quantity = models.IntegerField()
    stores = models.ManyToManyField(Store)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'item_id': self.id})

class Purchase(models.Model):
    date = models.DateField('Purchase date')
    quantity = models.IntegerField()

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.date

    class Meta:
        ordering = ['-date']

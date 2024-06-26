from django.db import models
from apps.base.models import BaseModel

# Create your models here.


class Sevimlilar(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sevimlilar')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.product}"
    
    
class Order(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product}"
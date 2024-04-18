from django.db import models

from apps.accounts.models import User
from apps.base.models import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from colorfield.fields import ColorField
from django.db.models import Avg


COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
        ("#0000FF", "blue",),
        ("#00FF00", "green",),
        ("#FF0000", "red",),

]


PRODUCT_STATUS_CHOICES = (
    ('None', 'None'),
    ('HOT', 'HOT'),
    ('NEW', 'NEW'),
    ('BEST', 'BEST SELL'),
    ('SALE', 'SALE')

)

RATING_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),

)


class Category(BaseModel, MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    icon = models.ImageField(upload_to="icons/", default="default/category.png")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(BaseModel):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="icons/", default="default/brand.png")

    def __str__(self):
        return self.name


class Size(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(BaseModel):
    name = models.CharField(max_length=50)
    code = ColorField(samples=COLOR_PALETTE)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS_CHOICES, default='NEW')
    percentage = models.FloatField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        product_size = self.sizes.all().first()
        return product_size.price

    @property
    def get_new_price(self):
        if self.percentage:
            product_price = self.sizes.all().first().price
            discount = (100 - self.percentage) / 100 * product_price
            return round(discount, 2)
        return 0

    @property
    def get_avg_rating(self):
        rating = self.reviews.all().aggregate(rating_avg=Avg('rating', default=0))
        return round(rating['rating_avg'], 1)


class ProductSize(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='sizes')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, related_name='sizes')
    availability = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product}"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product}"


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=2, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product} | {self.user} | {self.rating}"



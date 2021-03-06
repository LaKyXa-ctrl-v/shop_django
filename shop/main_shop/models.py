from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()


class LastestProductsManager:

    @staticmethod
    def get_products_for_main_page(self, *args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        Products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_models in ct_models:
            model_products = ct_models.model_class(
            )._base_manager.all().order_by('-id')[:5]
            Products.extend(model_products)
        if with_respect_to:
            ct_models = ContentType.objects.filter(model=with_respect_to)
            if ct_models.exists():
                if with_respect_to in args:
                    return sorted(Products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        return Products


class LastestProducts:

    objects = LastestProductsManager


# Create your models here.
# *********
# 1 Category
# 2 Product
# 3 CartProduct
# 4 Cart
# 5 Order
# *********
# 6 Customer
# 7 Specification


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    Content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return f"Продукт: {self.product.title} (Для корзины)"


class Cart(models.Model):

    owner = models.ForeignKey(
        "Customer", verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart',)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    adress = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class CheeseCake(Product):

    height = models.CharField(max_length=255, verbose_name='Высота')
    weight = models.CharField(max_length=255, verbose_name='Вес')
    width = models.CharField(max_length=255, verbose_name='Ширина')
    size = models.CharField(max_length=255, verbose_name='Размер')

    def __str__(self):
        return f"{self.category.name} : {self.title}"

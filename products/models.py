from django.db import models

from users.models import User

from mptt.models import MPTTModel, TreeForeignKey


class ProductCategory(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300, default='Описание')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title


class Product(models.Model):
    category = TreeForeignKey('ProductCategory', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    objects = models.Manager()
    name = models.TextField()
    description = models.TextField(default='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    unit_of_measurement = models.CharField(max_length=50, default='шт')
    image = models.ImageField(upload_to='products_images')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}' #Категория ProductCategory.title?


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': float(self.quantity),
            'price': float(self.sum()),
        }
        return basket_item

    # @classmethod
    # def create_or_update(cls, product_id, user):
    #     baskets = Basket.objects.filter(user=user, product_id=product_id)
    #
    #     if not baskets.exists():
    #         obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
    #         is_created = True
    #         return obj, is_created
    #     else:
    #         basket = baskets.first()
    #         basket.quantity += 1
    #         basket.save()
    #         is_crated = False
    #         return basket, is_crated

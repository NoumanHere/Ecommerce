from django.conf import settings
from django.db import models
from django.shortcuts import reverse
import random

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Profile_image = models.ImageField(upload_to='products/%Y/%m/%d',
                                      blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    image = models.ImageField(blank = True, null = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
<<<<<<< HEAD
        return reverse('core:order_summary',
                       )
    def get_absolute_url(self):
        return reverse('core:product_list_by_category',kwargs={"category_slug": self.slug}
                       )
=======
            return reverse('core:order_summary',
                           )
>>>>>>> 8e79960e736869fa88c3d9b3e3e2e5768ff075bd


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField()
    discount_price = models.FloatField(null=True, blank=True)
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug}
                       )

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={"slug": self.slug}
                       )

    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={"slug": self.slug}
                       )


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.quantity} of {self.item.title}"
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_item_title(self):
        return self.item.title

    def get_single_item_price(self):
        return self.item.price

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_price(self):
        return self.item.discount_price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    email = models.EmailField()

    def random_string():
        return str(random.randint(10000, 99999))
    rand_value = random_string()
    order_id = models.CharField(default=rand_value, max_length=20)
    Product = models.ForeignKey(Item, on_delete=models.CASCADE,
                                blank=True, null=True, db_index=False, related_name='products')
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Billing_Address', on_delete=models.SET_NULL,
                                        blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} with the email {self.email}"


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Billing_Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class RequiredProduct(models.Model):
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    ProductName = models.CharField(max_length=100)
    catagory = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='required/catagories/%Y/%m/%d',
                              blank=True)


class OrderUpdate(models.Model):
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


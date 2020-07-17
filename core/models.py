from django.conf import settings
from django.db import models
from django.shortcuts import reverse
import random
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
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
    image = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

#     def get_absolute_url(self):
# # <<<<<<< HEAD
#         return reverse('core:order_summary',
#                        )
    def get_absolute_url(self):
        return reverse('core:product_list_by_category', kwargs={"category_slug": self.slug})


COLOR_CHOICES = (
    ('B', 'Black'),
    ('W', 'White'),
    ('R', 'Red')
)
SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    image = models.ImageField()
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    discount_price = models.FloatField(null=True, blank=True)
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def get_absolute_url(self):
        return reverse("core:product_detail", kwargs={"slug": self.slug}
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
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.quantity} of {self.item.title}"
    def __str__(self):
        return f"{self.quantity} of {self.item.title} with {self.color} color and size {self.size}"

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
    Product = models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    half_paid = models.BooleanField(default=False)
    paid_amount = models.PositiveIntegerField(default=0)
    billing_address = models.ForeignKey('Billing_Address', on_delete=models.SET_NULL,
                                        blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} with the email {self.email}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_remaining_amount(self):
        remaining = 0
        total = self.get_total()
        paid = 10
        remaining = total - self.paid_amount
        return remaining

    def get_title(self):
        return self.Product.title


class Billing_Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    region = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class RequiredProduct(models.Model):
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    ProductName = models.CharField(max_length=100)
    catagory = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='required/%Y/%m/%d')

    def __str__(self):
        return self.ProductName


class OrderUpdate(models.Model):
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class Choices(models.Model):
    color = models.CharField(choices=COLOR_CHOICES, max_length=20)
    size = models.CharField(choices=SIZE_CHOICES, max_length=20)


class Instructions(models.Model):
    text = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.text[0:8]

    def get_absolute_url(self):
        return reverse('core:user_invoice', order_id = order_id)
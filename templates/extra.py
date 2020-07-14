from core.models import Order, Item, Choices
from core.models import RequiredProduct
from django.forms import ModelForm
from allauth.account.forms import LoginForm
from django import forms
import random
from django.shortcuts import reverse
from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, RequiredProduct, Category, Billing_Address, Profile, OrderUpdate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from core.forms import CheckoutForm
from allauth.account.forms import LoginForm, SignupForm
from core.forms import RequiredProductForm, CheckoutForm, SearchForm, ChoicesForm
from django.contrib.auth import authenticate

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
# Search Implementation
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from allauth.account.forms import ChangePasswordForm


# def form_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data['password'])
#             pass  # does nothing, just trigger the validation
#     else:
#         form = LoginForm()
#     return render(request, 'form.html', {'form': form})


# class HomeView(ListView):
#     model = Item
#     context_object_name = 'home_list'
#     template_name = 'home-page.html'

# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'home-page.html', context)
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Item.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Item.objects.filter(catagory=category)
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'home-page.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'page_obj': page_obj})

# @login_required
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'product-page.html', context)


@login_required
def item_detail(request, slug):
    form = ChoicesForm()
    item = get_object_or_404(Item, slug=slug)
    print(item)
    if request.method == 'POST':
        form = ChoicesForm(request.POST)
        if form.is_valid():
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user,
                                         ordered_date=ordered_date, email=request.user.email)
            color = form.cleaned_data['color']
            size = form.cleaned_data['size']
            print(color)
            item = get_object_or_404(Item, slug=slug, color=color, size=size)
            order_item, created = OrderItem.objects.create(item=item,
                                                           item__slug=item.slug,
                                                           user=request.user,
                                                           ordered=False)
            messages.info(request, "This item was added to your cart.")
            return redirect('core:order_summary')
            # order_qs = Order.objects.filter(
            #     user=request.user, ordered=False, email=request.user.email)
            # if order_qs.exists():
            #     order = order_qs[0]
            #     if order.items.filter(item__slug=item.slug).exists():
            #         order_item.quantity += 1
            #         order_item.save()
            #         messages.info(request, "This item quantity was Updated.")
            # return redirect('core:order_summary')
        # else:
        #     ordered_date = timezone.now()
        #     order = Order.objects.create(user=request.user,
        #                                 ordered_date=ordered_date, email=request.user.email)
        #     order_item = OrderItem.objects.create(item=item,
        #                                         user=request.user, ordered=False, color=color, size=size)
        #     order.items.add(order_item)
        #     # order.items.add(order_item)
        #     messages.info(request, "This item was added to your cart.")
        #     return redirect('core:product_detail', slug=slug)
        # else:
        #     return render(request, 'order_summary.html')
            # color = form.cleaned_data['color']
            # size = form.cleaned_data['size']
            # print(color)
            # order_item.color = color
            # order_item.size = size
            # order_item.save()
            # return render(request, 'product-page.html', {
            #     'form': form
            # })
        else:
            form = ChoicesForm()
        return render(request, 'product-page.html', {
            'form': form,
            'item': item
        })
    return redirect('core:product_list')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False
                                                          )
    order_qs = Order.objects.filter(
        user=request.user, ordered=False, email=request.user.email)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was Updated.")
            return redirect('core:order_summary')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('core:product_detail', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date, email=request.user.email)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('core:order_summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('core:order_summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, "You do not have any order now.")
        return redirect('core:product', slug=slug)
    return redirect('core:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was Updated.")
            return redirect('core:order_summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('core:product_list_by_category', slug=slug)
    else:
        messages.info(request, "You do not have any order now.")
        return redirect('core:product_detail', slug=slug)
    return redirect('core:product_detail', slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.all()

            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You donot have an active order')
            return redirect('/')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                user = self.request.user
                print(user)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                postal_code = form.cleaned_data['postal_code']
                city = form.cleaned_data['city']
                billing_address = Billing_Address(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address,
                    postal_code=postal_code,
                    city=city
                )
                billing_address.save()
                order.billing_address = billing_address

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.save()
                messages.info(self.request, 'Your order was successful')
                return redirect('core:user_invoice')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You donot have an active order')
            return redirect('core:order_summary')

        return redirect('core:checkout')


def user_order_pdf(request):
    user = request.user
    try:
        order = Order.objects.filter(ordered=True, paid=False, user=user)[0]
        # I wanna make it search by the order
        # order1 = Order.objects.filter(ordered = True, paid = True,user = user)[0]
        # order2 = Order.objects.filter(ordered = True, paid = False,user = user)[0]

        print(order)
        # first_name = order.billing_address.first_name
        # last_name = order.billing_address.last_name
        # email = order.billing_address.email
        # address = order.billing_address.address
        # city = order.billing_address.city
        # order_id = order.order_id
        html = render_to_string('pdf.html',
                                {'order': order,
                                 })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(
            order.id)
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(
                                                   settings.STATIC_ROOT + 'css/pdf.css')])

        return response
    except ObjectDoesNotExist:
        messages.warning(request, 'You do not have an order.')
        return redirect('core:product_list')


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, ordered=True)
    user = request.user
    email = request.user.email
    html = render_to_string('pdf.html',
                            {'order': order,
                             })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(
        order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])

    return response


def required_product(request):
    if request.method == 'POST':
        form = RequiredProductForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # print(username)
            print(request.user)
            print(email)
            print(username)
            if email == request.user.email:
                pass
            else:
                messages.warning(
                    request, 'Your credentials do not match, Please try again!')
                form = RequiredProductForm()
                return render(request, 'required-product-form.html',
                              {'form': form})

            email = request.user.email

            form.save()
            return render(request, 'required-product-form.html',
                          {'form': form,
                           'email': email})
    else:
        form = RequiredProductForm()
    return render(request, 'required-product-form.html',
                  {'form': form})


@login_required
def Tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        print(orderId)
        email = request.POST.get('email', '')
        print(email)
        order = Order.objects.filter(
            order_id=orderId, user=request.user, email=email)
        print(order)
        if len(order) > 0:
            update = OrderUpdate.objects.filter(order_id=orderId)

            updates = []
            for i in update:
                updates.append(i.update_desc)
            # order = Order.objects.filter(user = request.user,email = email)
            # order = order[0]

            # print(order.get_total())

            return render(request, 'tracker.html', {
                'update': updates
            })
        else:
            return HttpResponse('{}')
        # except Exception as e:
        #     return HttpResponse('{}')

    return render(request, 'tracker.html')

#     queryset = Item.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super(HomeView, self).get_context_data(**kwargs)
#         # context['items'] = Item.objects.all()
#         context['categories'] = Category.objects.all()
#         # And so on for more models
#         return context

# template_name = 'home-page.html'

# all_models_dict = {
#     "items": Item.objects.all(),
#     "categories":Category.objects.all()
# "extra_context" : {"role_list" : Role.objects.all(),
#                    "venue_list": Venue.objects.all(),
#                    #and so on for all the desired models...
#                    }
# }
# def get_context_data(self. **kwargs):
#     context = super(HomeView, self).get_context_data(**kwargs)
#     Items_context['items'] = Item.objects.all()
#     categories_context['categories'] = Category.objects.all()
# return context


# def invoice(request):
#     user = request.user
#     order = get_object_or_404(Order,ordered = True, paid = False,user = user)


class UserProfile(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = 'profile.html'


def item_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'description')
            search_query = SearchQuery(query)
            results = Item.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request, 'search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def user_profile(request):
    user = request.user
    form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        form.save()
        messages.info(request, 'Your password has been changed')
        return redirect('core:profile')
    else:
        form = ChangePasswordForm()
        return render(request, 'profile.html', {
            'user': request.user,
            'form': form
        })


def order_history(request):
    user = request.user
    Orders = Order.objects.all().filter(user=request.user)
    OrderItems = OrderItem.objects.all().filter(user=user)
    return render(request, 'order_history.html', {
        'orders': Orders,
        'order_items': OrderItems
    })

# def product_page(request,slug):
#     form = ChoicesForm()
#     item = get_object_or_404(Item, slug=slug)
#     order_item, created = OrderItem.objects.get_or_create(item=item,
#                                                           user=request.user,
#                                                           ordered=False
#                                                           )
#     order_qs = Order.objects.filter(
#         user=request.user, ordered=False, email=request.user.email)
#     if request.method == 'POST':
#         form = ChoicesForm(request.POST
#         color = form.cleaned_data['color']
#         size = form.cleaned_data['size']
#         order_item = OrderItem.objects.g


# Models

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
    color = models.CharField(choices=COLOR_CHOICES, max_length=10, blank=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=10, null=True)
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
        return f"{self.quantity} of {self.item.title} with {self.item.color} color"

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


class Choices(models.Model):
    color = models.CharField(choices=COLOR_CHOICES, max_length=20)
    size = models.CharField(choices=SIZE_CHOICES, max_length=20)


class RequiredProductForm(forms.ModelForm):

    class Meta:
        model = RequiredProduct
        fields = '__all__'


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "firstName",
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "lastName",
            'class': 'form-control'
        }
    ))
    # username = forms.CharField(widget=)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'id': "email",
            'class': 'form-control',
            'placeholder': 'user@exapmle.com'
        }
    ))
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "address",
            'class': 'form-control',
            'placeholder': '1234 Main Street 1'
        }
    ))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1111',
        'class': 'form-control',
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'id': "address",
        'class': 'form-control',
        'placeholder': 'Your City'
    }))


class ChoicesForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['color', 'size']

# class CheckoutForm(forms.ModelForm):

#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'email', 'address',
#                   'postal_code', 'city', 'zip_code']


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control mr-sm-2",
            'placeholder': "Search",
            'aria-label': "Search"
        }
    ))


class ChoicesForm(forms.ModelForm):

    class Meta:
        model = Choices
        fields = '__all__'

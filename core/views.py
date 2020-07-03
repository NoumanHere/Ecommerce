from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, RequiredProduct, Category
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from core.forms import CheckoutForm
from allauth.account.forms import LoginForm, SignupForm
from core.forms import RequiredProductForm
from django.contrib.auth import authenticate
# def form_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data['password'])
#             pass  # does nothing, just trigger the validation
#     else:
#         form = LoginForm()
#     return render(request, 'form.html', {'form': form})


class HomeView(ListView):

    context_object_name = 'home_list'    
    template_name = 'home-page.html'
    queryset = Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        # And so on for more models
        return context

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

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warnning(request, 'You donot have an active order')
            return redirect('/')


# def home(request):
#     context = {
#         'items':Item.objects.all()
#     }
#     return render(request,'home-page.html',context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


@login_required
def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product-page.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Item.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Item.objects.filter(catagory=category)
    return render(request,
                  'home-page.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False
                                                          )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
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
            return redirect('core:product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('core:product', slug=slug)


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
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, "You do not have any order now.")
        return redirect('core:product', slug=slug)
    return redirect('core:product', slug=slug)


@login_required
def checkout(request):
    return render(request, 'checkout-page.html')


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
                messages.warning(request, 'Your credentials do not match!')
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

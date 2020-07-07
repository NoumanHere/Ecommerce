from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, RequiredProduct, Category, Billing_Address, Profile, OrderUpdate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from core.forms import CheckoutForm
from allauth.account.forms import LoginForm, SignupForm
from core.forms import RequiredProductForm, CheckoutForm
from django.contrib.auth import authenticate

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import json
from django.utils.safestring import mark_safe


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
    model = Item
    context_object_name = 'home_list'
    template_name = 'home-page.html'
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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You donot have an active order')
            return redirect('/')


def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home-page.html', context)


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
            return redirect('core:product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date, email=request.user.email)
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
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                postal_code = form.cleaned_data['postal_code']
                city = form.cleaned_data['city']
                zip_code = form.cleaned_data['zip_code']
                billing_address = Billing_Address(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address,
                    postal_code=postal_code,
                    zip_code=zip_code,
                    city=city
                )
                billing_address.save()
                order.billing_address = billing_address
                
                order_items = order.items.all()
                order_items.update(ordered = True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.save()
                messages.info(self.request, 'Your order was successful')
                return redirect('core:user_invoice')
                # html = render_to_string(
                #     'pdf.html', {
                #         'order': order,
                #     }
                # )
                # messages.info(self.request, 'Your order was successful')
                # response = HttpResponse(content_type='application/pdf')
                # response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(
                #     order.id)
                # weasyprint.HTML(string=html).write_pdf(response,
                #                                        stylesheets=[weasyprint.CSS(
                #                                            settings.STATIC_ROOT + 'css/pdf.css')])
                # return response
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You donot have an active order')
            return redirect('core:order_summary')

        return redirect('core:checkout')

# def invoice(request):
#     user = request.user
#     order = get_object_or_404(Order,ordered = True, paid = False,user = user)

def user_order_pdf(request):
    user = request.user
    try:
        order = Order.objects.filter(ordered = True, paid = False,user = user)[0]
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




class UserProfile(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = 'profile.html'


@login_required
def Tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        print(orderId)
        email = request.POST.get('email', '')
        print(email)
        order = Order.objects.filter(order_id=orderId, user=request.user,email = email)
        print(order)
        if len(order) > 0:
            update = OrderUpdate.objects.filter(order_id=orderId)

            updates = []
            for i in update:
                updates.append(i.update_desc)
            # order = Order.objects.filter(user = request.user,email = email)
            # order = order[0]
            
            # print(order.get_total())
            
            return render(request,'tracker.html',{
                'update':updates
                })
        else:
            return HttpResponse('{}')
        # except Exception as e:
        #     return HttpResponse('{}')

    return render(request, 'tracker.html')

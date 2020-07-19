from allauth.account.forms import ChangePasswordForm
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import weasyprint
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from core.forms import RequiredProductForm, CheckoutForm, SearchForm, OrderItemForm
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, RequiredProduct, Category, Billing_Address, Profile, OrderUpdate, Instructions


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Item.objects.all().order_by('-price')
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


def item_detail(request, slug):
    form = OrderItemForm()
    item = get_object_or_404(Item, slug=slug)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            ordered_date = timezone.now()
            user = request.user
            quantity = form.cleaned_data['quantity']
            print(quantity)
            # image = form.cleaned_data['image']
            # print(image)
            details = form.cleaned_data['details']
            ordered_date = timezone.now()
            order_qs = Order.objects.all().filter(
                user=user, email=request.user.email, ordered=False)
            print(order_qs)
            if order_qs.exists():
                order = order_qs[0]
                print(order)
                if order.items.filter(item__slug=item.slug, details=details, user=request.user).exists():
                    order_item = OrderItem.objects.get(
                        user=user,
                        item=item,
                        details=details,
                    )
                    quantity = form.cleaned_data['quantity']
                    print(quantity)
                    order_item.quantity += quantity
                    order_item.save()
                    messages.info(request, "This item quantity was Updated.")
                    return redirect('core:order_summary')
                else:
                    order_item = OrderItem.objects.create(
                        user=user,
                        item=item,
                        details=form.cleaned_data['details'],
                        quantity=form.cleaned_data['quantity']
                    )
                    order_item.save()
                    order.items.add(order_item)
                    print("this one")
                    messages.info(request, "This item was added to your cart.")
                    return redirect('core:product_detail', slug=slug)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user,
                                             ordered_date=ordered_date, email=request.user.email, Product=item)
                order_item = OrderItem.objects.create(
                    user=user,
                    item=item,
                    details=form.cleaned_data['details'],
                    quantity=form.cleaned_data['quantity']
                )
                order.items.add(order_item)
                print("this two")
                messages.info(request, "This item was added to your cart.")
                return redirect('core:order_summary')
        else:
            form = OrderItemForm()
            return render(request, 'test-page.html', {
                'form': form,
                'item': item
            })
    return render(request, 'test-page.html', {
        'form': form,
        'item': item
    })


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
            print("This delete??/")
            messages.info(request, "This item was removed from your cart.")
            return redirect('core:order_summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('core:order_summary')
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
            return redirect('core:product_list_by_category', slug=catagory_slug)
    else:
        messages.info(request, "You do not have any order now.")
        return redirect('core:product_detail', slug=slug)
    return redirect('core:product_detail', slug=slug)


@login_required
def order_summary(request):
    # Orders_items = Order.objects.all().filter(user=request.user, ordered=False)
    Orders_items = OrderItem.objects.filter(
        user=request.user, ordered=False)
    try:
        Orders = Order.objects.filter(user=request.user, ordered=False)[0]
    except:
        Orders = Order.objects.filter(user=request.user, ordered=False)
    # print(Orders[0])
    # print(str(Orders[1]) + str(Orders[0]))
    context = {
        'object': Orders_items,
        'object2': Orders}
    return render(request, 'order_summary.html', context)


class CheckoutView(LoginRequiredMixin, View):
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
                full_name = form.cleaned_data['full_name']
                email = self.request.user.email
                phone_number = form.cleaned_data['phone_number']
                region = form.cleaned_data['region']
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                billing_address = Billing_Address(
                    user=user,
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    region=region,
                    address=address,
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
                messages.info(self.request, 'Your order was successful.')
                return redirect('core:Instructions')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You donot have an active order')
            return redirect('core:order_summary')

        return redirect('core:checkout')


def user_order_pdf(request, order_id):
    user = request.user
    try:
        # order_id = Order.objects.get(order_id).filter(user=user)
        order = Order.objects.filter(
            ordered=True, order_id=order_id, user=user)[0]

        print(order)
        html = render_to_string('pdf.html',
                                {'order': order,
                                 'order_id': order_id,
                                 })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(
            order.order_id)
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(
                                                   settings.STATIC_ROOT + 'css/pdf.css')])

        return response
    except ObjectDoesNotExist:
        messages.warning(request, 'You do not have an order.')
        return redirect('core:product_list')


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, ordered=True)
    user = request.user
    email = request.user.email
    html = render_to_string('pdf.html',
                            {'order': order,
                             })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(
        order.order_id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])

    return response


def required_product(request):
    if request.method == 'POST':
        form = RequiredProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            # print(username)
            email = request.user.email
            form.save()
            messages.info(
                request, "Your request have been submitted. Thanks:)")
            return redirect('core:product_list')
    else:
        form = RequiredProductForm()
    return render(request, 'required-product-form.html',
                  {'form': form})


@login_required
def Tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        print(orderId)
        order = Order.objects.filter(
            order_id=orderId, user=request.user)
        print(order)
        if len(order) > 0:
            update = OrderUpdate.objects.filter(order_id=orderId)
            updates = []
            if update:
                for i in update:
                    updates.append(i.update_desc)
                return render(request, 'tracker.html', {
                    'update': updates[0]
                })
            else:
                updates.append('No')
                return render(request, 'tracker.html', {
                    'update': updates[0]
                })
        else:
            return render(request, 'tracker.html', {
                'Info': "Your Credentials do not match. Please try again."
            })

    return render(request, 'tracker.html')


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
    Orders = Order.objects.all().filter(user=request.user).order_by('-ordered_date')
    return render(request, 'order_history.html', {
        'orders': Orders,
    })


def Ins(request):
    model = Instructions.objects.all()
    return render(request, 'Instructions.html', {
        'ins': model
    })


def testview(request):
    items = Item.objects.all()
    return render(request, 'test.html', {
        'item': items
    })

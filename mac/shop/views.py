from math import *
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from PayTm import Checksum
from .models import product, Contact, Orders, OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt


MERCHANT_KEY = "bKMfNxPPf_QdZppa"
# Create your views here.

def index(request):
    # products = product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # nSlides = ceil(n / 4)
    # params = {'no_of_slides':nSlides, 'range':range(1,nSlides),'product':products}
    # allProds=[[products, range(1, nSlides), nSlides],
    #           [products, range(1, nSlides), nSlides]]

    allprods = []
    catprods = product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod, range(1, nSlides),nSlides])
    params={'allprods':allprods }
    return render(request, 'shop/index.html',params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')



def productView(request,myid):
    products = product.objects.filter(id=myid)
    # print(products)
    return render(request, 'shop/productView.html',{"products":products[0]})






def checkout(request):
    if request.method == "POST":

        items_json = request.POST.get('itemsJson', '')

        amount = request.POST.get('amount')
        if amount is None or amount.strip() == "":
            amount = 0
        else:
            amount = int(amount)

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Save order
        order = Orders(
            items_json=items_json,
            amount=amount,
            name=name,
            email=email,
            address=address,
            country=country,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        # Show dummy payment page
        return render(request, "shop/dummy_payment.html", {"order_id": order.order_id, "amount": amount})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def paymentstatus(request):
    order_id = request.POST.get('order_id')
    return render(request, "shop/paymentstatus.html", {"order_id": order_id})


# def contact(request):
    thank=False
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        print(name, email, phone, desc)
        Contacts = Contact(name=name, email=email, phone=phone, desc=desc)
        Contacts.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})


def contact(request):
    thank=False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone =  form.cleaned_data['phone']
            desc = form.cleaned_data['desc']

            Contact.objects.create(name=name, email=email, phone=phone, desc=desc)
            thank = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request,"shop/contact.html", {"form":form, "thank":thank})




# use for paytm 

# def checkout(request):
#     if request.method == "POST":
#         items_json = request.POST.get('itemsJson', '')
#         amount = request.POST.get('amount', '')
#         amount = request.POST.get('amount')
#         if amount is None or amount.strip() == "":
#             amount = 0
#         else:
#             amount = int(amount)

#         name = request.POST.get('name','')
#         email = request.POST.get('email','')
#         address = request.POST.get('address1','') + " " + request.POST.get('address2','')
#         city = request.POST.get('city','')
#         state = request.POST.get('state','')
#         zip_code = request.POST.get('zip_code','')
#         phone = request.POST.get('phone','')

#         print(name, email, address, city, state, zip_code, phone)
#         order = Orders(items_json=items_json, amount=amount, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
#         order.save()

#         update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
#         update.save()
#         thank = True
#         id = order.order_id
#         # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
#         # Request paytm to transfer the amount to your account after payment by user
#         param_dict = {

#                 'MID': 'pvrgwZZ79933399236965',
#                 'ORDER_ID': str(order.order_id),
#                 'TXN_AMOUNT': str(amount),
#                 'CUST_ID': email,
#                 'INDUSTRY_TYPE_ID': 'Retail',
#                 'WEBSITE': 'WEBSTAGING',
#                 'CHANNEL_ID': 'WEB',
#                 'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY) # pyright: ignore[reportUndefinedVariable]
#         return render(request, 'shop/paytm.html', {'param_dict': param_dict})
#     return render(request, 'shop/checkout.html')


# @csrf_exempt
# def handlerequest(request):
    # paytm will send you post request here
    # form = request.POST
    # response_dict = {}
    # for i in form.keys():
    #     response_dict[i] = form[i]
    #     if i == 'CHECKSUMHASH':
    #         checksum = form[i]

    # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum) # pyright: ignore[reportUndefinedVariable]
    # if verify:
    #     if response_dict['RESPCODE'] == '01':
    #         print('order successful')
    #     else:
    #         print('order was not successful because' + response_dict['RESPMSG'])
    # return render(request, 'shop/paymentstatus.html', {'response': response_dict})
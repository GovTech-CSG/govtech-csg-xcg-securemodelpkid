from django.http import HttpResponse

from .models import Customer, CustomerWithRandomID

# Create your views here.


def test(request):
    html = "<html><body>It is now %s.</body></html>"
    customer1 = Customer.objects.create(name="John")
    print("Custome1 ID:", customer1.id)  # '725393588906066'
    msg = f"Custome1 ID: {customer1.id}"
    customer1.delete()

    msg = msg + "<br>"

    customer2 = CustomerWithRandomID.objects.create(name="Jane")
    print("Custome2 ID:", customer2.id)  # '725393588906066'
    msg = msg + f"Custome2 ID: {customer2.id}"
    customer2.delete()

    html = "<html><body><h1>Random ID test</h1>" + msg + "</body></html>"

    return HttpResponse(html)

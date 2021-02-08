from .models import *

def cart_total(request):
    if request.user.is_authenticated:
        totalcarts = Cart.objects.filter(user=request.user, purchase=False)
        return dict(totalcarts=totalcarts)
    else:
        totalcarts=[]
        return totalcarts  

def menu_links(request):
    links = Category.objects.filter(parent=None).filter(active=True)
    return dict(links=links)
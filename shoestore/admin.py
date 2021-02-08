from django.contrib import admin
from .models import *
# Register your models here.


class sizesAdmin(admin.TabularInline):
    model = sizes

class colorAdmin(admin.StackedInline):
    model = color

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [sizesAdmin, colorAdmin]
 
    class Meta:
       model = Product

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(slider)
admin.site.register(promocode)
admin.site.register(Order)
admin.site.register(Customer)
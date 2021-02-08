from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import Sum
from shoes import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='media/profile_pic',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Country = models.CharField(max_length=20,null=False, blank=True)
    Company = models.CharField(max_length=20,null=False, blank=True)
    City =  models.CharField(max_length=20,null=False, blank=True)
    State =  models.CharField(max_length=20,null=False, blank=True)
    Zip_Code =  models.IntegerField(blank=True, default="1")
    Telephone =  models.IntegerField(blank=True, default="1")
    Extension =  models.CharField(max_length=20,null=False, blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/category') 
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    hit = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=False, verbose_name='Status')

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()    

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    


class Product(models.Model):
    title = models.CharField(max_length=70)
    meta_tags = models.CharField(max_length=2000, blank=True)
    meta_desc = models.TextField(max_length=2000, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    image = models.ImageField(upload_to='media/product')
    image_alt_name = models.CharField(max_length=200, blank=True)
    desc = RichTextField(blank=True, null=True)
    author = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    hit = models.PositiveIntegerField(default=0) #This field is for popular posts
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title    
        
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.review.values() )

        return total / self.reviews.count()

class sizes(models.Model):
    SIZES = (
        ('7', "7"),
        ('7.5', "7.5"),
        ('8', "8"),
        ('8.5', "8.5"),
        ('9', "9"),
        ('9.5', "9.5"),
        ('10', "10"),
        ('10.5', "10.5"),
        ('11', "11"),
        ('12', "12"),
    )
    shoes = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZES, max_length=50)

    def __str__(self):
        return self.size
    

class color(models.Model):
    shoes = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ManyToManyField(sizes)
    color = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='media/colorproduct', blank=True)
    image2 = models.ImageField(upload_to='media/colorproduct', blank=True)
    image3 = models.ImageField(upload_to='media/colorproduct', blank=True)
    image4 = models.ImageField(upload_to='media/colorproduct', blank=True)
    image5 = models.ImageField(upload_to='media/colorproduct', blank=True)

    def __str__(self):
        return self.color
    
class slider(models.Model):
    head1 = models.CharField(max_length=100, blank=True, verbose_name='h6')
    head2 = models.CharField(max_length=100, blank=True, verbose_name='h1')
    head3 = models.CharField(max_length=100, blank=True, verbose_name='h5')
    image = models.ImageField(upload_to='media/slider')
    button = models.CharField(max_length=100, blank=True, verbose_name='Button Name')
    link = models.URLField(max_length=500, blank=True, verbose_name='Link')
    active = models.BooleanField(default=False)
    font_color = models.CharField(max_length=100, blank=True, verbose_name='Font Color')

    def __str__(self):
        return self.head1

class promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.FloatField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)
    # color = models.ForeignKey(color, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total    

class Order(models.Model):
    method = (
        ('EMI', "EMI"),
        ('ONLINE', "Online"),
    )
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null = False, default='0')
    coupon = models.ForeignKey(promocode, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='INR ORDER TOTAL')
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True)
    order_id =  models.CharField(max_length=100, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        if self.coupon:    
            total -= self.coupon.amount    
        return total

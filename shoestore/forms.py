from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from .models import *
from django.forms import inlineformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['hit', 'author']

class sliderForm(forms.ModelForm):
    class Meta:
        model = slider
        fields = '__all__'

class EditPostForm(forms.ModelForm): 
    class Meta:
        model = Product
        fields = '__all__'

class CatForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['hit']

class EditCatForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'

# User Creation Forms
class CustomerAuthForm(AuthenticationForm):
    username = forms.EmailField(required=True , label="Email")

class CustomerCreationForm(UserCreationForm):
    
    username = forms.EmailField(required=True , label="Email" )
    first_name = forms.CharField(required=True , label="First Name")
    last_name = forms.CharField(required=True , label="Last Name")
    class Meta:
        model = User
        fields = ['username' ,'first_name' , "last_name" ]

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name')
        if len(value.strip()) < 4 :
            raise ValidationError("First Name must be 4 char long...")
        return value.strip()
    
    def clean_last_name(self):
        value = self.cleaned_data.get('last_name')
        if len(value.strip()) < 4 :
            raise ValidationError("Last Name must be 4 char long...")
        return value.strip()

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['address','mobile','profile_pic']

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['address','mobile','profile_pic','Country','Company','City','State','Zip_Code','Telephone','Extension']

class CustomerCreationEditForm(UserChangeForm):
    # password = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden'}))
    username = forms.EmailField(required=True , label="Email" )
    first_name = forms.CharField(required=True , label="First Name")
    last_name = forms.CharField(required=True , label="Last Name")
    class Meta:
        model = User
        fields = ['username' ,'first_name' , "last_name"]
        exclude = ['password']

class changepassword(UserCreationForm):    
    class Meta:
        model = User
        fields = ['password1']
        exclude = ['username', 'first_name','last_name']

class Customerloginform(AuthenticationForm):
    username = forms.EmailField(required=True, label="Email") #Isme emailfield isliye liye hai qki humne isme username use ni kiya isme, username ki jagah humne isme email use ki hai to that's why we use this!!
    password = forms.PasswordInput()

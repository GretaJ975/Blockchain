from django import forms
from django.views.generic import DetailView
from django.forms import DateTimeInput, EmailField, ModelForm

from .models import BlockchainEntry, Order, Block, CreateMine, User, Profile


class BlockchainEntryForm(forms.ModelForm):
    class Meta:
        model = BlockchainEntry
        fields = ['name', 'description']  # Include fields you want in the form

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter a detailed description...'}),
        }


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['timestamp', 'previous_hash', 'hash', 'data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_address', 'total_amount', 'payment_method']


    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount <= 0:
            raise forms.ValidationError("The total amount must be greater than zero.")
        return total_amount

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'  # Ensure this template exists
    context_object_name = 'order'

class Blockchain:
    @staticmethod
    def add_new_block(data):
        new_block = Block(data=data)
        new_block.save()

class CreateMineForm(forms.ModelForm):
    class Meta:
        model = CreateMine
        fields = ['data']
        widgets = {
            'data': forms.Textarea(attrs={'placeholder': 'Enter block data...', 'rows': 4, 'cols': 50}),
        }

class UserUpdateForm(forms.ModelForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]

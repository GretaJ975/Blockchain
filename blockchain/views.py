import hashlib
import profile
import time
import requests

from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .models import Block, Order, CreateMine
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import BlockchainEntryForm, OrderForm, BlockForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.core.cache import cache

def index(request):
    return render(request, 'blockchain/index.html')



@csrf_exempt
def create_block(request):
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, 'blockchain/create_block.html', {'form': form})
    else:
        form = BlockForm()
        return render(request, 'blockchain/create_block.html', {'form': form})


def view_chain(request):
    chain = Block.objects.all().order_by('timestamp')  # Fetch all blocks ordered by time
    return render(request, 'blockchain/view_chain.html', {'chain': chain})

@api_view(['GET'])
def get_blockchain(request):
    blocks = Block.objects.all().values()
    return Response({"status": "success", "blockchain": list(blocks)})


@csrf_exempt
def home(request):
    if request.method == "POST":
        data = request.POST.get('data', 'Default Block Data')
        new_block = Block(data=data)
        new_block.save()

    blockchain = Block.objects.all().order_by('id')
    return render(request, 'blockchain/home.html', {'blockchain': blockchain, 'btc_price': get_btc_price()})


def block_detail(request, block_id):
    block = get_object_or_404(Block, id=block_id)
    return render(request, 'blockchain/block_detail.html', {'block_': block})


def about(request):
    return render(request, 'blockchain/about.html')


def create_blockchain_entry(request):
    if request.method == 'POST':
        form = BlockchainEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlockchainEntryForm()

    return render(request, 'blockchain/create_blockchain_entry.html', {'form': form})

def create_mine(request):
    if request.method == "POST":
        last_block = Block.objects.last()
        previous_hash = last_block.hash if last_block else "0"  # Genesis block case
        nonce = 0
        new_hash = ""

        while not new_hash.startswith("0000"):
            nonce += 1
            new_hash = hashlib.sha256(f"{previous_hash}{nonce}".encode()).hexdigest()
        print ("LAST_BLOCK", last_block)

        block = CreateMine(
            block= last_block,
            data=f"Mined block at {time.ctime()}",
            previous_hash=previous_hash,
            # nonce=nonce,
            hash=new_hash,
        )
        block.save()
        return render(request, 'blockchain/create_mine.html', {'last_block': last_block})



def mine (request):
    mines = CreateMine.objects.all()
    return render(request, 'blockchain/mine.html', context = {'mines': mines})

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

def order_list(request):
    orders = Order.objects.all().order_by('-timestamp')
    return render(request, 'blockchain/orders.html', {'orders': orders})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = OrderForm()

    return render(request, 'blockchain/create_order.html', {'form': form})


def block_list(request):
    blocks = Block.objects.all()
    return render(request, 'blockchain/block_list.html', {'blocks': blocks})

def generate_block_hash(block):
    block_string = f"{block.id}{block.timestamp}{block.data}{block.previous_hash}"
    return hashlib.sha256(block_string.encode()).hexdigest()


class OrderDetailView:
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'


def create_block_view(request):
    context = {"message": "Create a new block"}
    return render(request, 'blockchain/create_block.html', context)

def create_mine_view(request):
    return render(request, 'blockchain/create_mine.html')


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                message=("Profile of {username_bold} updated!").format(
                    username_bold=f"<strong>{request.user}</strong>"
                ),
            )
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, template_name="registration/profile.html", context={'profile':profile})

def show_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    return render (request, template_name="registration/profile.html", context= {'user':user , 'profile':profile})



def get_btc_price():
    btc_price = cache.get('btc_price')

    if not btc_price:
        url = "https://api.coinlore.com/api/tickers/?id=90"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            btc_price = data['data'][0]['price_usd']

            cache.set('btc_price', btc_price, timeout=300)
        else:
            btc_price = None

    return btc_price


def calculate_hash():
    return None
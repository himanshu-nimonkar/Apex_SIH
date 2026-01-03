from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required

from .models import GraphicalPassword
import hashlib
import secrets


# Create your views here.

def hash_image_sequence(sequence, salt):
    """
    Hash the image sequence with salt for secure storage.
    """
    combined = sequence + salt
    return hashlib.sha256(combined.encode()).hexdigest()


def index(request):
    return render(request, 'accounts/register.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        graphical_password = request.POST.get('graphical_password', '')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid EMAIL')
            return redirect('register')

        # Validate graphical password
        if not graphical_password:
            messages.error(request, 'Please select your graphical password (4-6 images)')
            return redirect('register')
        
        images = graphical_password.split(',')
        if len(images) < 4 or len(images) > 6:
            messages.error(request, 'Please select between 4 to 6 images for your graphical password')
            return redirect('register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # Check if email exists
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Create graphical password
            salt = secrets.token_hex(16)
            hashed_sequence = hash_image_sequence(graphical_password, salt)
            
            GraphicalPassword.objects.create(
                user=user,
                image_sequence_hash=hashed_sequence,
                salt=salt
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

    # List of images for the graphical password
    images = ['anonymity.png', 'bitcoin.png', 'blackcoin.png',
              'block_chain.png', 'centralized.png', 'conversion.png',
              'currency_cap.png', 'decentralized.png', 'decryption.png',
              'digital_key.png', 'disclosed_identity.png', 'distributed.png',
              'dogecoin.png', 'emercoin.png', 'encryption.png', 'ethereum.png',
              'feathercoin.png', 'free.png', 'ledger.png', 'litecoin.png',
              'lost_key.png', 'mastercoin.png', 'miner.png', 'miner2.png',
              'mining.png', 'mining2.png', 'mining_center.png',
              'mining_pool.png', 'mining_pool2.png', 'monero.png', 'myriad.png', 
              'namecoin.png', 'no_double_spending.png', 'nxt.png', 'p2p.png', 
              'peercoin.png', 'ponzi_scheme.png', 'primecoin.png', 'pseudonimity.png',
              'pyramid_scheme.png', 'receive.png', 'ripple.png', 'send.png',
              'siacoin.png', 'stellar_lumen.png', 'transaction.png',
              'tumbler.png', 'wallet.png', 'zcash.png', 'zcoin.png']
    
    context = {'images': images}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        graphical_password = request.POST.get('graphical_password', '')

        # Validate graphical password is provided
        if not graphical_password:
            messages.error(request, 'Please select your graphical password')
            return redirect('login')

        # Authenticate with text password
        user = authenticate(username=username, password=password)

        if user is not None:
            # Verify graphical password
            try:
                gp = GraphicalPassword.objects.get(user=user)
                hashed_input = hash_image_sequence(graphical_password, gp.salt)
                
                if hashed_input == gp.image_sequence_hash:
                    auth.login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid graphical password')
                    return redirect('login')
                    
            except GraphicalPassword.DoesNotExist:
                messages.error(request, 'Graphical password not set for this user')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    # Same images list for login
    images = ['anonymity.png', 'bitcoin.png', 'blackcoin.png',
              'block_chain.png', 'centralized.png', 'conversion.png',
              'currency_cap.png', 'decentralized.png', 'decryption.png',
              'digital_key.png', 'disclosed_identity.png', 'distributed.png',
              'dogecoin.png', 'emercoin.png', 'encryption.png', 'ethereum.png',
              'feathercoin.png', 'free.png', 'ledger.png', 'litecoin.png',
              'lost_key.png', 'mastercoin.png', 'miner.png', 'miner2.png',
              'mining.png', 'mining2.png', 'mining_center.png',
              'mining_pool.png', 'mining_pool2.png', 'monero.png', 'myriad.png', 
              'namecoin.png', 'no_double_spending.png', 'nxt.png', 'p2p.png', 
              'peercoin.png', 'ponzi_scheme.png', 'primecoin.png', 'pseudonimity.png',
              'pyramid_scheme.png', 'receive.png', 'ripple.png', 'send.png',
              'siacoin.png', 'stellar_lumen.png', 'transaction.png',
              'tumbler.png', 'wallet.png', 'zcash.png', 'zcoin.png']
    
    context = {'images': images}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('/')


def about(request):
    return render(request, 'accounts/about.html')


def team(request):
    return render(request, 'accounts/team.html')


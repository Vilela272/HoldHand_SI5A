from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from products.models import ProductProfile
from .models import UserProfile


# Create your views here.
def register(request):
    """
    Function at register user
    """
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username is None:
            return redirect('register')
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        email2 = request.POST['email2']
        password = request.POST['password']
        password2 = request.POST['password2']
        address = request.POST['address']
        zip_code = request.POST['zip_code']
        city = request.POST['city']
        uf = request.POST['uf']
        number = request.POST['number']
        district = request.POST['district']
        complement = request.POST['complement']

        if (campo_vazio(username) or username is None):
            messages.erro(
                request, 'WARNING!!! The user field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(name) or name is None):
            messages.error(
                request, 'WARNING!!! The name field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(surname) or surname is None):
            messages.error(
                request, 'WARNING !!! The surname field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(email) or email is None):
            messages.error(
                request, 'WARNING!!! The email field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(email2) or email2 is None):
            messages.error(
                request, 'WARNING!!! The confirmation email field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(password) or password is None):
            messages.error(
                request, 'WARNING!!! The password field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(password2) or password2 is None):
            messages.error(
                request, 'WARNING!!! The confirmation password field cannot be empty'
            )
            return redirect('register')
        # Address
        if (campo_vazio(address) or address is None):
            messages.error(
                request, 'WARNING!!! The address field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(zip_code) or zip_code is None):
            messages.error(
                request, 'WARNING!!! The zip_code field cannot be empty'
            )
            return redirect('register')

        if (campo_vazio(city) or city is None):
            messages.error(
                request, 'WARNING!!! The city field cannot be empty'
            )
            return redirect('register')
        
        if (campo_vazio(uf) or uf is None):
            messages.error(
                request, 'WARNING!!! The zip_code field cannot be empty'
            )
            return redirect('register')
    
        if (campo_vazio(complement) or complement is None):
            messages.error(
                request, 'WARNING!!! The complement field cannot be empty'
            )
            return redirect('register')
        
        if (campo_vazio(district) or district is None):
            messages.error(
                request, 'WARNING!!! The district field cannot be empty'
            )
            return redirect('register')
        
        if (campo_vazio(number) or number is None):
            messages.error(
                request, 'WARNING!!! The number field cannot be empty'
            )
            return redirect('register')
        # Address

        if (senhas_nao_sao_iguais(password, password2)):
            messages.error(
                request, 'WARNING!!! The password and password confirmation fields do not match'
            )
            return redirect('register')

        if (email_nao_sao_iguais(email, email2)):
            messages.error(
                request, 'WARNING!!! The e-mail and e-mail confirmation fields do not match'
            )
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(
                request, 'WARNING!!! This email is already registered'
            )
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(
                request, 'WARNING!!! This username already exists. Please insert another'
            )
            return redirect('register')
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=name, last_name=surname
        )
        user_address = UserProfile.objects.create(
            username=user, address=address, number=number, district=district, 
            city=city, uf=uf, complement=complement, zip_code=zip_code
        )
        user.save()
        user_address.save()
        datas = {
            'user': user,
            'user_address': user_address
        }
        
        messages.success(request, 'Successful registration', datas)
        return redirect('login')
    else:
        return render(request, 'users/register.html')


def login(request):
    """
    function login
    """
    dados_cookie = {
        'email': request.COOKIES.get('email'),
        'password': request.COOKIES.get('password')
    }

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']

        if (campo_vazio(email) or campo_vazio(senha)):
            messages.error(
                request, 'WARNING!!! E-mail and / or password fields cannot be empty'
            )
            return redirect('login')

        if User.objects.filter(email=email).exists():
            name = User.objects.filter(email=email).values_list(
                'username', flat=True
            ).get()
            user = auth.authenticate(request, username=name, password=senha)

            if user is not None:
                auth.login(request, user)
                response = redirect('home')
                response.set_cookie(key='email', value=email)
                return response

        if User.objects.filter(email=email).exists():
            messages.error(
                request, 'WARNING!!! Invalid email and / or password'
            )
        else:
            messages.error(
                request, 'WARNING!!! This email is not registered'
            )

        response = render(request, 'users/login.html')
        response.set_cookie(key='email', value=email)
        return response
    return render(request, 'users/login.html', dados_cookie)


def dashboard(request):
    if request.user.is_authenticated:
        identification = request.user.id
        products = ProductProfile.objects.order_by('product_name').filter(username=identification)

        datas = {
            'products': products
        }
        return render(request, 'users/dashboard.html', datas)
    else:
        return redirect('login')


def logout(request):
    """
    Function logout
    """
    auth.logout(request)
    return redirect('login')


def campo_vazio(campo):
    """
    Função que verifica se um determinado campo, de cadastro ou login está vazio
    """
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    """
    Função que verifica se as senha são diferentes para realizar o cadastro
    """
    return senha != senha2


def email_nao_sao_iguais(email, email2):
    """
    Função que verifica se os emails não são iguais para realizar o cadastro
    """
    return email != email2

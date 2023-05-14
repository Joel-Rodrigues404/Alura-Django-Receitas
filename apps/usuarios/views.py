from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        print(email)
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O nome nao pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request,'O email nao pode ficar em branco')
            return redirect('cadastro')
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas nao sao iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome,email=email,password=senha)
        user.save()
        messages.success(request, 'Usuario cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, "os campos de email e senha devem ser preenchidos")
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'login feito com sucesso')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def dashboard(request):
    if request.user.is_authenticated:
        identificador = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=identificador)
        dados = {
            'receitas': receitas
        }
        return render(request,'usuarios/dashboard.html',dados)
    else:
        return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')

def campo_vazio(campo):
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2


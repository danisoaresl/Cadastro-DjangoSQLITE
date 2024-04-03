from django.shortcuts import render, redirect
from django.http import HttpResponse 
from cadastro.forms import CadastroForm
from cadastro.models import Cadastro
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    sucesso = False 
    #if request.method == 'GET':
    form = CadastroForm(request.POST, request.FILES)
    if form.is_valid(): 
        sucesso = True
        form.save()
        return render(request, 'cadastro_logado.html', {'usuarios': Cadastro.objects.all()})
    contexto = {
        'form': form,
        'sucesso': sucesso
    }
    
    return render(request, 'cadastro.html', contexto)

# views.py


def logout_user(request):
    logout(request)
    return redirect('home')  # Redireciona para a página inicial após o logout

def verificar_cadastro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        # Verifica se existe um usuário com o email fornecido
        if Cadastro.objects.filter(email=email, senha=senha).exists():
            # Usuário foi cadastrado com sucesso
            return render(request, 'cadastro_logado.html', {'usuarios': Cadastro.objects.all()})
        else:
            # Usuário não foi cadastrado
            return HttpResponse("Usuário não cadastrado!")
    elif request.method == 'GET' and 'email' in request.GET:
        # Obtém o parâmetro de busca por email do GET request
        email_busca = request.GET.get('email')

        # Filtra os usuários pelo email fornecido
        usuarios = Cadastro.objects.filter(email__icontains=email_busca)

        return render(request, 'cadastro_logado.html', {'usuarios': usuarios})
    else:
        return HttpResponse("Método não permitido. Esta visualização aceita apenas solicitações POST.")


def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Cadastro, pk=usuario_id)
    usuario.delete()
    return render(request, 'cadastro_logado.html', {'usuarios': Cadastro.objects.all()})

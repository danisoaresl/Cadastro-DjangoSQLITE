from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from cadastro.forms import CadastroForm
from cadastro.models import Cadastro
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    sucesso = False 
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

def logout_user(request):
    logout(request)
    return redirect('home')


def verificar_cadastro(request):
    usuarios = Cadastro.objects.all()

    # Paginate users
    paginator = Paginator(usuarios, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    try:
        usuarios = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        usuarios = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se existe um usuário com o email fornecido
        if Cadastro.objects.filter(email=email, senha=senha).exists():
            # Usuário autenticado com sucesso
            # Redirecionar para a mesma página para exibir usuários paginados
            return render(request, 'cadastro_logado.html', {'usuarios': usuarios})
        else:
            # Usuário não autenticado
            return HttpResponse("Usuário não autenticado!")

    elif request.method == 'GET' and 'email' in request.GET:
        # Obtém o parâmetro de busca por email do GET request
        email_busca = request.GET.get('email')

        # Filtra os usuários pelo email fornecido
        usuarios = Cadastro.objects.filter(email__icontains=email_busca)

        # Paginate filtered users
        paginator = Paginator(usuarios, 10)
        page_number = request.GET.get('page')
        try:
            usuarios = paginator.page(page_number)
        except PageNotAnInteger:
            usuarios = paginator.page(1)
        except EmptyPage:
            usuarios = paginator.page(paginator.num_pages)

    return render(request, 'cadastro_logado.html', {'usuarios': usuarios})

def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Cadastro, pk=usuario_id)
    usuario.delete()
    return redirect('verificar_cadastro')

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Cadastro, pk=usuario_id)
    if request.method == 'POST':
        form = CadastroForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('verificar_cadastro')
    else:
        form = CadastroForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario_id': usuario_id})

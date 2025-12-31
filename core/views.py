from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from functools import wraps
from .models import (
    Configuracao, Banner, Faculdade, Curso, Disciplina, 
    Funcionario, Cargo, Noticia, EventoAcademico, NivelAcesso
)

def get_configuracao():
    """Obtém ou cria a configuração do site"""
    config = Configuracao.objects.first()
    if not config:
        config = Configuracao.objects.create(nome_universidade='URNM - Universidade')
    return config

def nivel_acesso_requerido(*niveis_permitidos):
    """Decorator para verificar nível de acesso do usuário"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                nivel_usuario = request.user.nivel_acesso.nivel
                if nivel_usuario in niveis_permitidos or 'administrador' in niveis_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Você não tem permissão para acessar esta área.')
                    return redirect('core:homepage')
            except NivelAcesso.DoesNotExist:
                messages.error(request, 'Seu usuário não possui nível de acesso definido.')
                return redirect('core:homepage')
        return _wrapped_view
    return decorator

def login_view(request):
    """View de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'core:homepage')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    config = get_configuracao()
    return render(request, 'core/login.html', {'config': config})

def logout_view(request):
    """View de logout"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('core:homepage')

def homepage(request):
    """Página inicial"""
    config = get_configuracao()
    banners = Banner.objects.filter(ativo=True)[:5]
    noticias_destaque = Noticia.objects.filter(publicada=True, destaque=True)[:3]
    noticias_recentes = Noticia.objects.filter(publicada=True)[:6]
    faculdades = Faculdade.objects.filter(ativo=True)
    
    context = {
        'config': config,
        'banners': banners,
        'noticias_destaque': noticias_destaque,
        'noticias_recentes': noticias_recentes,
        'faculdades': faculdades,
    }
    return render(request, 'core/homepage.html', context)

def faculdades_list(request):
    """Lista de faculdades"""
    config = get_configuracao()
    faculdades = Faculdade.objects.filter(ativo=True)
    
    context = {
        'config': config,
        'faculdades': faculdades,
    }
    return render(request, 'core/faculdades_list.html', context)

def faculdade_detail(request, faculdade_id):
    """Detalhes de uma faculdade específica"""
    config = get_configuracao()
    faculdade = get_object_or_404(Faculdade, id=faculdade_id, ativo=True)
    cursos = faculdade.cursos.filter(ativo=True)
    funcionarios = Funcionario.objects.filter(faculdade=faculdade, ativo=True)
    noticias = Noticia.objects.filter(faculdade=faculdade, publicada=True)[:5]
    
    context = {
        'config': config,
        'faculdade': faculdade,
        'cursos': cursos,
        'funcionarios': funcionarios,
        'noticias': noticias,
    }
    return render(request, 'core/faculdade_detail.html', context)

def cursos_list(request):
    """Lista de cursos"""
    config = get_configuracao()
    faculdade_id = request.GET.get('faculdade')
    nivel = request.GET.get('nivel')
    
    cursos = Curso.objects.filter(ativo=True)
    
    if faculdade_id:
        cursos = cursos.filter(faculdade_id=faculdade_id)
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    
    faculdades = Faculdade.objects.filter(ativo=True)
    
    context = {
        'config': config,
        'cursos': cursos,
        'faculdades': faculdades,
        'faculdade_selecionada': faculdade_id,
        'nivel_selecionado': nivel,
    }
    return render(request, 'core/cursos_list.html', context)

def curso_detail(request, curso_id):
    """Detalhes de um curso e sua grelha curricular"""
    config = get_configuracao()
    curso = get_object_or_404(Curso, id=curso_id, ativo=True)
    
    disciplinas_por_ano = {}
    for ano in range(1, curso.duracao_anos + 1):
        disciplinas_por_ano[ano] = {
            1: curso.disciplinas.filter(ano=ano, semestre=1).order_by('nome'),
            2: curso.disciplinas.filter(ano=ano, semestre=2).order_by('nome'),
        }
    
    context = {
        'config': config,
        'curso': curso,
        'disciplinas_por_ano': disciplinas_por_ano,
    }
    return render(request, 'core/curso_detail.html', context)

def noticias_list(request):
    """Lista de notícias"""
    config = get_configuracao()
    noticias = Noticia.objects.filter(publicada=True)
    faculdade_id = request.GET.get('faculdade')
    busca = request.GET.get('q')
    
    if faculdade_id:
        noticias = noticias.filter(faculdade_id=faculdade_id)
    if busca:
        noticias = noticias.filter(
            Q(titulo__icontains=busca) | Q(resumo__icontains=busca)
        )
    
    faculdades = Faculdade.objects.filter(ativo=True)
    
    context = {
        'config': config,
        'noticias': noticias,
        'faculdades': faculdades,
    }
    return render(request, 'core/noticias_list.html', context)

def noticia_detail(request, slug):
    """Detalhes de uma notícia"""
    config = get_configuracao()
    noticia = get_object_or_404(Noticia, slug=slug, publicada=True)
    
    noticia.visualizacoes += 1
    noticia.save(update_fields=['visualizacoes'])
    
    noticias_relacionadas = Noticia.objects.filter(
        publicada=True
    ).exclude(id=noticia.id)[:4]
    
    context = {
        'config': config,
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
    }
    return render(request, 'core/noticia_detail.html', context)

def calendario_academico(request):
    """Calendário acadêmico"""
    config = get_configuracao()
    ano = request.GET.get('ano')
    
    if not ano:
        import datetime
        ano = datetime.datetime.now().year
    else:
        ano = int(ano)
    
    eventos = EventoAcademico.objects.filter(
        ano_letivo=ano,
        publicado=True
    ).order_by('data_inicio')
    
    context = {
        'config': config,
        'eventos': eventos,
        'ano_selecionado': ano,
        'anos_disponiveis': range(ano - 2, ano + 3),
    }
    return render(request, 'core/calendario_academico.html', context)

def organigrama(request):
    """Organigrama institucional"""
    config = get_configuracao()
    
    funcionarios = Funcionario.objects.filter(ativo=True).select_related('cargo', 'superior_hierarquico')
    
    reitor = funcionarios.filter(cargo__nivel='reitor').first()
    vice_reitores = funcionarios.filter(cargo__nivel='vice_reitor')
    diretores = funcionarios.filter(cargo__nivel='diretor')
    coordenadores = funcionarios.filter(cargo__nivel='coordenador')
    
    context = {
        'config': config,
        'reitor': reitor,
        'vice_reitores': vice_reitores,
        'diretores': diretores,
        'coordenadores': coordenadores,
        'funcionarios': funcionarios,
    }
    return render(request, 'core/organigrama.html', context)

def sobre(request):
    """Página sobre a universidade"""
    config = get_configuracao()
    
    context = {
        'config': config,
    }
    return render(request, 'core/sobre.html', context)

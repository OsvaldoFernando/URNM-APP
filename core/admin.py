from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Configuracao, Banner, Faculdade, Cargo, Funcionario, 
    Curso, Disciplina, Noticia, EventoAcademico, NivelAcesso
)

admin.site.site_header = 'URNM - Administração'
admin.site.site_title = 'URNM Admin'
admin.site.index_title = 'Dashboard Administrativo'

@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ['nome_universidade', 'email_contato', 'telefone']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_universidade', 'logotipo')
        }),
        ('Cores Institucionais', {
            'fields': ('cor_primaria', 'cor_secundaria')
        }),
        ('Links Externos', {
            'fields': ('link_siga',)
        }),
        ('Sobre a Universidade', {
            'fields': ('sobre_universidade',)
        }),
        ('Contato', {
            'fields': ('email_contato', 'telefone', 'endereco')
        }),
    )
    
    def has_add_permission(self, request):
        return not Configuracao.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ordem', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    list_editable = ['ordem', 'ativo']
    search_fields = ['titulo', 'descricao']
    prepopulated_fields = {}

@admin.register(Faculdade)
class FaculdadeAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'ativo', 'ordem']
    list_filter = ['ativo']
    list_editable = ['ordem', 'ativo']
    search_fields = ['nome', 'sigla']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'sigla', 'descricao', 'imagem_capa')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'endereco')
        }),
        ('Configurações', {
            'fields': ('site_externo', 'ativo', 'ordem')
        }),
    )

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nivel', 'nivel_hierarquico']
    list_filter = ['nivel']
    search_fields = ['nome']
    ordering = ['nivel_hierarquico', 'nome']

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cargo', 'faculdade', 'email', 'ativo']
    list_filter = ['cargo', 'faculdade', 'ativo']
    search_fields = ['nome_completo', 'email']
    list_editable = ['ativo']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'foto', 'email', 'telefone')
        }),
        ('Cargo e Vínculo', {
            'fields': ('cargo', 'faculdade', 'data_admissao')
        }),
        ('Formação Acadêmica', {
            'fields': ('formacao', 'especializacao', 'biografia')
        }),
        ('Hierarquia', {
            'fields': ('superior_hierarquico', 'ordem_exibicao')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

class DisciplinaInline(admin.TabularInline):
    model = Disciplina
    extra = 1
    fields = ['codigo', 'nome', 'ano', 'semestre', 'carga_horaria', 'creditos', 'tipo', 'docente']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'faculdade', 'nivel', 'duracao_anos', 'vagas', 'coordenador', 'ativo']
    list_filter = ['faculdade', 'nivel', 'ativo']
    search_fields = ['nome']
    list_editable = ['ativo']
    inlines = [DisciplinaInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'faculdade', 'nivel', 'coordenador')
        }),
        ('Detalhes do Curso', {
            'fields': ('descricao', 'duracao_anos', 'vagas')
        }),
        ('Informações Acadêmicas', {
            'fields': ('objetivos', 'perfil_profissional', 'requisitos_ingresso')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'curso', 'ano', 'semestre', 'carga_horaria', 'creditos', 'tipo', 'docente']
    list_filter = ['curso', 'ano', 'semestre', 'tipo']
    search_fields = ['codigo', 'nome']
    filter_horizontal = ['pre_requisitos']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome', 'curso', 'tipo')
        }),
        ('Posição no Curso', {
            'fields': ('ano', 'semestre', 'carga_horaria', 'creditos')
        }),
        ('Conteúdo', {
            'fields': ('ementa', 'objetivos', 'bibliografia')
        }),
        ('Docente e Pré-requisitos', {
            'fields': ('docente', 'pre_requisitos')
        }),
    )

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'faculdade', 'destaque', 'publicada', 'data_publicacao', 'visualizacoes']
    list_filter = ['publicada', 'destaque', 'faculdade', 'data_publicacao']
    search_fields = ['titulo', 'resumo', 'conteudo']
    list_editable = ['destaque', 'publicada']
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ['visualizacoes', 'data_publicacao', 'data_atualizacao']
    fieldsets = (
        ('Conteúdo', {
            'fields': ('titulo', 'slug', 'resumo', 'conteudo', 'imagem_destaque')
        }),
        ('Classificação', {
            'fields': ('faculdade', 'autor')
        }),
        ('Publicação', {
            'fields': ('destaque', 'publicada', 'data_publicacao', 'data_atualizacao', 'visualizacoes')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

@admin.register(EventoAcademico)
class EventoAcademicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'data_inicio', 'data_fim', 'ano_letivo', 'semestre', 'faculdade', 'publicado']
    list_filter = ['tipo', 'ano_letivo', 'semestre', 'faculdade', 'publicado']
    search_fields = ['titulo', 'descricao']
    list_editable = ['publicado']
    date_hierarchy = 'data_inicio'
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('titulo', 'descricao', 'tipo')
        }),
        ('Período', {
            'fields': ('data_inicio', 'data_fim', 'ano_letivo', 'semestre')
        }),
        ('Classificação', {
            'fields': ('faculdade', 'publicado')
        }),
    )

class NivelAcessoInline(admin.StackedInline):
    model = NivelAcesso
    can_delete = False
    verbose_name = 'Nível de Acesso'
    verbose_name_plural = 'Níveis de Acesso'
    fields = ['nivel', 'funcionario']

class UserAdmin(BaseUserAdmin):
    inlines = [NivelAcessoInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(NivelAcesso)
class NivelAcessoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nivel', 'funcionario']
    list_filter = ['nivel']
    search_fields = ['usuario__username', 'usuario__email']

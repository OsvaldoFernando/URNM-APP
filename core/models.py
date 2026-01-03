from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Configuracao(models.Model):
    """Configurações gerais do site da universidade"""
    nome_universidade = models.CharField(max_length=200, default='BIOCON')
    logotipo = models.ImageField(upload_to='configuracao/', null=True, blank=True)
    cor_primaria = models.CharField(max_length=7, default='#003366', help_text='Cor primária em hexadecimal (Navy Blue)')
    cor_secundaria = models.CharField(max_length=7, default='#C69214', help_text='Cor secundária em hexadecimal (Gold)')
    link_siga = models.URLField(max_length=500, blank=True, help_text='Link para o sistema SIGA')
    sobre_universidade = RichTextField(blank=True)
    email_contato = models.EmailField(blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    endereco = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
    
    def __str__(self):
        return self.nome_universidade
    
    def save(self, *args, **kwargs):
        if not self.pk and Configuracao.objects.exists():
            raise ValueError('Só pode existir uma configuração')
        return super().save(*args, **kwargs)

class Banner(models.Model):
    """Banners/Carrossel da página inicial"""
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='banners/')
    link = models.URLField(max_length=500, blank=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['ordem', '-data_criacao']
    
    def __str__(self):
        return self.titulo

class Faculdade(models.Model):
    """Faculdades da universidade (ITA, IP, FMM, etc)"""
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10)
    descricao = RichTextField(blank=True)
    imagem_capa = models.ImageField(upload_to='faculdades/', null=True, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    endereco = models.TextField(blank=True)
    site_externo = models.URLField(max_length=500, blank=True, help_text='Link para site externo da faculdade')
    ativo = models.BooleanField(default=True)
    ordem = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Faculdade'
        verbose_name_plural = 'Faculdades'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return f'{self.sigla} - {self.nome}'

class Cargo(models.Model):
    """Cargos para funcionários e professores"""
    NIVEL_CHOICES = [
        ('reitor', 'Reitor'),
        ('vice_reitor', 'Vice-Reitor'),
        ('diretor', 'Diretor de Faculdade'),
        ('coordenador', 'Coordenador de Curso'),
        ('professor', 'Professor'),
        ('administrativo', 'Administrativo'),
    ]
    
    nome = models.CharField(max_length=200)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    nivel_hierarquico = models.IntegerField(default=10, help_text='1=Reitor, 2=Vice-Reitor, etc')
    descricao = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nivel_hierarquico', 'nome']
    
    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    """Funcionários administrativos e professores"""
    nome_completo = models.CharField(max_length=200)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='funcionarios/', null=True, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    biografia = RichTextField(blank=True)
    formacao = models.TextField(blank=True, help_text='Formação acadêmica')
    especializacao = models.TextField(blank=True)
    data_admissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    superior_hierarquico = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados')
    ordem_exibicao = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['cargo__nivel_hierarquico', 'ordem_exibicao', 'nome_completo']
    
    def __str__(self):
        return f'{self.nome_completo} - {self.cargo}'

class Curso(models.Model):
    """Cursos oferecidos pelas faculdades"""
    NIVEL_CHOICES = [
        ('licenciatura', 'Licenciatura'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]
    
    nome = models.CharField(max_length=200)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.CASCADE, related_name='cursos')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='licenciatura')
    descricao = RichTextField(blank=True)
    duracao_anos = models.IntegerField(default=4, help_text='Duração em anos')
    vagas = models.IntegerField(default=30)
    coordenador = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos_coordenados')
    objetivos = RichTextField(blank=True)
    perfil_profissional = RichTextField(blank=True, help_text='Perfil do profissional formado')
    requisitos_ingresso = RichTextField(blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['faculdade', 'nome']
    
    def __str__(self):
        return f'{self.nome} - {self.faculdade.sigla}'

class Disciplina(models.Model):
    """Disciplinas da grelha curricular"""
    TIPO_CHOICES = [
        ('obrigatoria', 'Obrigatória'),
        ('optativa', 'Optativa'),
        ('eletiva', 'Eletiva'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='disciplinas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='obrigatoria')
    ano = models.IntegerField(help_text='Ano do curso (1, 2, 3, 4)')
    semestre = models.IntegerField(help_text='Semestre (1 ou 2)')
    carga_horaria = models.IntegerField(help_text='Carga horária total')
    creditos = models.IntegerField(default=3)
    ementa = RichTextField(blank=True)
    objetivos = RichTextField(blank=True)
    bibliografia = RichTextField(blank=True)
    docente = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='disciplinas_lecionadas')
    pre_requisitos = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependentes')
    
    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['curso', 'ano', 'semestre', 'nome']
    
    def __str__(self):
        return f'{self.codigo} - {self.nome}'

class Noticia(models.Model):
    """Notícias da universidade"""
    titulo = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    resumo = models.TextField(max_length=500)
    conteudo = RichTextField()
    imagem_destaque = models.ImageField(upload_to='noticias/')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.SET_NULL, null=True, blank=True, help_text='Notícia específica de uma faculdade')
    destaque = models.BooleanField(default=False, help_text='Aparecer na área de destaque')
    publicada = models.BooleanField(default=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    visualizacoes = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-data_publicacao']
    
    def __str__(self):
        return self.titulo

class EventoAcademico(models.Model):
    """Eventos do calendário acadêmico"""
    TIPO_CHOICES = [
        ('inicio_aulas', 'Início das Aulas'),
        ('fim_aulas', 'Fim das Aulas'),
        ('exames', 'Período de Exames'),
        ('matriculas', 'Matrículas'),
        ('ferias', 'Férias'),
        ('outro', 'Outro Evento'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = RichTextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    ano_letivo = models.IntegerField()
    semestre = models.IntegerField(choices=[(1, '1º Semestre'), (2, '2º Semestre')], null=True, blank=True)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.CASCADE, null=True, blank=True, help_text='Evento específico de uma faculdade')
    publicado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Evento Acadêmico'
        verbose_name_plural = 'Eventos Acadêmicos'
        ordering = ['data_inicio']
    
    def __str__(self):
        return f'{self.titulo} - {self.data_inicio}'

class NivelAcesso(models.Model):
    """Níveis de acesso customizados para usuários"""
    NIVEL_CHOICES = [
        ('administrador', 'Administrador'),
        ('gestor', 'Gestor'),
        ('professor', 'Professor'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nivel_acesso')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='professor')
    funcionario = models.OneToOneField(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, help_text='Vincular a um funcionário')
    
    class Meta:
        verbose_name = 'Nível de Acesso'
        verbose_name_plural = 'Níveis de Acesso'
    
    def __str__(self):
        return f'{self.usuario.username} - {self.get_nivel_display()}'

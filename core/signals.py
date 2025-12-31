from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NivelAcesso

@receiver(post_save, sender=User)
def criar_nivel_acesso(sender, instance, created, **kwargs):
    """Cria automaticamente um NivelAcesso para novos usuários"""
    if created:
        NivelAcesso.objects.get_or_create(
            usuario=instance,
            defaults={'nivel': 'professor'}
        )

@receiver(post_save, sender=User)
def salvar_nivel_acesso(sender, instance, **kwargs):
    """Garante que o NivelAcesso existe ao salvar usuário"""
    if hasattr(instance, 'nivel_acesso'):
        instance.nivel_acesso.save()
    else:
        NivelAcesso.objects.get_or_create(
            usuario=instance,
            defaults={'nivel': 'professor'}
        )

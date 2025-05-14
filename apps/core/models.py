from django.db import models
from django.contrib.auth.models import User

class Foto(models.Model):
    imagem = models.ImageField(upload_to='fotos/')
    descricao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fotos')
    aprovada = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Foto de {self.usuario.username} - {'Aprovada' if self.aprovada else 'Pendente'}"

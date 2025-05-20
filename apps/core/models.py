from django.db import models
from django.contrib.auth.models import User

class Foto(models.Model):
    imagem = models.ImageField(upload_to='fotos/', blank=True, null=True)
    imagem_url = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True)
    usuario_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fotos')
    aprovada = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        db_table = 'fotos'
    
    def __str__(self):
        return f"Foto de {self.usuario_id.username} - {'Aprovada' if self.aprovada else 'Pendente'}"

class Curtida(models.Model):
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_id = models.ForeignKey('Foto', on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'
        db_table = 'curtidas'
        unique_together = ['usuario_id', 'foto_id']

    def __str__(self):
        return f'{self.usuario_id.username} curtiu {self.foto_id.id}'

class Comentario(models.Model):
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_id = models.ForeignKey('Foto', on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        db_table = 'comentarios'

    def __str__(self):
        return f'{self.usuario_id.username} comentou na foto {self.foto_id.id}'

from django.db import models


class Hash(models.Model):
    nome = models.CharField(max_length=50)
    chave = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - {self.chave} - {self.valor}"

    class Meta:
        verbose_name = "Hash"
        verbose_name_plural = "Hashes"

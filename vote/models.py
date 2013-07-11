import hashlib
from django.db import models


class Persona(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class Votante(models.Model):
    hashed = models.CharField('Votante', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Votante'
        verbose_name_plural = 'Votantes'

    def __unicode__(self):
        return self.hashed

    def save(self, *args, **kwargs):
        self.hashed = self._hash(self.hashed)
        super(Votante, self).save(*args, **kwargs)

    @classmethod
    def get_votante(cls, name):
        return cls.objects.get(hashed=cls._hash(name))

    @classmethod
    def _hash(self, val):
        h = hashlib.sha1()
        h.update(val)
        return h.hexdigest()


class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class Voto(models.Model):
    persona = models.ForeignKey('Persona')
    votante = models.ForeignKey('Votante')
    habilidad = models.ForeignKey('Habilidad')
    valor = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        unique_together = ("persona", "votante", 'habilidad')
        ordering = ['votante', 'persona', 'habilidad']

    def __unicode__(self):
        return "V:%s, P:%s, S:%s: %d" % (self.votante, self.persona, self.habilidad, self.valor or 0)

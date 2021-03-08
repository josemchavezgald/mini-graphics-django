from django.db import models

# Create your models here.


class Paises(models.Model):
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre

class Regiones(models.Model):
	nombre = models.CharField(max_length=200)
	numero_region = models.IntegerField(null=True)
	pais = models.ForeignKey(Paises, on_delete = models.CASCADE)

	def __str__(self):
		return self.nombre


class Capitales(models.Model):
	nombre = models.CharField(max_length=200)
	pais = models.ForeignKey(Paises, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre



class Topicos(models.Model):
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return self.nombre


class Tips(models.Model):
	nombre = models.TextField()
	topico = models.ForeignKey(Topicos, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre


class data_CO2(models.Model):
	valor = models.FloatField()
	anio = models.IntegerField()
	pais = models.ForeignKey(Paises,on_delete=models.CASCADE)


class data_Temperatura(models.Model):
	promedio = models.FloatField()
	anio = models.IntegerField()
	ciudad = models.ForeignKey(Capitales,on_delete=models.CASCADE)
	pais =models.ForeignKey(Paises,on_delete = models.CASCADE)
	
class data_Deforestacion(models.Model):

	valor = models.IntegerField()
	umbral = models.IntegerField()
	anio = models.IntegerField()
	ciudad = models.ForeignKey(Capitales,on_delete=models.CASCADE)
	pais = models.ForeignKey(Paises,on_delete=models.CASCADE)
























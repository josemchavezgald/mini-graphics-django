from django.shortcuts import render
from django.db.models import Sum,Avg
from json import dumps 
from dashboard.models import Paises, Capitales,Topicos, data_CO2,Tips, \
data_Temperatura, data_Deforestacion
# Create your views here.

def format(number):
	temp = str(number)
	if len(temp) == 4:
		temp2 = temp[0]+'.'+temp[1:4]
	elif len(temp) == 5:
		temp2 = temp[0:2]+'.'+temp[2:5]
	elif len(temp) == 6:
		temp2 = temp[0:3]+'.'+temp[3:6]
	else:
		temp2 = temp
	return temp2



def generar_anios(anio1,anio2):

	lista = []
	for anio in range(anio1,anio2+1):
		lista.append(anio)
	lista.sort(reverse=True)
	return lista

def generar_umbral():

	lista = []
	i = 10
	while i <= 75:
		if i == 30:
			lista.append(i)
			i+=20
		elif i == 50:
			lista.append(i)
			i+=25
		else:
			lista.append(i)
			i+=5
	return lista

def home_index(request):
	paises = Paises.objects.all()
	topicos = Topicos.objects.all()
	context = {
		'paises': paises,
		'topicos':topicos
	}

	return render(request,'inicio.html',context)

def dashboard_index(request):
	if request.method == 'POST':
		id_pais = request.POST['selectedPais']
		id_topico = request.POST['selectedTopico']
		
		pais = Paises.objects.get(id=id_pais)
		tips = Tips.objects.filter(topico=id_topico)
		topico = Topicos.objects.get(id=id_topico)
		context = {}
		#Sin Ciudad

		if int(id_topico) == 1:
			anios = generar_anios(1990,2019)
			anio_init = anios[0]
			data_anual = data_CO2.objects.get(pais=id_pais,anio=anio_init)
			data = data_CO2.objects.filter(pais=id_pais)
			data_anual_paises = data_CO2.objects.filter(anio=anio_init)

			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.valor,'tipo': 'Emisiones CO2'}
				json_data.append(valor)


			for dato in data_anual_paises:
				valor = {'valor': dato.valor, 'pais': dato.pais.nombre,'tipo': 'Emisiones CO2'}
				json_data_anual.append(valor)

			dataAnualJSON = dumps(json_data_anual)
			dataJSON = dumps(json_data)

			context = {
				'pais':pais,
				'tips': tips,
				'topico': topico,
				'anios': anios,
				'anio_i':anio_init,
				'data_anual': data_anual,
				'data_anual_paises': dataAnualJSON,
				'data': dataJSON

			}

		elif int(id_topico) == 2:
			ciudades = []
			ciudades2 = data_Temperatura.objects.filter(pais=id_pais)

			for ciudad in ciudades2:
				if ciudad.ciudad not in ciudades:
					ciudades.append(ciudad.ciudad)

			anios = generar_anios(1990,2019)
			ciudad_init = ciudades2[0].ciudad
			anio_init = anios[0]
			total_pais = data_Temperatura.objects.filter(pais=id_pais,anio=anio_init).aggregate(total=Avg('promedio'))['total']
			data = data_Temperatura.objects.filter(ciudad=ciudad_init.id)
			data_anual = data_Temperatura.objects.get(ciudad=ciudad_init.id,anio=anio_init)
			data_anual_ciudades = data_Temperatura.objects.filter(pais=id_pais, anio=anio_init)


			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.promedio,'tipo': 'Grados Celsius'}
				json_data.append(valor)


			for dato in data_anual_ciudades:
				valor = {'valor': dato.promedio, 'pais': dato.ciudad.nombre,'tipo': 'Grados Celsius'}
				json_data_anual.append(valor)

			dataAnualJSON = dumps(json_data_anual)
			dataJSON = dumps(json_data)

			context = {
				'pais':pais,
				'ciudades':ciudades,
				'tips': tips[3],
				'topico': topico,
				'anios': anios,
				'ciudad_i': ciudad_init,
				'anio_i': anio_init,
				'data': dataJSON,
				'data_anual': data_anual,
				'data_anual_paises': dataAnualJSON,
				'total_pais': total_pais
			}
	
			# data = data_Temperatura.objects.filter()
		elif int(id_topico) == 3:


			#Tipo dato Kha
			ciudades = Capitales.objects.filter(pais=id_pais)
			anios = generar_anios(2001,2019)
			ciudad_init = ciudades[0]
			print(ciudad_init.id)
			if ciudad_init.id == 16:
				ciudad_init = ciudades[1]
			elif ciudad_init.id == 12 or ciudad_init.id == 8:
				ciudad_init = Capitales.objects.get(id=46)
				ciudades = []
			anio_init = anios[0]
			umbrales = generar_umbral()
			umbral_init = umbrales[0]


			total_pais = data_Deforestacion.objects.filter(pais=id_pais,anio=anio_init,umbral=umbral_init).aggregate(total=Sum('valor'))['total']
			data = data_Deforestacion.objects.filter(ciudad=ciudad_init.id,umbral=umbral_init)
			data_anual = data_Deforestacion.objects.get(ciudad=ciudad_init.id,pais=id_pais,anio=anio_init,umbral = umbral_init)
			print(data_anual)
			data_anual_ciudades = data_Deforestacion.objects.filter(pais=id_pais, anio=anio_init,umbral=umbral_init)


			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.valor,'tipo': 'Kilos/Hectareas'}
				json_data.append(valor)


			for dato in data_anual_ciudades:
				valor = {'valor': dato.valor, 'pais': dato.ciudad.nombre,'tipo': 'Kilos/Hectareas'}
				json_data_anual.append(valor)

			dataAnualJSON = dumps(json_data_anual)
			dataJSON = dumps(json_data)



			context = {
				'valor': format(data_anual.valor),
				'pais':pais,
				'ciudades':ciudades,
				'tips': tips,
				'topico': topico,
				'anios': anios,
				'ciudad_i': ciudad_init,
				'anio_i': anio_init,
				'umbrales': umbrales,
				'umbral_i': umbral_init,
				'data': dataJSON,
				'data_anual': data_anual,
				'total_pais': format(total_pais),
				'data_anual_paises': dataAnualJSON
			}

	return render(request,'dashboard.html',context)


def dashboard_change(request):
	is_private = request.POST.get('is_private', False);
	if request.method == 'POST':
		id_pais = request.POST['selectedPais1']
		id_topico = request.POST['selectedTopico1']
		anio = request.POST['selectedAnio']

		pais = Paises.objects.get(id=id_pais)
		tips = Tips.objects.filter(topico=id_topico)
		topico = Topicos.objects.get(id=id_topico)

		if int(id_topico) == 1:
			anios = generar_anios(1990,2019)
			data_anual = data_CO2.objects.get(pais=id_pais,anio=anio)
			data = data_CO2.objects.filter(pais=id_pais)
			data_anual_paises = data_CO2.objects.filter(anio=anio)

			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.valor,'tipo': 'Emisiones CO2'}
				json_data.append(valor)

			for dato in data_anual_paises:
				valor = {'valor': dato.valor, 'pais': dato.pais.nombre,'tipo': 'Emisiones CO2'}
				json_data_anual.append(valor)

			dataJSON = dumps(json_data)
			dataAnualJSON = dumps(json_data_anual)

			context = {
				'pais':pais,
				'tips': tips,
				'topico': topico,
				'anios': anios,
				'anio_i':anio,
				'data_anual': data_anual,
				'data_anual_paises': dataAnualJSON,
				'data': dataJSON
			}

		elif int(id_topico) == 2:
			ciudades = []
			ciudades2 = data_Temperatura.objects.filter(pais=id_pais)

			for ciudad in ciudades2:
				if ciudad.ciudad not in ciudades:
					ciudades.append(ciudad.ciudad)

			anios = generar_anios(1990,2019)
			city = Capitales.objects.get(id=request.POST['selectedCiudad'])
			ciudad_init = city
			anio_init = anio
			total_pais = data_Temperatura.objects.filter(pais=id_pais,anio=anio_init).aggregate(total=Avg('promedio'))['total']
			data = data_Temperatura.objects.filter(ciudad=ciudad_init.id)
			data_anual = data_Temperatura.objects.get(ciudad=ciudad_init.id,anio=anio_init)
			data_anual_ciudades = data_Temperatura.objects.filter(pais=id_pais, anio=anio_init)


			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.promedio,'tipo': 'Grados Celsius'}
				json_data.append(valor)


			for dato in data_anual_ciudades:
				valor = {'valor': dato.promedio, 'pais': dato.ciudad.nombre,'tipo': 'Grados Celsius'}
				json_data_anual.append(valor)

			dataAnualJSON = dumps(json_data_anual)
			dataJSON = dumps(json_data)

			context = {
				'pais':pais,
				'ciudades':ciudades,
				'tips': tips,
				'topico': topico,
				'anios': anios,
				'ciudad_i': ciudad_init,
				'anio_i': anio_init,
				'data': dataJSON,
				'data_anual': data_anual,
				'data_anual_paises': dataAnualJSON,
				'total_pais': total_pais
			}			

		elif int(id_topico) == 3:


			#Tipo dato Kha
			ciudades = Capitales.objects.filter(pais=id_pais)
			anios = generar_anios(2001,2019)
			city = Capitales.objects.get(id=request.POST['selectedCiudad'])
			ciudad_init = city
			anio_init = anio
			umbrales = generar_umbral()
			umbral_init = request.POST['selectedUmbral']


			total_pais = data_Deforestacion.objects.filter(pais=id_pais,anio=anio_init,umbral=umbral_init).aggregate(total=Sum('valor'))['total']
			data = data_Deforestacion.objects.filter(ciudad=ciudad_init.id,umbral=umbral_init)
			data_anual = data_Deforestacion.objects.get(ciudad=ciudad_init.id,anio=anio_init,umbral = umbral_init)
			data_anual_ciudades = data_Deforestacion.objects.filter(pais=id_pais, anio=anio_init,umbral=umbral_init)


			json_data = []
			json_data_anual = []

			for dato in data:
				valor = {'anio': dato.anio,'valor':dato.valor,'tipo': 'Kilos/Hectareas'}
				json_data.append(valor)


			for dato in data_anual_ciudades:
				valor = {'valor': dato.valor, 'pais': dato.ciudad.nombre,'tipo': 'Kilos/Hectareas'}
				json_data_anual.append(valor)

			dataAnualJSON = dumps(json_data_anual)
			dataJSON = dumps(json_data)



			context = {
				'valor': format(data_anual.valor),
				'pais':pais,
				'ciudades':ciudades,
				'tips': tips,
				'topico': topico,
				'anios': anios,
				'ciudad_i': ciudad_init,
				'anio_i': anio_init,
				'umbrales': umbrales,
				'umbral_i': umbral_init,
				'data': dataJSON,
				'data_anual': data_anual,
				'total_pais': format(total_pais),
				'data_anual_paises': dataAnualJSON
			}
	

	return render(request,'dashboard.html',context)
from django.shortcuts import render, render_to_response
from django.db import connection
from reports.models import *
from datetime import datetime

rm = "xxx"

#Generadores de Templates

def getReportes(request):

	rmGlobal = rm

	return render_to_response("reportes.html", locals())

def getDia(request):

	if 'fecha' in request.GET:
		date = request.GET['fecha']
	else:
		date = datetime.now()

	rmGlobal = rm
	
	consumo = genDia(date)

	return render_to_response("dia.html", locals())

def getMes(request):

	if 'mes' in request.GET:
		mes = request.GET['mes']
		ano = request.GET['ano']
		date = str(ano) + "-" + str(mes) + "-01"
		date = date.split("-")
		date = datetime(int(date[0]), int(date[1]), int(date[2]))
	else:
		date = datetime.now()

	rmGlobal = rm

	consumo = genMes(date)

	return render_to_response("mes.html", locals())

#Generadores de consulta

def genMes(date):

	ano = date.year
	if date.month < 10:
		mes = "0" + str(date.month)
	else:
		mes = date.month

	cursor = connection.cursor()
	cursor.execute('select fechahora, codvariable, valor from datos where month(fechahora) = month("'+str(date)+'") and year(fechahora) = year("'+str(date)+'");')
	rows = cursor.fetchall()
	cursor.close()

	dias = []

	for dia in range(1, 32):		
		if dia < 10:
			dia = "0" + str(dia)
		else:
			dia = str(dia)

		prp000 = []
		prp001 = []
		prp002 = []
		prs000 = []
		prs001 = []
		prs002 = []
		bow001 = []
		bow002 = []
		gep001 = []
		gep002 = []
		ges001 = []
		ges002 = []

		for r in rows:
			if int(dia) < 9:
				auxdia = "0" + str(int(dia) + 1)
			else:
				auxdia = int(dia) + 1
			#print ano, mes, dia, auxdia

			if str(r[0]) > (str(ano) + "-" + str(mes) + "-" + str(dia)) and str(r[0]) < (str(ano) + "-" + str(mes) + "-" + str(auxdia)):
				if r[1] == "PRP000":
					if r[2] > 400:
						prp000.append(r[2])
				elif r[1] == "PRP001":
					prp001.append(r[2])
				elif r[1] == "PRP002":
					prp002.append(r[2])
				elif r[1] == "PRS000":
					if r[2] > 400:
						prs000.append(r[2])
				elif r[1] == "PRS001":
					prs001.append(r[2])
				elif r[1] == "PRS002":
					prs002.append(r[2])
				elif r[1] == "BOW001":
					bow001.append(r[2])
				elif r[1] == "BOW002":
					bow002.append(r[2])
				elif r[1] == "GEP001":
					gep001.append(r[2])
				elif r[1] == "GEP002":
					gep002.append(r[2])
				elif r[1] == "GES001":
					ges001.append(r[2])
				elif r[1] == "GES002":
					ges002.append(r[2])			
					
		if len(prp002) == 0:
			consumoCombustiblePropBab = 0
		else: 
			consumoCombustiblePropBab = round((max(prp002) - min(prp002)) * 0.2641720512415584, 2)	
		if len(prp000) == 0:
			consumoHorasPropBab = 0
	 	else:
			consumoHorasPropBab = round(len(prp000) * 0.51666 / 60.0, 2)

		if len(prs002) == 0:
			consumoCombustiblePropEst = 0
		else:
			consumoCombustiblePropEst = round((max(prs002) - min(prs002)) * 0.2641720512415584, 2) 
		if len(prs000) == 0:
			consumoHorasPropEst = 0
		else:
			consumoHorasPropEst = round(len(prs000) * 0.51666 / 60.0, 2)

		if len(bow002) == 0:
			consumoCombustibleBow = 0
		else:
			consumoCombustibleBow = round((max(bow002) - min(bow002)) * 0.2641720512415584, 2) 
		if len(bow001) == 0:
			consumoHorasBow = 0
		else:
			consumoHorasBow = round((max(bow001) - min(bow001)), 2)

		if len(gep002) == 0:
			consumoCombustibleGenBab = 0
		else:
			consumoCombustibleGenBab = round((max(gep002) - min(gep002)) * 0.2641720512415584, 2) 
		if len(gep001) == 0:
			consumoHorasGenBab = 0
		else:
			consumoHorasGenBab = round((max(gep001) - min(gep001)), 2)

		if len(ges002) == 0:
			consumoCombustibleGenEst = 0
		else:
			consumoCombustibleGenEst = round((max(ges002) - min(ges002)) * 0.2641720512415584, 2) 
		if len(ges001) == 0:
			consumoHorasGenEst = 0
		else:
			consumoHorasGenEst = round((max(ges001) - min(ges001)), 2)

		total = consumoCombustiblePropBab + consumoCombustiblePropEst + consumoCombustibleBow + consumoCombustibleGenBab + consumoCombustibleGenEst
		consumos = (consumoCombustiblePropBab, consumoHorasPropBab, consumoCombustiblePropEst, consumoHorasPropEst, consumoCombustibleBow, consumoHorasBow, consumoCombustibleGenBab, consumoHorasGenBab, consumoCombustibleGenEst, consumoHorasGenEst, total)

		dias.append(consumos)							

	return dias

def genDia(date):

	cursor = connection.cursor()
	cursor.execute('select codvariable, valor from datos where dayofyear(fechahora) = dayofyear("'+str(date)+'") and year(fechahora) = year("'+str(date)+'");')
	rows = cursor.fetchall()
	cursor.close()

	prp000 = []
	prp001 = []
	prp002 = []
	prs000 = []
	prs001 = []
	prs002 = []
	bow001 = []
	bow002 = []
	gep001 = []
	gep002 = []
	ges001 = []
	ges002 = []

	for r in rows:
		if r[0] == "PRP000":
			if r[1] > 400:
				prp000.append(r[1])
		elif r[0] == "PRP001":
			prp001.append(r[1])
		elif r[0] == "PRP002":
			prp002.append(r[1])
		elif r[0] == "PRS000":
			if r[1] > 400:
				prs000.append(r[1])
		elif r[0] == "PRS001":
			prs001.append(r[1])
		elif r[0] == "PRS002":
			prs002.append(r[1])
		elif r[0] == "BOW001":
			bow001.append(r[1])
		elif r[0] == "BOW002":
			bow002.append(r[1])
		elif r[0] == "GEP001":
			gep001.append(r[1])
		elif r[0] == "GEP002":
			gep002.append(r[1])
		elif r[0] == "GES001":
			ges001.append(r[1])
		elif r[0] == "GES002":
			ges002.append(r[1])

	if len(prp002) == 0:
		consumoCombustiblePropBab = 0
	else: 
		consumoCombustiblePropBab = round((max(prp002) - min(prp002)) * 0.2641720512415584, 2)	
	if len(prp000) == 0:
		consumoHorasPropBab = 0
 	else:
		consumoHorasPropBab = round(len(prp000) * 0.51666 / 60.0, 2)

	if len(prs002) == 0:
		consumoCombustiblePropEst = 0
	else:
		consumoCombustiblePropEst = round((max(prs002) - min(prs002)) * 0.2641720512415584, 2) 
	if len(prs000) == 0:
		consumoHorasPropEst = 0
	else:
		consumoHorasPropEst = round(len(prs000) * 0.51666 / 60.0, 2)

	if len(bow002) == 0:
		consumoCombustibleBow = 0
	else:
		consumoCombustibleBow = round((max(bow002) - min(bow002)) * 0.2641720512415584, 2) 
	if len(bow001) == 0:
		consumoHorasBow = 0
	else:
		consumoHorasBow = round((max(bow001) - min(bow001)), 2)

	if len(gep002) == 0:
		consumoCombustibleGenBab = 0
	else:
		consumoCombustibleGenBab = round((max(gep002) - min(gep002)) * 0.2641720512415584, 2) 
	if len(gep001) == 0:
		consumoHorasGenBab = 0
	else:
		consumoHorasGenBab = round((max(gep001) - min(gep001)), 2)

	if len(ges002) == 0:
		consumoCombustibleGenEst = 0
	else:
		consumoCombustibleGenEst = round((max(ges002) - min(ges002)) * 0.2641720512415584, 2) 
	if len(ges001) == 0:
		consumoHorasGenEst = 0
	else:
		consumoHorasGenEst = round((max(ges001) - min(ges001)), 2)

	total = consumoCombustiblePropBab + consumoCombustiblePropEst + consumoCombustibleBow + consumoCombustibleGenBab + consumoCombustibleGenEst
	consumos = (consumoCombustiblePropBab, consumoHorasPropBab, consumoCombustiblePropEst, consumoHorasPropEst, consumoCombustibleBow, consumoHorasBow, consumoCombustibleGenBab, consumoHorasGenBab, consumoCombustibleGenEst, consumoHorasGenEst, total)

	return consumos
import time
start_time = time.time()
import json
import datetime
import httpx
import pandas as pd
import sqlite3
from Pte import Paciente
import baseDatos
from Evaluar import Evaluacion
from nlpMedico import constHistoria, awsDiagnostico, awsMedicamentos
from simulacionMC import pacienteMC
from optimizacionConstantes import Tratamientos
import requests
global idInc
global tratamiento
idInc=0

# Press the green button in the gutter to run the script.
##SQLite --Conection
conn = sqlite3.connect('test.db')
#baseDatos.crearTablas(conn)
#baseDatos.crearTablaMedicamentos(conn)
#baseDatos.alterarTablas(conn)


def connectAPI(url='http://localhost:8000/IPS/'):
    x = httpx.get(url) ##Get the info from the API
    paciente_data = x.json()["paciente"]
    paciente_dict = json.loads(paciente_data)
    paciente_data = paciente_dict['paciente']
    apiPaciente = Paciente(edad=paciente_data['edad'], imc=paciente_data['imc'], tfg=paciente_data['tfg'], hba1c=paciente_data['hba1c'], meta_hba1c=paciente_data['meta_hba1c'], medicamento=paciente_data['medicamento'], antecedente=paciente_data['antecedente'], tolera_metform=paciente_data['tolera_metform'], hipos=paciente_data['hipos'], glicemia=paciente_data['glicemia'], ultGlicada=paciente_data['ultGlicada'], ultCreatinina=paciente_data['ultCreatinina'], tolera_aGLP1=paciente_data['tolera_aGLP1'])
    return apiPaciente

def pruebaAPI():
    return 'Saludos'



# for i in range(1, 51): #(Queda indentado a la izquierda)

def mainSucre():
        mds = awsMedicamentos(constHistoria.historia)
        antecedente = awsDiagnostico(constHistoria.historia)
        ##Montar un paciente con lo de la historia (medicamentos e historia) en Friduski
        ###


        ##FRIDUSKI
        pte = Paciente(35,28,75,8,7,mds,
                       antecedente,
                       False, True, 235, 2, 7,False)


        # medications = ['Metformina', 'Glibenclamida', 'Glimepiride', 'Empaglifozina', 'Dapaglifozina', 'canaglifozina',
        #                'sotaglifozina', 'linagliptina', 'Vildagliptina', 'sitagliptina', 'Semaglutide 1', 'Liraglutide',
        #                'Exenatide', 'Dulaglutide', 'Glargina U100', 'Glargina U300', 'Degludec', 'Detemir', 'NPH',
        #                'Glulisina', 'Aspart',
        #                'Cristalina', 'Lispro']


        # pte=connectAPI()

        # pte=pacienteMC().pteSimulado
        # baseDatos.guardarPaciente(conn, pte.edad,pte.imc, pte.tfg, pte.hba1c, pte.meta_hba1c , str(",".join(pte.medicamento)),
        #                                         str(",".join(pte.antecedente)), pte.tolera_metform, pte.hipos,pte.glicemia,pte.ultGlicada,
        #                           pte.ultCreatinina,pte.tolera_aGLP1,pte.cuantosADO,pte.subGrupoMedicamento,datetime.datetime.now())

        # pte.identif=baseDatos.obtenerIdentif(conn)

        ##Prediagnosticar:
        pte.m_preDiagnostico()
        # print(pte.prediagnostico)
        # print('Los ADOS que tiene son: ' + pte.cuantosADO)


        # now = datetime.datetime.now()
        # now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        # baseDatos.guardarEvaluacion(conn, pte.identif,'Prediagnostico',pte.via,str(",".join(pte.prediagnostico)),datetime.datetime.now())

        #Siempre arranca en la 0
        pte.via=0

        pteVia=pte.eval_via(0)

        while pte.salida==False:
            if pte.via==1:
                ##PteVia(izq) tendra el nuevo valor de la via a evaluar (actual)
               pteVia = pte.eval_via(pteVia)
               #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==2:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==3:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==4:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==5:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==6:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==7:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==8:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==9:
                pteVia =pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==10:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==11:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==12:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==13:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==14:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==15:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==16:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==17:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==18:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==19:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==20:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==21:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==22:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==23:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==24:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==25:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==26:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==27:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==28:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==29:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==30:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==31:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==32:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==33:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==34:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==35:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==36:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==37:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==38:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==39:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==40:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==41:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==42:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==43:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==44:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==45:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==46:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==47:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==48:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==49:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia==50:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 50:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 51:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 52:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 53:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 54:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 55:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 56:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 57:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 58:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 59:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 60:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 61:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 62:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 63:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 64:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
            if pteVia == 65:
                pteVia = pte.eval_via(pteVia)
                #baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())


        # ##baseDatos.guardarEvaluacion(conn, pte.identif, 'Via', pte.via,','.join(pte.tratamiento['Tratamiento'].astype(str)),datetime.datetime.now())
        #baseDatos.guardarEvaluacion(conn, pte.identif, 'Zalida', pte.via,','.join(pte.tratamiento['Tratamiento'].unique().astype(str)),datetime.datetime.now())
        # print('Tratamiento final')
        # print(pte.tratamiento)
        # print('________________________________________________')
        # print('SIN DUPLICADOS')
        # print(pd.DataFrame(pte.tratamiento['Tratamiento'].unique(),columns=['Tratamiento']))

        # print('Via en la que se salio: '+str(pte.via))



        # url = "http://localhost:8000/tto"
        # response = requests.post(url, json=json.loads(pte.tto_tostr()))
        # print(response.json())

        # return pte.tto_tostr()
        return pte.tto_tostr()

# conn.close() #(Queda indentado a la izquierda)

end_time = time.time()
execution_time = end_time - start_time
# print("Execution time:", execution_time, "seconds")

# print(resultado)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
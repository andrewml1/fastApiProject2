import json
import httpx as httpx
from Pte import Paciente

# This is a sample Python script.


# for i in range(1, 31): #(Queda indentado a la izquierda)
def connectAPI(url='http://localhost:8000/IPS/'):
    x = httpx.get(url) ##Get the info from the API
    paciente_data = x.json()["paciente"]
    paciente_dict = json.loads(paciente_data)
    paciente_data = paciente_dict['paciente']
    apiPaciente = Paciente(edad=paciente_data['edad'], imc=paciente_data['imc'], tfg=paciente_data['tfg'], hba1c=paciente_data['hba1c'], meta_hba1c=paciente_data['meta_hba1c'], medicamento=paciente_data['medicamento'], antecedente=paciente_data['antecedente'], tolera_metform=paciente_data['tolera_metform'], hipos=paciente_data['hipos'], glicemia=paciente_data['glicemia'], ultGlicada=paciente_data['ultGlicada'], ultCreatinina=paciente_data['ultCreatinina'], tolera_aGLP1=paciente_data['tolera_aGLP1'])
    return apiPaciente

def pruebaPTE(pte):

        ##Prediagnosticar:
        pte.m_preDiagnostico()
        print(pte.prediagnostico)
        print('Los ADOS que tiene son: ' + pte.cuantosADO)

        #Siempre arranca en la 0
        pte.via=0
        pteVia=pte.eval_via(0)
        while pte.salida==False:
            if pte.via==1:
                ##PteVia(izq) tendra el nuevo valor de la via a evaluar (actual)
               pteVia = pte.eval_via(pteVia)
               
            if pteVia==2:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==3:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==4:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==5:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==6:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==7:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==8:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==9:
                pteVia =pte.eval_via(pteVia)
                
            if pteVia==10:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==11:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==12:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==13:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==14:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==15:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==16:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==17:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==18:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==19:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==20:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==21:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==22:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==23:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==24:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==25:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==26:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==27:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==28:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==29:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==30:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==31:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==32:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==33:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==34:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==35:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==36:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==37:
                pteVia = pte.eval_via(pteVia)

            if pteVia==38:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==39:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==40:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==41:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==42:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==43:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==44:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==45:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==46:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==47:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==48:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==49:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia==50:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 50:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 51:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 52:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 53:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 54:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 55:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 56:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 57:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 58:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 59:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 60:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 61:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 62:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 63:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 64:
                pteVia = pte.eval_via(pteVia)
                
            if pteVia == 65:
                pteVia = pte.eval_via(pteVia)
                


        print('Tratamiento final')
        print(pte.tratamiento)
        print('Via en la que se salio: '+str(pte.via))

        #
        # url = "http://localhost:8000/tto"
        # response = requests.post(url, json=json.loads(pte.tto_tostr()))
        # print(response.json())

        return ','.join(pte.tratamiento['Tratamiento'].astype(str))
        # conn.close() #(Queda indentado a la izquierda)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

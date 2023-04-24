import json
import pandas as pd
from Evaluar import Evaluacion


class Paciente:
    def __init__(self, edad, imc, tfg, hba1c, meta_hba1c,medicamento, antecedente,tolera_metform,hipos,glicemia,ultGlicada,ultCreatinina,tolera_aGLP1,via=0, salida=False):
        self.identif = ""
        self.edad = edad
        self.imc = imc
        self.tfg = tfg
        self.hba1c = hba1c #Pensar como poner la fecha
        self.meta_hba1c = meta_hba1c
        self.medicamento = medicamento
        self.antecedente = antecedente #Pensar como tener una lista de estos
        self.tolera_metform = tolera_metform #boolean
        self.hipos = hipos #boolean
        self.catabolicos = "" #Como lo vamos a nombrar en la historia?
        self.glicemia = glicemia
        self.ultGlicada = ultGlicada #(datetime.today()-datetime.datetime.strptime(ultGlicada, '%m-%d-%Y').date()).days/30
        self.ultCreatinina = ultCreatinina #(datetime.today()-datetime.datetime.strptime(ultGlicada, '%m-%d-%Y').date()).days/30
        self.tolera_aGLP1 = tolera_aGLP1 #boolean
        self.via=via
        self.salida=salida #Clave por que es el que da la salida del ciclo
        self.prediagnostico = pd.DataFrame(columns=['Prediagnostico']) #Dataframe de Pandas que luego va ser poblado
        self.tratamiento = pd.DataFrame(columns=['Via','Tratamiento'])  # Dataframe de Pandas que luego va ser poblado
        self.tipoTto = ''
        self.subGrupoMedicamento =''
        self.cuantosADO =''

    def m_preDiagnostico(self):
        eval_pte = Evaluacion(self.identif, 2, self)
        prediagnos = eval_pte.m_preDiagnostico(self)
        self.prediagnostico=prediagnos

    def eval_via(self, num):
        eval_pte = Evaluacion(self.identif, 2, self)
        method_name = f"m_via{num}"
        getattr(eval_pte, method_name)(self)
        return self.via

    def m_evaluar(self):
        eval_pte = Evaluacion(self.identif, 2, self)
        buscarVia=eval_pte.m_Buscarvia(self)
        evaluarVia = eval_pte.m_Evaluarvia(self, buscarVia)  # Via en la que queda el paciente
        diagnost = eval_pte.m_Tratamiento(self,evaluarVia)  # Via en la que queda el paciente


    #
    # def arbolDM2(self):
    #     # hba1c es actual (menor a 3 meses)
    #     if self.antecedente != 'risk cardio':
    #         if (self.hba1c/self.meta_hba1c)>1:
    #             lejosMeta=self.hba1c-self.meta_hba1c
    #             if lejosMeta<1.5:
    #                 if self.medicamento=='':
    #                     if self.tfg<15:
    #                         return 'linagliptina'
    #                     elif self.tfg>15 and self.tfg<30:
    #                         return 'idpp4'
    #                     elif self.tfg>30 and self.tfg<45:
    #                         return 'metformina 500 cada 12'
    #                     else:
    #                         return 'metformina 1000 cada 12'
    #                 elif self.medicamento=='ados':
    #                     return 'Prueba_ados'
    #                 elif self.medicamento=='glp1':
    #                     return 'Prueba_glp1'
    #                 elif self.medicamento=='insulina':
    #                     return 'Prueba_insulina'
    #     else:
    #         return 'mayor'

    def pte_tostr(self):
        paciente_data = {
            'edad': self.edad,
            'imc': self.imc,
            'tfg': self.tfg,
            'hba1c': self.hba1c,
            'meta_hba1c': self.meta_hba1c,
            'medicamento': self.medicamento,
            'antecedente': self.antecedente,
            'tolera_metform': self.tolera_metform,
            'hipos': self.hipos,
            'glicemia': self.glicemia,
            'ultGlicada': self.ultGlicada,
            'ultCreatinina': self.ultCreatinina,
            'tolera_aGLP1': self.tolera_aGLP1,
        }

        json_data = json.dumps({'paciente': paciente_data})
        return json_data

    def tto_tostr(self):
        paciente_data = {
            'tratamiento': ','.join(self.tratamiento['Tratamiento'].astype(str))
        }

        json_data = json.dumps({'paciente': paciente_data})
        return json_data
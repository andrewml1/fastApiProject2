import os
import sqlite3
import pandas as pd
import medicamentos as md

class constTipotto:
    naive = ''
    ADOS = 'ADOS'
    aglp1 = 'aGLP1.'
    Insulina = 'Insulina'

class constPredx:
    ADOS = 'ADOS'
    aglp1 = 'aGLP1.'
    Insulina = 'Insulina'

class constRisks:
    risk_cardio='risk cardio'
    no_risk_cardio = 'no risk cardio'
    risk_hipoglicemia='risk hipoglicemia'
    no_risk_hipoglicemia='no risk hipoglicemia'
    risk_insulinopenia='insulinopenia'
    no_risk_insulinopenia='no insulinopenia'
    risk_dialisis = 'dialisis'
    no_risk_dialisis = 'no dialisis'


# Va a dar
class Evaluacion:

    def __init__(self, id, fecha, paciente):
        self.id = id
        self.fecha = fecha
        self.paciente = paciente
        self.conn= sqlite3.connect('test.db')


    def m_Buscarvia(self, paciente):
        ##Devuelve en que via esta el paciente
        return 1  # Numero de via en la que se encuentra

    def m_Evaluarvia(self, paciente, viaActual):
        # De acuerdo a la via en la que se encuentra hace un recorrido y da un diagnostico
        ##Revisa en que punto esta y de alli se ira recorriendo el arbol

        return 1  # Numero de via en la que evaluo

    def m_preDiagnostico(self, paciente):

        #################### Prediagnostico --Debe de cambiar con GPT
        if "infarto" in paciente.antecedente or "iam" in paciente.antecedente or "enfermedad coronaria" in paciente.antecedente or "enfermedad coronaria" in paciente.antecedente\
                or "stroke" in paciente.antecedente or "sv" in paciente.antecedente or "acv" in paciente.antecedente or "enfermedad vascular periferica" in paciente.antecedente \
                or "falla cardiaca" in paciente.antecedente or "icc" in paciente.antecedente or "eaoc" in paciente.antecedente or "angina inestable" in paciente.antecedente:
            paciente.prediagnostico=paciente.prediagnostico.append(pd.Series([constRisks.risk_cardio], index=['Prediagnostico']), ignore_index=True)
        else:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.no_risk_cardio], index=['Prediagnostico']), ignore_index=True)

        if paciente.hba1c>10 or "crisis hiperglicemica" in paciente.antecedente or paciente.glicemia>300:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.risk_insulinopenia], index=['Prediagnostico']), ignore_index=True)
        else:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.no_risk_insulinopenia], index=['Prediagnostico']), ignore_index=True)

        if paciente.tfg<5 or "dialisis" in paciente.antecedente:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.risk_dialisis], index=['Prediagnostico']), ignore_index=True)
        else:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.no_risk_dialisis], index=['Prediagnostico']), ignore_index=True)

        if paciente.edad>65 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique() \
                or paciente.tfg<40 or "hipoglicemia grave" in paciente.antecedente or "hipoglicemia" in paciente.antecedente \
                or constRisks.risk_cardio in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.risk_hipoglicemia], index=['Prediagnostico']), ignore_index=True)
        else:
            paciente.prediagnostico = paciente.prediagnostico.append(pd.Series([constRisks.no_risk_hipoglicemia], index=['Prediagnostico']), ignore_index=True)

        #################### Method - Medicamentos NLP
        ##Seleccionara unicamenete los medicamentos de la diabetes que nos interesan
        ##Estos seran los que iran en el pdAux en lugar de los medicamentos con los que viene el paciente
        # self.medicamentosNLP(paciente) ##Revisar que llegue como una lista

        #################### Method - Fuzzy Logic method (no tiene en cuenta el contexto)
        # fuzzyMedicamentos=self.fuzzyCompare(paciente.medicamento,md.constListas.medicamentos)####Nueva, fuzzy
        # if len(fuzzyMedicamentos)>0:
        #     paciente.medicamento=fuzzyMedicamentos

        # fuzzyAntecedentes=self.fuzzyCompare(paciente.antecedente,md.constListas.antecedentes)####Nueva, fuzzy
        # if len(fuzzyMedicamentos)>0:
        #     paciente.antecedente=fuzzyAntecedentes

        # self.clinicalBERTModelo()


        #################### Tipo de Tratamiento
        ### Modificar por que va depender del NLP
        pdMedicamentos=self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/','Medicamentos_DM2.csv')
        dfMedicamentos=pd.DataFrame(paciente.medicamento, columns=['Medicamento'])
        merged_df = pd.merge(dfMedicamentos,pdMedicamentos, on='Medicamento', how='left')

        ##Escribe los subgrupos unicos en una lista
        paciente.subGrupoMedicamento = merged_df['Subgrupos'].unique().tolist()

        if len(paciente.medicamento)=='':
            paciente.tipoTto=constTipotto.naive
        elif (constTipotto.ADOS in merged_df['Grupos'].unique()) and (constTipotto.aglp1 not in merged_df['Grupos'].unique()) and (constTipotto.Insulina not in merged_df['Grupos'].unique()):
            paciente.tipoTto = constTipotto.ADOS
        elif constTipotto.aglp1 in merged_df['Grupos'].unique() and constTipotto.Insulina not in merged_df['Grupos'].unique():
            paciente.tipoTto = constTipotto.aglp1
        elif constTipotto.Insulina in merged_df['Grupos'].unique():
            paciente.tipoTto = constTipotto.Insulina


        #################### NLP -- Historia Clinica
        # self.procesarHistoria(paciente) ##Revisar que llegue como una lista

        #################### Contar ADOS
        if paciente.tipoTto==constTipotto.ADOS:
            self.cuantosADOS(paciente, merged_df)

        #Retorna el paciente con el prediagnostico
        return paciente.prediagnostico

    #################### Method - cuantos ADOS tiene
    def cuantosADOS(self, paciente,dfMedicamentos):
        ### Filtrar solo por ADOS
        dfFiltered= dfMedicamentos.loc[dfMedicamentos['Grupos'] == constTipotto.ADOS]
        # dfADOS = self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/','cuantos_ADO.csv')

        numSubgrupos=len(dfFiltered['Subgrupos'].unique())

        if numSubgrupos==4:
            paciente.cuantosADO='4A'
        elif numSubgrupos==3:
            if 'Metformina' in paciente.subGrupoMedicamento and 'iDPP4.' in paciente.subGrupoMedicamento and 'iSGLT2.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '3A'
            elif 'Metformina' in paciente.subGrupoMedicamento and 'iSGLT2.' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '3B'
            elif 'Metformina' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento and 'iDPP4.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '3C'
            elif 'iDPP4.' in paciente.subGrupoMedicamento and 'iSGLT2.' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '3D'
        elif numSubgrupos == 2:
            if 'Metformina' in paciente.subGrupoMedicamento and 'iDPP4.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2A'
            elif 'Metformina' in paciente.subGrupoMedicamento and 'iSGLT2.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2B'
            elif 'Metformina' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2C'
            elif 'iDPP4.' in paciente.subGrupoMedicamento and 'iSGLT2.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2D'
            elif 'iDPP4.' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2E'
            elif 'iSGLT2.' in paciente.subGrupoMedicamento and 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '2F'
        else:
            if 'Metformina' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '1A'
            elif 'iDPP4.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '1B'
            elif 'iSGLT2.' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '1C'
            elif 'SU' in paciente.subGrupoMedicamento:
                paciente.cuantosADO = '1D'


    def readFile(self,path,file):
        ###Traduccion grupos medicamentos
        os.getcwd()
        os.chdir(path)
        os.getcwd()
        pdMedicamentos = pd.read_csv(file)
        return pdMedicamentos

    def recetarTratamiento(self,accion,medicamento, dosis='', freq='', titulacion=''):
        medicamento = md.Medicamento(medicamento)  ##Generico para medicamento o Subgrupo
        formula = medicamento.recetar(accion, dosis, freq, titulacion)
        tratamiento = formula.toSring()  ##It is a string
        return tratamiento


###################################### Vias ######################################

    def m_via0(self, paciente):
        if constRisks.no_risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.ultCreatinina>12:
                tratamiento = md.constOrdenes.creatinina_hba1c
                self.appendTratamiento(paciente, tratamiento)
                if md.constSubG.Basal in paciente.subGrupoMedicamento or md.constSubG.Prandial in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    self.m_via0_1(paciente)
                else:
                    if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique():
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar,md.constSubG.Basal,md.constDosis.insulina_02)
                        self.appendTratamiento(paciente, tratamiento)
                        self.m_via0_1(paciente)
                    else:
                        self.m_via0_1(paciente)
            else:
                paciente.via = 1
        else:
            paciente.via = 1

    def m_via0_1(self, paciente):
        if md.constSubG.SU in paciente.subGrupoMedicamento:
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                paciente.via = 64
        else:
            paciente.via = 64


    def m_via1(self, paciente):
        if constRisks.risk_cardio in paciente.prediagnostico['Prediagnostico'].unique():
            if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar,md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                        paciente.via = 2
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 2
                else:
                    if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                        paciente.via = 2
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 2
            else:
                if paciente.tfg<25:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        paciente.via = 2
                    else:
                        if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                            paciente.via = 2
                        else:
                            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 2
                elif paciente.tfg>=25:
                    if md.constSubG.aGLP1 in paciente.subGrupoMedicamento or md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        paciente.via=2
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 2
        else:
            paciente.via = 2


    def m_via2(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if md.constSubG.iSGLT2 not in paciente.subGrupoMedicamento:
                if md.constSubG.Metformina not in paciente.subGrupoMedicamento:
                    if md.constMedicamentos.Exenatide not in paciente.medicamento or md.constMedicamentos.Lixisenatide not in paciente.medicamento:
                        self.m_via2_2(paciente)
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        self.m_via2_2(paciente)
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constMedicamentos.Exenatide not in paciente.medicamento or md.constMedicamentos.Lixisenatide not in paciente.medicamento:
                        self.m_via2_2(paciente)
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        self.m_via2_2(paciente)
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if md.constSubG.Metformina not in paciente.subGrupoMedicamento:
                    if md.constMedicamentos.Exenatide not in paciente.medicamento or md.constMedicamentos.Lixisenatide not in paciente.medicamento:
                        self.m_via2_2(paciente)
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        self.m_via2_2(paciente)
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constMedicamentos.Exenatide not in paciente.medicamento or md.constMedicamentos.Lixisenatide not in paciente.medicamento:
                        self.m_via2_2(paciente)
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        self.m_via2_2(paciente)
        else:
                self.m_via2_2(paciente)

    def m_via2_2(self, paciente):
        if md.constSubG.SU in paciente.subGrupoMedicamento:
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                self.m_via2_1(paciente)
            else:
                self.m_via2_1(paciente)
        else:
            self.m_via2_1(paciente)

    def m_via2_1(self,paciente):
        if paciente.ultGlicada > 3:
            tratamiento = md.constOrdenes.hba1c
            self.appendTratamiento(paciente, tratamiento)
            if paciente.ultGlicada > 9:
                if md.constGrupo.Insulina in paciente.tipoTto:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
                else:
                    if (constRisks.no_risk_insulinopenia in paciente.prediagnostico[
                        'Prediagnostico'].unique() or paciente.glicemia > 300) or "crisis hiperglicemica" in paciente.antecedente:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                    else:
                        paciente.via=64
            else:
                if (paciente.hba1c / paciente.meta_hba1c) <= 1:
                    paciente.via = 3
                else:
                    paciente.via = 4
        else:
            if (paciente.hba1c / paciente.meta_hba1c) <= 1:
                paciente.via = 3
            else:
                paciente.via = 4

    def m_via3(self, paciente):
        if md.constGrupo.Insulina in paciente.tipoTto:
            tratamiento = 'Considere retirar insulinoterapia si es posible'
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via=64
        else:
            if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
            else:
                paciente.via = 64

    def m_via4(self, paciente):
        if (paciente.hba1c-paciente.meta_hba1c)<1.5:
            paciente.via = 5
        else:
            paciente.via = 6

    def m_via5(self, paciente):
        if paciente.tipoTto==constTipotto.naive:
            paciente.via = 7
        elif paciente.tipoTto==constTipotto.ADOS:
            paciente.via = 8
        elif paciente.tipoTto==constTipotto.aglp1:
            paciente.via = 9
        elif paciente.tipoTto==constTipotto.Insulina:
            paciente.via= 10

    def m_via6(self, paciente):
        if paciente.tipoTto==constTipotto.naive:
            paciente.via = 11
        elif paciente.tipoTto==constTipotto.ADOS:
            paciente.via = 12
        elif paciente.tipoTto==constTipotto.aglp1:
            paciente.via = 13
        elif paciente.tipoTto==constTipotto.Insulina:
            paciente.via= 14

    def m_via7(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 3
        else:
            if paciente.tfg<25:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.tfg>=25 and paciente.tfg<30:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
                #paciente.via = None
            elif paciente.tfg>=30:
                if paciente.tolera_metform==True:
                    if paciente.tfg>=30 and paciente.tfg<45:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                              md.constDosis.Metformina_500,md.constFreq.c12)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 3
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                              md.constDosis.Metformina_1000, md.constFreq.c12)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 3
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3

    def m_via8(self, paciente):
        if paciente.cuantosADO[0]=='1':
            paciente.via = 17
        elif paciente.cuantosADO[0]=='2':
            paciente.via = 18
        elif paciente.cuantosADO[0]=='3':
            paciente.via = 19
        elif paciente.cuantosADO[0]=='4':
            paciente.via = 20

    def m_via9(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via = 32
        elif paciente.tfg>= 25 and paciente.tfg < 30:
            paciente.via = 33
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via = 35
        else:
            paciente.via = 36

    def m_via10(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                paciente.via=41
        elif paciente.tfg >= 25 and paciente.tfg<30:
            if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                paciente.via = 41
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=39
        else:
            paciente.via=40


    def m_via11(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique():
                if paciente.imc>35:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar,md.constMedicamentos.Coformulacion)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
            else:
                if paciente.imc>35:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
        elif paciente.tfg>=25 and paciente.tfg<30:
            if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique():
                if paciente.imc > 35:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.salida = True
        elif paciente.tfg>=30 and paciente.tfg<45:
            paciente.via = 15
        else:
            paciente.via = 16

    def m_via12(self, paciente):
        if paciente.cuantosADO[0]=='1':
            paciente.via = 50
        elif paciente.cuantosADO[0]=='2':
            paciente.via = 51
        elif paciente.cuantosADO[0]=='3':
            paciente.via = 52
        elif paciente.cuantosADO[0]=='4':
            paciente.via = 53


    def m_via13(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.tolera_aGLP1==True:
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
                else:
                    if md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.ajustar,md.constMedicamentos.Semaglutide1,'',md.constFreq.semana)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar,md.constMedicamentos.Semaglutide05,'',md.constFreq.semana)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
            else:
                # md.constSubG.aGLP1 in paciente.subGrupoMedicamento and
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05,'',md.constFreq.semana)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
        elif paciente.tfg>=25 and paciente.tfg<30:
            paciente.via=43
        elif paciente.tfg>=30 and paciente.tfg<45:
            paciente.via=44
        else:
            paciente.via=45

    def m_via14(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via=46
        elif paciente.tfg>=25 and paciente.tfg<30:
            if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                paciente.via = 46
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 46
        elif paciente.tfg>=30 and paciente.tfg<45:
            paciente.via=47
        else:
            paciente.via=48

    def m_via15(self, paciente):
        if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique() or paciente.hba1c>=10:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                self.m_via15_1(paciente)
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                self.m_via15_1(paciente)
        else:
            self.m_via15_1(paciente)

    def m_via15_1(self, paciente):
        if paciente.tolera_metform == True:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_500, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_cardio in paciente.prediagnostico['Prediagnostico'].unique():
                paciente.salida = True
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.salida = True
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
            self.appendTratamiento(paciente, tratamiento)
            paciente.salida = True

    def m_via16(self, paciente):
        if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique() or paciente.hba1c>=10:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                self.m_via16_1(paciente)
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,
                                                      md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                self.m_via16_1(paciente)
        else:
            self.m_via16_1(paciente)

    def m_via16_1(self, paciente):
        if paciente.tolera_metform == True:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_1000, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_cardio in paciente.prediagnostico['Prediagnostico'].unique():
                paciente.salida = True
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.salida = True
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
            self.appendTratamiento(paciente, tratamiento)
            paciente.salida = True

    def m_via17(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                if paciente.cuantosADO=='1A' or paciente.cuantosADO=='1C' or paciente.cuantosADO=='1D':
                    tratamiento = md.constOrdenes.suspenderMedicamento
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=24
                else:
                    paciente.via=23
            else:
                if paciente.cuantosADO=='1A' or paciente.cuantosADO=='1D':
                    tratamiento = md.constOrdenes.suspenderMedicamento
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=24
                elif paciente.cuantosADO=='1C':
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=3
                elif paciente.cuantosADO=='1B':
                    paciente.via=23
        elif paciente.tfg >=25 and paciente.tfg < 30:
            if paciente.cuantosADO=='1A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=21
        else:
            paciente.via=22

    def m_via18(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                if paciente.cuantosADO == '2A':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                elif paciente.cuantosADO == '2B' or paciente.cuantosADO == '2C' or paciente.cuantosADO == '2F':
                    tratamiento = md.constOrdenes.suspenderMedicamento
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 24
                elif paciente.cuantosADO == '2D':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                elif paciente.cuantosADO == '2E':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
            else:
                if paciente.cuantosADO == '2A':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                elif paciente.cuantosADO == '2B':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 24
                elif paciente.cuantosADO == '2C':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 24
                elif paciente.cuantosADO == '2D':
                    paciente.via = 23
                elif paciente.cuantosADO == '2E':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                elif paciente.cuantosADO == '2F':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 24
        elif paciente.tfg >= 25 and paciente.tfg < 30:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 24
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '2D':
                paciente.via = 23
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 24
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via = 25
        else:
            paciente.via = 26

    def m_via19(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                if paciente.cuantosADO == '3A':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
                elif paciente.cuantosADO == '3B':
                    tratamiento = md.constOrdenes.suspenderMedicamento
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=24
                elif paciente.cuantosADO == '3C':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
                elif paciente.cuantosADO == '3D':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
            else:
                if paciente.cuantosADO == '3A':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
                elif paciente.cuantosADO == '3B':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=24
                elif paciente.cuantosADO == '3C':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
                elif paciente.cuantosADO == '3D':
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=23
        elif paciente.tfg>=25 and paciente.tfg<30:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 24
            elif paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via = 27
        elif paciente.tfg >= 45:
            paciente.via = 28

    def m_via20(self, paciente):
        if paciente.tfg<30:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
            self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=23
            else:
                paciente.via = 23
        elif paciente.tfg>=30 and paciente.tfg<45:
            paciente.via=30
        else:
            paciente.via=31

    def m_via21(self,paciente):
        if paciente.tolera_metform==True:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1B' or paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=3
                else:
                    paciente.via=3
        else:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=3
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=3
                else:
                    paciente.via=3


    def m_via22(self,paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '1B' or paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
        else:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3

    def m_via23(self, paciente):
        if paciente.imc>=35:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 3
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 64

    def m_via24(self, paciente):
        if paciente.imc>=35:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 3
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal, md.constDosis.insulina_02)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 64


    def m_via25(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            else:
                paciente.via = 3
        else:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2D':
                paciente.via = 23
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            else:
                paciente.via = 3


    def m_via26(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            else:
                paciente.via = 3
        else:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 3
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2D':
                paciente.via = 23
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 23
                else:
                    paciente.via = 3
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
            if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            else:
                paciente.via = 3

    def m_via27(self, paciente):
        if paciente.tolera_metform==True:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3B' or paciente.cuantosADO == '3C' or paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 29
        else:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3B' or paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 29
            elif paciente.cuantosADO == '3D':
                paciente.via = 23

    def m_via28(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3B' or paciente.cuantosADO == '3C' or paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 29
        else:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
            elif paciente.cuantosADO == '3B' or paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 29
            elif paciente.cuantosADO == '3D':
                paciente.via = 23

    def m_via29(self, paciente):
        if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.cuantosADO== '3B' or paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 24
            elif paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 23
        else:
            if paciente.cuantosADO== '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 3
            elif paciente.cuantosADO == '3D':
                paciente.via = 3

    def m_via30(self, paciente):
        if paciente.tolera_metform==True:
            tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_500, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via=23
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 23

    def m_via31(self, paciente):
        if paciente.tolera_metform == True:
            tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_1000, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 23
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            paciente.via = 23

    def m_via32(self, paciente):
        if paciente.tolera_aGLP1 == False:
            if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
        else:
            if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                if paciente.hba1c > 8:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,
                                                          md.constDosis.insulina_01)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
            elif md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide1, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            else:
                # tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.aGLP1)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Semaglutide1, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42

    def m_via33(self, paciente):
        if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
            paciente.via = 32
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 3

    def m_via34(self, paciente):
            paciente.salida = True

    def m_via35(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via = 32
        else:
            if paciente.tolera_metform == True:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_500, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 33
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_500, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 32
            else:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 33
                else:
                    paciente.via = 33

    def m_via36(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via = 32
        else:
            if paciente.tolera_metform == True:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_1000, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 33
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_1000, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 32
            else:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 33
                else:
                    paciente.via = 33

    def m_via37(self, paciente):
        if paciente.tolera_aGLP1 == False:
            if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
        else:
            if md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide1, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            elif md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64

    def m_via38(self, paciente):
        if md.constSubG.SU in paciente.subGrupoMedicamento:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
            self.appendTratamiento(paciente, tratamiento)
            if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida = True
        else:
            if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
            else:
                if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida = True

    def m_via39(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via = 41
        else:
            if paciente.tolera_metform == True:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_500, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 38
            else:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38
                else:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38

    def m_via40(self, paciente):
        if constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            paciente.via = 41
        else:
            if paciente.tolera_metform == True:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                          md.constDosis.Metformina_1000, md.constFreq.c12)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 38
            else:
                if md.constSubG.Metformina in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38
                else:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        if md.constSubG.SU in paciente.subGrupoMedicamento:
                            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.via = 41
                        else:
                            paciente.via = 41
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 38

    def m_via41(self, paciente):
        if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
            if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 37
            else:
                if paciente.tolera_aGLP1==True:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
        else:
            if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
                paciente.via = 37
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64

    def m_via42(self, paciente):
        if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique() or paciente.hba1c > 10:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal, md.constDosis.insulina_02)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via=64
        else:
            paciente.via=64

    def m_via43(self, paciente):
        if paciente.tolera_aGLP1 == True:
            if md.constSubG.aGLP1 in paciente.subGrupoMedicamento and (md.constMedicamentos.Semaglutide1 not in paciente.medicamento
                                                             or md.constMedicamentos.Semaglutide05 not in paciente.medicamento):

                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        paciente.via=64
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
            else:
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=42
                elif md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide1, '',
                                                          md.constFreq.semana)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        paciente.via = 42
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 42
        else:
            if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05, '',
                                                      md.constFreq.semana)
                self.appendTratamiento(paciente, tratamiento)
                if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                    paciente.via = 42
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42
            else:
                if md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 42
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Semaglutide05,
                                                              '',md.constFreq.semana)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 42
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via = 42

    def m_via44(self, paciente):
        if md.constSubG.Metformina in paciente.subGrupoMedicamento:
            if paciente.tolera_metform==True:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=43
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 43
        else:
            if paciente.tolera_metform==True:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=43
            else:
                paciente.via = 43

    def m_via45(self, paciente):
        if md.constSubG.Metformina in paciente.subGrupoMedicamento:
            if paciente.tolera_metform == True:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 43
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 43
        else:
            if paciente.tolera_metform == True:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 43
            else:
                paciente.via = 43

    def m_via46(self, paciente):
        if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
            if paciente.tolera_aGLP1==True:
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento or md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                    if md.constMedicamentos.Semaglutide05 in paciente.medicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide1,
                                                              '',md.constFreq.semana)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                    else:
                        tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
                else:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.iniciar,md.constMedicamentos.Semaglutide05,
                                                              '', md.constFreq.semana)
                        self.appendTratamiento(paciente, tratamiento)
                        tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.via=64
            else:
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05,
                                                          '', md.constFreq.semana)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
        else:
            if paciente.tolera_aGLP1==True:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 64
            else:
                if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 64


    def m_via47(self, paciente):
        if md.constSubG.Metformina in paciente.subGrupoMedicamento:
            if paciente.tolera_metform==True:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 49
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 49
        else:
            if paciente.tolera_metform == True:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                    paciente.via=46
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
            else:
                paciente.via = 49

    def m_via48(self, paciente):
        if md.constSubG.Metformina in paciente.subGrupoMedicamento:
            if paciente.tolera_metform == True:
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 49
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 49

        else:
            if paciente.tolera_metform == True:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                    paciente.via = 46
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constGrupo.Insulina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=64
            else:
                paciente.via = 49

    def m_via49(self, paciente):
        if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
            paciente.via=46
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 46

    def m_via50(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.cuantosADO == '1A' or paciente.cuantosADO == '1D':
                tratamiento = md.constOrdenes.suspenderMedicamento
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '1C':
                paciente.via=54
            elif paciente.cuantosADO == '1B':
                paciente.via=55
        elif paciente.tfg>=25 and paciente.tfg<30:
            if paciente.cuantosADO == '1A' or paciente.cuantosADO == '1D':
                tratamiento = md.constOrdenes.suspenderMedicamento
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '1C':
                paciente.via=54
            elif paciente.cuantosADO == '1B':
                paciente.via=55
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=56
        else:
            paciente.via = 57

    def m_via51(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B' or paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2D' or paciente.cuantosADO == '2E':
                paciente.via=55
            elif paciente.cuantosADO == '2F':
                paciente.via=54
        elif paciente.tfg>=25 and paciente.tfg<30:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2D':
                paciente.via=55
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2F':
                paciente.via=54
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=58
        else:
            paciente.via = 59
    def m_via52(self, paciente):
        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
            if paciente.cuantosADO == '3A' or paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=55
            elif paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '3D':
                paciente.via = 55
        elif paciente.tfg >= 25 and paciente.tfg < 30:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '3D':
                paciente.via = 55
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=60
        else:
            paciente.via=61

    def m_via53(self, paciente):
        if paciente.tfg<30:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            self.appendTratamiento(paciente, tratamiento)
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 55
        elif paciente.tfg >= 30 and paciente.tfg < 45:
            paciente.via=62
        else:
            paciente.via=63

    def m_via54(self, paciente):
        if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique() or paciente.hba1c>=10:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,
                                                      md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
        else:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,
                                                      md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64

    def m_via55(self, paciente):
        if constRisks.risk_insulinopenia in paciente.prediagnostico['Prediagnostico'].unique() or paciente.hba1c>=10:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constMedicamentos.Coformulacion)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
        else:
            if paciente.imc>=35:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.aGLP1)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64
            else:
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Basal,md.constDosis.insulina_02)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=64

    def m_via56(self, paciente):
        if paciente.tolera_metform==True:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=42
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=42
            elif paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=42
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via=42
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42
        else:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '1C':
                paciente.via = 54
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 54
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42

    def m_via57(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '1C':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42
        else:
            if paciente.cuantosADO == '1A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '1B':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '1C':
                paciente.via = 54
            elif paciente.cuantosADO == '1D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                if constRisks.risk_hipoglicemia in paciente.prediagnostico['Prediagnostico'].unique():
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.SU)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 54
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 42

    def m_via58(self, paciente):
        if paciente.tolera_metform==True:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
        else:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2D':
                paciente.via = 55
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2F':
                paciente.via = 54

    def m_via59(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 42
            elif paciente.cuantosADO == '2F':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
        else:
            if paciente.cuantosADO == '2A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '2C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2D':
                paciente.via = 55
            elif paciente.cuantosADO == '2E':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '2F':
                paciente.via = 54

    def m_via60(self, paciente):
        if paciente.tolera_metform==True:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=55
            elif paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=54
            elif paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=55
            elif paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_500, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=55
        else:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            if paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            if paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            if paciente.cuantosADO == '3D':
                paciente.via = 55

    def m_via61(self, paciente):
        if paciente.tolera_metform == True:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            elif paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            elif paciente.cuantosADO == '3D':
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.Metformina,
                                                      md.constDosis.Metformina_1000, md.constFreq.c12)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
        else:
            if paciente.cuantosADO == '3A':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            if paciente.cuantosADO == '3B':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 54
            if paciente.cuantosADO == '3C':
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via = 55
            if paciente.cuantosADO == '3D':
                paciente.via = 55

    def m_via62(self, paciente):
        if paciente.tolera_metform==True:
            tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_500, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 55
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 55

    def m_via63(self, paciente):
        if paciente.tolera_metform == True:
            tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constSubG.Metformina,
                                                  md.constDosis.Metformina_1000, md.constFreq.c12)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 55
        else:
            tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
            self.appendTratamiento(paciente, tratamiento)
            paciente.via = 55

    def m_via64(self, paciente):
        if md.constSubG.Metformina in paciente.subGrupoMedicamento:
            if paciente.tfg<=30:
                tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                self.appendTratamiento(paciente, tratamiento)
                paciente.via=65
            else:
                if paciente.tolera_metform==True:
                    paciente.via=65
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.Metformina)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.via = 65
        else:
            paciente.via = 65

    def m_via65(self, paciente):
        if md.constSubG.aGLP1 in paciente.subGrupoMedicamento:
            if paciente.tolera_aGLP1==True:
                if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
                    self.appendTratamiento(paciente, tratamiento)
                    paciente.salida=True
                else:
                    paciente.salida = True
            else:
                if md.constMedicamentos.Semaglutide1 in paciente.medicamento:
                    tratamiento = self.recetarTratamiento(md.constAccion.ajustar, md.constMedicamentos.Semaglutide05,
                                                          '',md.constFreq.semana)
                    self.appendTratamiento(paciente, tratamiento)
                    if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                        tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.iDPP4)
                        self.appendTratamiento(paciente, tratamiento)
                        paciente.salida = True
                    else:
                        paciente.salida = True
                else:
                    tratamiento = self.recetarTratamiento(md.constAccion.retirar, md.constSubG.aGLP1)
                    self.appendTratamiento(paciente, tratamiento)
                    if constRisks.risk_cardio in paciente.prediagnostico['Prediagnostico'].unique():
                        if paciente.tfg<25 or constRisks.risk_dialisis in paciente.prediagnostico['Prediagnostico'].unique():
                            if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                                paciente.salida = True
                            else:
                                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                                self.appendTratamiento(paciente, tratamiento)
                                paciente.salida = True
                        else:
                            if md.constSubG.iSGLT2 in paciente.subGrupoMedicamento:
                                if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                                    paciente.salida = True
                                else:
                                    tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                                    self.appendTratamiento(paciente, tratamiento)
                                    paciente.salida = True
                            else:
                                tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iSGLT2)
                                self.appendTratamiento(paciente, tratamiento)
                                paciente.salida = True
                    else:
                        if md.constSubG.iDPP4 in paciente.subGrupoMedicamento:
                            paciente.salida = True
                        else:
                            tratamiento = self.recetarTratamiento(md.constAccion.iniciar, md.constSubG.iDPP4)
                            self.appendTratamiento(paciente, tratamiento)
                            paciente.salida = True
        else:
            paciente.salida = True

    ##Resume el historial
    def appendTratamiento(self,paciente,tratamiento):
        paciente.tratamiento = paciente.tratamiento.append(pd.Series([paciente.via, tratamiento], index=['Via', 'Tratamiento']), ignore_index=True)
        # baseDatos.guardarEvaluacion(self.conn, self.id, 'Via', paciente.via,','.join(paciente.tratamiento['Tratamiento'].astype(str)))
        # baseDatos.guardarEvaluacion(self.conn,self.id,'Via',paciente.via,','.join(paciente.tratamiento['Tratamiento'].astype(str)))
        # baseDatos.guardarEvaluacion(self.conn,self.id,'Via',paciente.via, str('Hola'))
        print(tratamiento)





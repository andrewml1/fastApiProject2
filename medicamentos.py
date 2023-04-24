
class Medicamento:
    def __init__(self,medicamento):
        self.medicamento = medicamento
        self.formula = ''

    ##Metodo para las dosificaciones y acciones
    def recetar(self, accion, dosis='', freq='', titulacion=''):
        formula = Formula(self.medicamento, accion, dosis, freq, titulacion)
        return formula

    def __repr__(self):
        formula = str(self.medicamento)
        return formula

class Formula:
    def __init__(self, medicina, accion, dosis, freq, titulacion):
        self.medicina=medicina
        self.accion = accion
        self.dosis = dosis
        self.freq =freq
        self.titulacion=titulacion

    def toSring(self):
        formula=str(self.accion) + ' '\
                +str(self.medicina) + ' '\
                +str(self.dosis) + ' '\
                +str(self.freq) + ' '\
                +str(self.titulacion)

        return formula.strip()

class constAccion:
    iniciar = 'Iniciar'
    retirar = 'Retirar'
    ajustar = 'Ajustar'

class constDosis:
    insulina_02 = '0.2 u/kg'
    insulina_01 = '0.1 u/kg'
    Metformina_500='500 mg'
    Metformina_1000='1000 mg'

class constFreq:
    c12 = 'cada 12h'
    c24 = 'cada 24h'
    semana = 'cada semana'

class constGrupo:
    ADOS = 'ADOS'
    aGLP1 = 'aGLP1.'
    Insulina = 'Insulina'

class constOrdenes:
    creatinina = 'Realizar orden creatinina'
    hba1c = 'Realizar orden hba1c'
    creatinina_hba1c = 'Realizar orden creatinina y hba1c'
    suspenderMedicamento = 'Suspenda medicamento actual'

class constSubG:
    Metformina = 'Metformina'
    SU = 'SU'
    iSGLT2 = 'iSGLT2.'
    iDPP4 = 'iDPP4.'
    aGLP1 = 'aGLP1.'
    Basal = 'Insulina Basal'
    Prandial = 'Insulina Prandial'

class constMedicamentos:
    Metformina = 'Metformina'
    Glibenclamida = 'Glibenclamida'
    Glimepride = 'Glimepride'
    Empaglifozina = 'Empaglifozina'
    Dapaglifozina = 'Dapaglifozina'
    canaglifozina = 'canaglifozina'
    sotaglifozina = 'sotaglifozina'
    linagliptina = 'linagliptina'
    Vildagliptina = 'Vildagliptina'
    sitagliptina = 'sitagliptina'
    Semaglutide05 = 'Semaglutide 0.5'
    Semaglutide1 = 'Semaglutide 1'
    Liraglutide = 'Liraglutide'
    Exenatide = 'Exenatide'
    Dulaglutide = 'Dulaglutide'
    Lixisenatide = 'Lixisenatide'
    GlarginaU100 = 'Glargina U100'
    GlarginaU300 = 'Glargina U300'
    Degludec = 'Degludec'
    Detemir = 'Detemir'
    NPH = 'NPH'
    Glulisina = 'Glulisina'
    Aspart = 'Aspart'
    Cristalina = 'Cristalina'
    Lispro = 'Lispro'
    Coformulacion='Coformulacion'


class constListas:
    medicamentos = ['Metformina', 'Glibenclamida', 'Glimepiride', 'Empaglifozina', 'Dapaglifozina', 'canaglifozina',
                    'sotaglifozina', 'linagliptina', 'Vildagliptina', 'sitagliptina', 'Semaglutide','Semaglutide1', 'Liraglutide',
                    'Semaglutide0.5', 'Exenatide', 'Dulaglutide', 'Glargina', 'Glargina toujeo', 'Degludec', 'Detemir', 'NPH',
                    'Glulisina', 'Aspart',
                    'Cristalina', 'Lispro']

    antecedentes = ['infarto','iam','enfermedad coronaria','stroke','sv','acv','enfermedad vascular periferica',
'falla cardiaca','icc','eaoc','angina inestable','dialisis','hipoglicemia grave','crisis hiperglicemica','hipoglicemia']
    #Validar con Valen

    grupos= ['ADOS','aGLP1.','Insulina']
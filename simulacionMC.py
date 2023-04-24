import random
import numpy as np
import sqlite3

from scipy.stats import skewnorm

from Pte import Paciente
import baseDatos

class pacienteMC:
    conn = sqlite3.connect('test.db')
    baseDatos.crearTablas(conn)
    #
    # medications = ['Metformina', 'Glibenclamida', 'Glimepiride', 'Empaglifozina', 'Dapaglifozina', 'canaglifozina',
    #                'sotaglifozina', 'linagliptina', 'Vildagliptina', 'sitagliptina', 'Semaglutide', 'Liraglutide',
    #                'Exenatide', 'Dulaglutide', 'Glargina U100', 'Glargina U300', 'Degludec', 'Detemir', 'NPH',
    #                'Glulisina', 'Aspart',
    #                'Cristalina', 'Lispro']

    medications = ['Metformina',
                   'Glibenclamida',
                   'Glimepiride',
                   'Empaglifozina',
                   # 'Dapaglifozina', 'canaglifozina',
                   # 'sotaglifozina',
                   'linagliptina',
                   # 'Vildagliptina', 'sitagliptina',
                   'Semaglutide 1', 'Semaglutide 0.5','Liraglutide']
                   # 'Exenatide',
                   # 'Liraglutide','Dulaglutide', 'Glargina U100',
                   # 'Glulisina', 'Aspart','Cristalina', 'Lispro',
                   # 'Degludec', 'Detemir']

    antecedentes = ['infarto', 'iam',
                    'enfermedad coronaria', 'stroke', 'sv', 'acv', 'enfermedad vascular periferica',
                    'falla cardiaca', 'icc', 'eaoc', 'angina inestable',
                    'hipoglicemia grave', 'crisis hiperglicemica',
                    'dialisis']


    # Generar 1000 datos aleatorios que siguen la distribución
    dataEdad = skewnorm.rvs(1, loc=55, scale=10, size=1000)

    dataIMC = skewnorm.rvs(1, loc=28, scale=6, size=1000)

    dataGlicemia = skewnorm.rvs(1, loc=170, scale=50, size=1000)
    dataGlicemia = dataGlicemia[dataGlicemia > 60]

    dataGlicada = skewnorm.rvs(0, loc=8.5, scale=1, size=1000)
    dataGlicada = dataGlicada[dataGlicada > 5.5]

    def __init__(self):
        self.medications = self.medications
        self.random_medicamentos = random.sample(self.medications,k=random.randint(0,5))
        self.antecedentes=self.antecedentes
        self.random_antecedentes = random.sample(self.antecedentes, k=random.randint(0, 3))
        self.pteSimulado = Paciente(round(np.random.choice(self.dataEdad),1),
                                    round(np.random.choice(self.dataIMC),1),
                                    random.randint(0, 120),
                                    round(np.random.choice(self.dataGlicada),1),
                                    7,
                                    self.random_medicamentos,
                                    self.random_antecedentes,
                                    random.choice([True, False]),
                                    random.choice([True, False]),
                                    round(np.random.choice(self.dataGlicemia),1),
                                    random.randint(0, 10),
                                    random.randint(0, 13),
                                    random.choice([True, False]))
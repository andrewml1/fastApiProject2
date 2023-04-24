import time
import pandas as pd
import openai
import re
from fuzzywuzzy import fuzz
from pymongo.server_api import ServerApi
import medicamentos as md
import numpy as np
import boto3
from pymongo import MongoClient

########################################## NOTAS
#
# ClinicalBERT: Un modelo pre-entrenado basado en la arquitectura BERT que fue entrenado en un corpus médico de
# EHRs para tareas como la identificación de entidades médicas y la clasificación de notas clínicas.
#
# MedBERT: Un modelo de lenguaje basado en BERT diseñado específicamente para el contexto médico, que fue entrenado
# en un corpus de notas clínicas de pacientes.
#
# Biomedical Language Model (BioBERT): Un modelo pre-entrenado basado en BERT que fue entrenado en un corpus médico
# de texto biomédico, como artículos de investigación y patentes.
#
# Clinical Language Understanding (CLU): Un modelo de lenguaje diseñado específicamente para la comprensión de
# lenguaje natural en el contexto médico. Utiliza técnicas de procesamiento de lenguaje natural para extraer
# información de texto clínico no estructurado.
#
# Disease Named Entity Recognition and Normalization (DNorm): Un modelo específico para la identificación de
# entidades médicas en texto no estructurado, como nombres de enfermedades y condiciones médicas.

class constHistoria:
    historia= 'DIAGNÓSTICOS:'+\
'1. Acromegalia, con posible macroadenoma hipofisiario de 10 mm en IRM de 3 Tesla'+\
'Hormona de crecimiento basal: 6.77'+\
'- Postquirurgico de resección tranesfenoidal (15/5/14). Día # 4'+\
'2. HTA'+\
'3. DM secundaria: Hiperglucemia de estres con Hba1c por HPLC en rango de prediabetes, aunque puede tomaba metformina 425 mg  cada día en casa.'+\
'3. Glaucoma'+\
'4. Nodulos tiroideos: ACAF : compatible con tiroiditis linfociticaTiene nausea y sensación de mareo. Se siente mejor de la nausea; presentó episodio de '+\
'hipoglucemia.'+\
'ANÁLISIS DE RESULTADOS'+\
'OBSERVACIONES'+\
'Na.134  K:5.1'+\
'Buena evolución clinica y bioquimica respecto a control de su acromegalia. Incluso han disminuido sus necesidades de insulina.'+\
'PLAN'+\
'- Insulina glargina 6 U SC cada día'+\
'- Suspender insulina glulisina'+\
'- En caso de nueva hipogluemia opor favor sangrar en ese momento para cortisol sérico.'+\
'- Pendiente colonoscopia total.'+\
'ÓRDENES MÉDICAS'+\
'LABORATORIO CLINICO'+\
'27/05/2014 11:46 Cortisol'+\
'sangrar urgent en caso de nuevo episodio de hipoglucemia'+\
'idem'+\
'ORDENADO'+\
'MEDICAMENTOS'+\
'27/05/2014 11:45 Insulina Glargina Lapicero 100UI/mL (Lantus) 6 UNIDADES INTERNACIONALES, SUBCUTANEA, CADA 24 HORAS, por 90 DIAS'


##Mongo DB conexion:
uri = "mongodb+srv://andrewml1:ludacris@cluster0.iwdoxtk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.test
##Crear objeto collection (sobre este es que va a insertar los datos)
collection = db.my_collection

#Fuzzy sin contexto
def fuzzyCompare(health_record,listaMedicamentos,listaGrupos):
    health_record = str(health_record)
    medicines_list = listaMedicamentos ##Mejorar OJO SEMAGLUTIDES
    grupos_list = listaGrupos

    # Extract drugs from health record
    drugs = [word for word in health_record.split()]

    # Match each drug with the list of medicines
    matches = {}
    for drug in drugs:
        for medicine in medicines_list:
            similarity = fuzz.token_set_ratio(drug.lower(), medicine.lower())
            if similarity >= 80:
                if medicine not in matches or similarity > matches[medicine][1]:
                    print(f"{medicine}: '{drug}' (similarity score: {similarity})")
                    matches[medicine] = (drug, similarity)


    for drug in drugs:
        for medicine in grupos_list:
            similarity = fuzz.token_set_ratio(drug.lower(), medicine.lower())
            if similarity >= 80:
                if medicine not in matches or similarity > matches[medicine][1]:
                    print(f"{medicine}: '{drug}' (similarity score: {similarity})")
                    matches[medicine] = (drug, similarity)


    # Print matches
    if len(matches) > 0:
        print(f"Matches found:")
        medicamentos=[]
        for medicine, (drug, similarity) in matches.items():
            # print(f"{medicine}: '{drug}' (similarity score: {similarity})")
            medicamentos.append(medicine)
        print('Lo que encontramos fue: ' + str(medicamentos))
        return medicamentos
    else:
        medicamentos = []
        return medicamentos
        print("No matches found.")



def awsMedicamentos(historia):

    print('------------------------------------------------------------------------------')
    print('-----------------------------MEDICAMENTOS-------------------------------------')
    print('------------------------------------------------------------------------------')

    # Load credentials from environment variables or configuration files
    aws_access_key_id = 'AKIAURMGD5POQMUEBUPG' #os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = '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' #os.environ.get('AWS_SECRET_ACCESS_KEY')


    comprehend = boto3.client('comprehendmedical',region_name='us-west-2',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)

    ##Traductor de la historia y luego ponerla aqui


    # text = "The patient was prescribed ibuprofen for pain relief, " \
    #        "but later switched to aspirin due to stomach. He has an a1c of 8, cr 1.2, ldl 85, " \
    #        "and normal thyroid function. Also, hearth failure" \
    #        "and Metformin intolerance"


    # text="**JORGE ARANGO, 63 AÑOS, CASADO, RESIDENTE EN CONQUISTADORES. *PREVIAMENTE VALORADO EN IPS ESPECIALIZADA DIABETES SAN DIEGO, EN OCTUBRE 2022 CONSULTA ASISTIDA *Raza: mestiza, grupo poblacional general, ocupacion: pensionado, reside en: barrio conquistadores, Teléfono: 3108215081. *DIAGNOSTICOS de: >>>1. Diabetes Mellitus tipo LADA dx a los 30 años Insulinorrequiriente a los 6 meses del diagnostico. Ususario de bomba de insulina hace 8 años MINIMED 640. SIN COMPLICACIONES. OFT 10/2022 >>>2. Dislipidemia. >>>3. Osteoporosis sin fractura: USO DE ALENDRONATO DESDE INICIOS DE 2022. NO TENGO DATOS DE DMO.>>>OTROS ANTECEDENTES: VITILIGO. QUIRÚRGICOS; FX RODILLA POR ACCIDENTE TRÁNSITO, GLÁNDULAS LAGRIMALES. ALÉRGICO: A LA DIPIRONA. TÓXICOS: NO FUMA, LICOR OCASIONAL FAMILIARES: MADRE HTA **TRATAMIENTO FARMACOLOGICO:-INSULINA LISPRO.-Pantoprazol 40 mg dia. --Metformina 850 mg cada 12 horas. --Carvedilol 6,25 mg dia. Atorvastatina 40 mg dia. -AC ascorbico 1 dia. Alendronato 70 mg. -Citrato de calcio. **PARACLINICOS: 03/10/2022: CR 0.9, HBA1C 8.4%, HDL 66, CT 147, TGC 58, LDL CALC 69.4, MICROALBUMINURIA 4 INFORME MINIMED 640 DEL 9/12/2022 AL 22/12/2022: --USO SENSOR 82% ICG 7.36%-EN RANGO 62% ENCIMA RANGO 22% MENOR 250-ENCIMA RANGO 15% MAYOR 250-DEBAJO RANGO 1% ENTRE 54 A 70"

    text=historia

    ###Traductor AWS
    translate = boto3.client('translate',region_name='us-west-2')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode='es',
        TargetLanguageCode='en'
    )

    textoHR=response['TranslatedText']

    ##
    response = comprehend.detect_entities_v2(Text=textoHR)
    collection.insert_one(response)
    print(response)
    medications = []
    for entity in response['Entities']:
        if entity['Category'] == 'MEDICATION': #and entity['Traits'][0]['Name'] != 'AFFIRMATIVE':
            medications.append(entity['Text'])

    # print(medications)
    textoHrESP = str(",".join(medications))
    response = translate.translate_text(
        Text=textoHrESP,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )

    medicamentosEHR=response['TranslatedText'].lower()
    # print(medicamentosEHR)

    fuzzyMedicamentos=fuzzyCompare(medicamentosEHR,md.constListas.medicamentos,md.constListas.grupos)####Nueva, fuzzy
    if len(fuzzyMedicamentos)>0:
        print(fuzzyMedicamentos)


    return fuzzyMedicamentos

# awsMedicamentos(constHistoria.historia)

def awsDiagnostico(historia):

    print('------------------------------------------------------------------------------')
    print('-----------------------------ANTECEDENTES-------------------------------------')
    print('------------------------------------------------------------------------------')

    # Load credentials from environment variables or configuration files
    aws_access_key_id = 'AKIAURMGD5POQMUEBUPG' #os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = '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' #os.environ.get('AWS_SECRET_ACCESS_KEY')


    comprehend = boto3.client('comprehendmedical',region_name='us-west-2',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)

    ##Traductor de la historia y luego ponerla aqui


    # text="**JORGE ARANGO, 63 AÑOS, CASADO, RESIDENTE EN CONQUISTADORES. *PREVIAMENTE VALORADO EN IPS ESPECIALIZADA DIABETES SAN DIEGO, EN OCTUBRE 2022 CONSULTA ASISTIDA *Raza: mestiza, grupo poblacional general, ocupacion: pensionado, reside en: barrio conquistadores, Teléfono: 3108215081. *DIAGNOSTICOS de: >>>1. Diabetes Mellitus tipo LADA dx a los 30 años Insulinorrequiriente a los 6 meses del diagnostico. Ususario de bomba de insulina hace 8 años MINIMED 640. SIN COMPLICACIONES. OFT 10/2022 >>>2. Dislipidemia. >>>3. Osteoporosis sin fractura: USO DE ALENDRONATO DESDE INICIOS DE 2022. NO TENGO DATOS DE DMO.>>>OTROS ANTECEDENTES: VITILIGO. QUIRÚRGICOS; FX RODILLA POR ACCIDENTE TRÁNSITO, GLÁNDULAS LAGRIMALES. ALÉRGICO: A LA DIPIRONA. TÓXICOS: NO FUMA, LICOR OCASIONAL FAMILIARES: MADRE HTA **TRATAMIENTO FARMACOLOGICO:-INSULINA LISPRO.-Pantoprazol 40 mg dia. --Metformina 850 mg cada 12 horas. --Carvedilol 6,25 mg dia. Atorvastatina 40 mg dia. -AC ascorbico 1 dia. Alendronato 70 mg. -Citrato de calcio. **PARACLINICOS: 03/10/2022: CR 0.9, HBA1C 8.4%, HDL 66, CT 147, TGC 58, LDL CALC 69.4, MICROALBUMINURIA 4 INFORME MINIMED 640 DEL 9/12/2022 AL 22/12/2022: --USO SENSOR 82% ICG 7.36%-EN RANGO 62% ENCIMA RANGO 22% MENOR 250-ENCIMA RANGO 15% MAYOR 250-DEBAJO RANGO 1% ENTRE 54 A 70"

    text=historia

    ###Traductor AWS
    translate = boto3.client('translate',region_name='us-west-2')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode='es',
        TargetLanguageCode='en'
    )

    textoHR=response['TranslatedText']

    ##
    response = comprehend.detect_entities_v2(Text=textoHR)
    # print(response)
    medications = []
    for entity in response['Entities']:
        if entity['Category'] == 'MEDICAL_CONDITION': #and entity['Traits'][0]['Name'] != 'AFFIRMATIVE':
            medications.append(entity['Text'])


    # print(medications)
    textoHrESP = str(",".join(medications))
    response = translate.translate_text(
        Text=textoHrESP,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )

    medicamentosEHR=response['TranslatedText'].lower()
    # print(medicamentosEHR)

    fuzzyMedicamentos=fuzzyCompare(medicamentosEHR,md.constListas.antecedentes,md.constListas.grupos)####Nueva, fuzzy
    if len(fuzzyMedicamentos)>0:
        print(fuzzyMedicamentos)
    else:
        print('No encontro antecedentes')

    return fuzzyMedicamentos

# awsDiagnostico(constHistoria.historia)

#
# #Funciono Individual incluso con el de Microsoft
# def clinicalGatorTron():
#
#     # Load the pre-trained GatorTron model and tokenizer
#     model_name = "microsoft/BioGPT-Large-PubMedQA"
#     # model_name = "AshtonIsNotHere/GatorTron-OG"
#     tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
#     model = AutoModelForTokenClassification.from_pretrained(model_name, use_auth_token=True)
#
#     # Define a sample sentence to classify
#     sentence = "The patient was prescribed aspirin for their headache. They are also taking ibuprofen for their back pain."
#
#     # Tokenize the sentence and convert it to input IDs
#     tokens = tokenizer.encode(sentence, add_special_tokens=True)
#     input_ids = torch.tensor([tokens])
#
#     # Use the model to predict the labels for each token in the sentence
#     outputs = model(input_ids)
#     predictions = torch.argmax(outputs.logits, dim=2)
#
#     # Convert the predicted label IDs back to their corresponding labels
#     labels = [tokenizer.decode([label_id]) for label_id in predictions[0].tolist()]
#
#     # Check if any tokens are labeled as drugs other than aspirin
#     other_drugs_mentioned = False
#     for token, label in zip(tokenizer.tokenize(sentence), labels[1:-1]):
#         if label == "B-DRUG" and token != "aspirin":
#             other_drugs_mentioned = True
#
#     if other_drugs_mentioned:
#         print("Another drug was mentioned in the clinical note.")
#     else:
#         print("No other drugs were mentioned in the clinical note.")
#
# #Correrlo
# # clinicalGatorTron()
#
# def similitudGatorTron():
#     from transformers import AutoModelForSequenceClassification, AutoTokenizer
#
#     # Load the pre-trained model and tokenizer
#     model_name = "AshtonIsNotHere/GatorTron-OG"
#     model = AutoModelForSequenceClassification.from_pretrained(model_name, use_auth_token=True, num_labels=1, output_attentions=False,
#                                                                output_hidden_states=False)
#     tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
#
#     # Define the list of drugs and the health record
#     drugs = ['aspirin', 'ibuprofen', 'acetaminophen','metformin']
#     record = "dog"
#
#     # Estimate the similarity between each drug and the health record
#     for drug in drugs:
#         # Tokenize the drug and the health record
#         drug_tokens = tokenizer(drug, padding=True, truncation=True, return_tensors="pt")
#         record_tokens = tokenizer(record, padding=True, truncation=True, return_tensors="pt")
#
#         # Convert the PyTorch tensors to numpy arrays
#         drug_array = drug_tokens['input_ids'].detach().numpy()
#         record_array = record_tokens['input_ids'].detach().numpy()
#
#         # Calculate the cosine similarity
#         similarity_score = cosine_similarity(drug_array.reshape(1, -1), record_array.reshape(1, -1))[0][0]
#
#         # Print the result
#         print(f"The similarity between '{drug}' and '{record}' is {similarity_score:.2f}")
#
# # similitudGatorTron()
#
#
#
# def todosModelos():
#     import transformers
#     import tensorflow as tf
#
#     # Define list of pre-trained models
#     models = [
#         "microsoft/BioGPT-Large-PubMedQA",
#         "AshtonIsNotHere/GatorTron-OG",
#         # 'monologg/biomegatron-bert-345m-uncased',
#         # 'monologg/biobert_v1.1_pubmed',
#         # 'microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext',
#         # 'microsoft/BiomedNLP-DARTS-PMC',
#         # 'allenai/scholar-bert',
#         # 'dmis-lab/biogpt'
#     ]
#
#     # Load tokenizers and models
#     tokenizers = [transformers.AutoTokenizer.from_pretrained(model_name,use_auth_token=True) for model_name in models]
#     models = [tf.keras.models.load_model(model_name) for model_name in models]
#     # model = AutoModelForTokenClassification.from_pretrained(model_name, use_auth_token=True)
#
#     # Input list of terms and target term
#     terms = ['aspirin', 'ibuprofen', 'paracetamol']  # listaMedicamentos
#     target_term = 'metformin'  # health_record
#
#     # Encode target term
#     target_tokens = [tokenizer(target_term, padding=True, truncation=True, return_tensors='tf') for tokenizer in
#                      tokenizers]
#     target_embeddings = [model(target_token)[0][:, 0, :] for model, target_token in zip(models, target_tokens)]
#
#     # Compute similarity scores for each term and model
#     for term in terms:
#         term_tokens = [tokenizer(term, padding=True, truncation=True, return_tensors='tf') for tokenizer in tokenizers]
#         term_embeddings = [model(term_token)[0][:, 0, :] for model, term_token in zip(models, term_tokens)]
#         similarity_scores = [tf.matmul(term_embedding, target_embedding, transpose_b=True) for
#                              term_embedding, target_embedding in zip(term_embeddings, target_embeddings)]
#
#         # Print similarity scores for each term and model
#         for i, model_name in enumerate(models):
#             print(f"{term} - {model_name}: {similarity_scores[i][0][0]}")
#
# # todosModelos()
#
# def clinicalBERTModelo(self):
#     import torch
#     import transformers
#     from sklearn.metrics.pairwise import cosine_similarity
#
#     # load ClinicalBERT model and tokenizer
#     model = transformers.AutoModel.from_pretrained('emilyalsentzer/Bio_ClinicalBERT')
#     tokenizer = transformers.AutoTokenizer.from_pretrained('emilyalsentzer/Bio_ClinicalBERT')
#
#     # define a list of illnesses
#     illnesses = ['hypertension', 'diabetes', 'asthma']
#
#     # define clinical text
#     text = "The patient is a 45-year-old male with a history of hypertension and diabetes. He presents with shortness of breath and wheezing, suggestive of asthma."
#
#     # tokenize text
#     tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
#
#     # run model on tokenized text
#     inputs = tokenizer.encode(text, return_tensors='pt')
#     outputs = model(inputs)[0]
#
#     # extract clinical concepts from model outputs
#     concepts = []
#     for i, token in enumerate(tokens):
#         if outputs[0][i].sum() > 0:  # check if token has a non-zero output
#             concepts.append(token)
#
#     # compute cosine similarity between extracted concepts and illnesses
#     similarity_scores = cosine_similarity([tokenizer.encode(illness) for illness in illnesses],
#                                           [tokenizer.encode(concept) for concept in concepts])
#
#     # print similarity scores
#     print(similarity_scores)
#
#     # Output: [[0.87123579 0.36637684 0.22882777]]
# def preEntrenado():
#     import spacy
#     import numpy as np
#
#     # cargar modelo de word embeddings pre-entrenado
#     nlp = spacy.load('es_core_news_md')
#
#     # texto de ejemplo
#     texto = "El paciente está tomando paracetamol para el dolor de cabeza."
#
#     # lista de medicamentos de ejemplo
#     medicamentos = ["paracetamol", "ibuprofeno", "aspirina"]
#
#     # preprocesamiento de texto
#     doc = nlp(texto)
#     tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
#
#     # representación de texto como vector de word embeddings
#     vector = np.mean([nlp(token).vector for token in tokens], axis=0)
#
#     # calcular similitud coseno entre vector del texto y vector de cada medicamento
#     similitudes = []
#     for medicamento in medicamentos:
#         similitud = np.dot(nlp(medicamento).vector, vector) / (np.linalg.norm(nlp(medicamento).vector) * np.linalg.norm(vector))
#         similitudes.append(similitud)
#
#     # mostrar resultados
#     for i, medicamento in enumerate(medicamentos):
#         print(f"Similitud entre '{texto}' y '{medicamento}': {similitudes[i]}")
#

#################### Method - Medicamentos NLP
def medicamentosNLP(self, paciente):
    df_medicamentos = pd.DataFrame(paciente.medicamento, columns=['Medicamento'])  ##Como llega
    words_df = self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/', 'Medicamentos_DM2.csv')
    resultado = self.similarity_dfs(words_df, 'Medicamento', df_medicamentos, 'Medicamento', 'GPT')
    # results_df = pd.merge(resultado, words_df, on='Medicamento', how='left')
    results_df = resultado.groupby(['word'])['Similarity'].max().reset_index()
    results_df = pd.merge(results_df, resultado, on='Similarity', how='left')  ###Pensarle
    ##Tomar los maximos
    # return results_df


#################### NLP -- Historia Clinica
def procesarHistoria(self, paciente):
    health_records_df = self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/', 'historiaAntecedentes.csv')
    # health_records_df = paciente.antecedente
    words_df = self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/', 'palabrasAntecedentes2.csv')
    resultado = self.similarity_dfs(health_records_df, 'text', words_df, 'word', 'GPT')
    results_df = pd.merge(resultado, words_df, on='word', how='left')
    ##Tomar los maximos
    # return results_df


# def procesarMedicamentos(self, paciente):
#################### NLP -- antecedentes con nuestras enfermedades
## No lo estamos teniendo en cuenta ya que eso es lo que hacemos con GPT
# df_antecedentes = pd.DataFrame(paciente.antecedente, columns=['word'])
# words_df = self.readFile('C:/Users/Andres Lo/Documents/Personales/Salud/', 'palabrasAntecedentes2.csv')
# resultado = self.similarity_dfs(words_df, 'word', df_antecedentes, 'word')
# results_df = pd.merge(resultado, words_df, on='word', how='left')

def calculate_similarity(self, health_record, word):
    model_engine = "text-davinci-002"
    # model_engine = "text-9" ##Med-Pub
    openai.api_key = "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"  ##Key de OpenAI
    prompt = f"Estimate the similarity score (between 0 and 1) of the health record '{health_record}' and the word '{word}'"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    similarity = response.choices[0].text
    # Si por alguna razon que no calcula el score
    try:
        similarity = re.findall("\d+\.\d+|\d+\.|\d+|\n\n\d+", similarity)[0]
    except IndexError:
        similarity = 0

    if similarity[0] == 1:
        similarity = similarity[0]

    return float(similarity)


def similarity_dfs(self, health_records_df, header1, words_df, header2, technique):
    # Loop through each health record and each word in the dataframe and calculate the similarity between them

    results = []
    for _, row in health_records_df.iterrows():
        if technique == 'GPT' and (health_records_df.shape[0] * words_df.shape[0]) > 60:
            time.sleep(1)  # Avoid any issue with the OpenAI API
        health_record = row[header1]
        for _, word_row in words_df.iterrows():
            word = word_row[header2]
            if technique == 'GPT':
                similarity_threshold = 0.0
                similarity = self.calculate_similarity(health_record, word)
                if similarity >= similarity_threshold:
                    results.append((health_record, word, similarity))
            else:
                similarity_threshold = 0.0
                similarity = self.levenshtein_similarity(health_record, word)
                if similarity >= similarity_threshold:
                    results.append((health_record, word, similarity))

        # Store the results in a new dataframe
    results_df = pd.DataFrame(results, columns=['Health Record', 'word', 'Similarity'])
    return results_df

#No tienen en cuenta contexto





##Jaccard similarity
def jaccard_similarity(self, word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def levenshtein_similarity(self, str1, str2):
    m = len(str1)
    n = len(str2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return 1 - dp[m][n] / max(m, n)
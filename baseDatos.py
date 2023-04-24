
import pandas as pd


def alterarTablas(conn, alterar=False):
    if alterar == True:
        conn.execute('''ALTER TABLE `evaluaciones`
               ADD  `timeInicio` DATETIME;''')


def crearTablas(conn):
    cursor = conn.cursor()
    table_name = 'paciente'
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()

    if result == None:
        ##Si ya esta creada no la cree
        conn.execute('''CREATE TABLE `paciente` (
        `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `edad` INTEGER,
        `imc` INTEGER,
        `tfg` INTEGER,
        `hba1c` INTEGER,
        `meta_hba1c` INTEGER,
        `medicamento` TEXT,
        `antecedente` TEXT,
        `tolera_metform` TEXT,
        `hipos` TEXT,
        `glicemia` INTEGER,
        `ultGlicada` INTEGER,
        `ultCreatinina` INTEGER,
        `tolera_aGLP1` INTEGER,
        `cuantosADO` TEXT,
        `subGrupoMedicamento` TEXT,
        `timeInicio` DATETIME

);''')

    cursor = conn.cursor()
    table_name = 'evaluaciones'
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()

    if result == None:
        ##Si ya esta creada no la cree
        conn.execute('''CREATE TABLE `evaluaciones` (
          `ID` INTEGER,
          `Tipo` LONGTEXT(10000),
          `Via` INT(20),
          `Evaluacion` LONGTEXT(10000),
          `timeInicio` DATETIME,
          FOREIGN KEY (`ID`) REFERENCES `paciente` (`ID`)
        );''')


def crearTablaMedicamentos(conn):
    cursor = conn.cursor()
    table_name = 'Grupos'
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()

    if result == None:
        ##Si ya esta creada no la cree
        conn.execute('''CREATE TABLE Grupos (
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
            Grupos TEXT,
            Subgrupos TEXT
        );''')

    cursor = conn.cursor()
    table_name = 'Subgrupos'
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    ##Subgrupos
    if result == None:
        ##Si ya esta creada no la cree
        conn.execute('''CREATE TABLE Subgrupos (
        `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        Grupos TEXT,
        Subgrupos TEXT,
        FOREIGN KEY (Grupos) REFERENCES Grupos(`ID`)
    );''')

        cursor = conn.cursor()
        table_name = 'Medicamento'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()

        ##Medicamentos
        if result == None:
            ##Si ya esta creada no la cree
            conn.execute('''CREATE TABLE Medicamento (
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
              Grupos TEXT,
              Subgrupos TEXT,
              Medicamento TEXT,
              FOREIGN KEY (Grupos, Subgrupos) REFERENCES Subgrupos(Grupos, Subgrupos));
            ''')

    conn.commit()

    llenarTablaMedicamentos(conn)


def llenarTablaMedicamentos(conn):
    ruta = 'C:/Users/Andres Lo/Documents/Personales/Salud/Medicamentos_DM2.csv'

    df = pd.read_csv(ruta)
    dfGrupo = df['Grupos'].unique()
    dfGrupo = pd.DataFrame({'Grupos': dfGrupo})
    dfGrupo.to_sql('Grupos', conn, if_exists='replace', index=False)

    dfSubGrupo = df[['Grupos', 'Subgrupos']].drop_duplicates()
    dfSubGrupo.to_sql('Subgrupos', conn, if_exists='replace', index=False)

    # Medicamentos
    df.to_sql('Medicamento', conn, if_exists='replace', index=False)


def obtenerIdentif(conn):
    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID) FROM paciente")

    # Fetch the result
    max_id = cursor.fetchone()[0]

    # If there are no rows in the `paciente` table yet, set the max_id to 0
    if max_id is None:
        max_id = 0

    # Increment the max_id to get the next available ID for the `evaluaciones` table
    new_id = max_id

    # Close the cursor and the database connection
    cursor.close()
    return new_id


##La identificacion saldra del autoincremental de la base de datos


def guardarPaciente(conn, edad, imc,tfg, hba1c, meta_hba1c, medicamento, antecedente,
                    tolera_metform, hipos,glicemia,ultGlicada,ultCreatinina,tolera_aGLP1,cuantosADO,subGrupoMedicamento,timeInicio):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `paciente` (`edad`,`imc`,`tfg`, `hba1c`, `meta_hba1c`, `medicamento`, `antecedente`, `tolera_metform`, `hipos`,`glicemia`,`ultGlicada`,`ultCreatinina`,`tolera_aGLP1`,`cuantosADO`,`subGrupoMedicamento`,`timeInicio`) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?)", \
                    (edad, imc,tfg, hba1c, meta_hba1c, medicamento, antecedente, tolera_metform, hipos,glicemia,ultGlicada,ultCreatinina,tolera_aGLP1,cuantosADO,subGrupoMedicamento,timeInicio));
    conn.commit()


def guardarEvaluacion(conn, identif, Tipo, Via, Evaluacion,timeInicio):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `evaluaciones` (`ID`, `Tipo`, `Via`, `Evaluacion`,`timeInicio`)"  "VALUES (?, ?, ?, ?,?)", \
                   (identif, Tipo, Via, Evaluacion,timeInicio));
    conn.commit()

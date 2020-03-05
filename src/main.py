# Python script to start database
import MySQLdb

# Connection and cursor
db = MySQLdb.connect(host="localhost", user="bdprojeto", passwd="password")
db_cursor = db.cursor()

# Create database
db_cursor.execute("CREATE DATABASE IF NOT EXISTS bd_projeto;")
db_cursor.execute("USE bd_projeto;")

#####################
### Create tables ###
#####################

# Main Team Table

query = """
        CREATE TABLE IF NOT EXISTS Equipe (\
            nome_equipe VARCHAR(30) NOT NULL,\
            curso VARCHAR(40) NOT NULL,\
            CONSTRAINT pk_equipe PRIMARY KEY (nome_equipe)\
        );
        """
db_cursor.execute(query)

# Member Related-Tables

query = """
        CREATE TABLE IF NOT EXISTS Membros_equipe (\
            mat_int CHAR(9) NOT NULL,\
            nome_equipe VARCHAR(30) NOT NULL,\
            CONSTRAINT pk_membros PRIMARY KEY (mat_int, nome_equipe),\
            CONSTRAINT fk_membros_equipe FOREIGN KEY (nome_equipe) REFERENCES Equipe (nome_equipe) ON DELETE CASCADE\
        );
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Integrante (\
            matricula CHAR(9) NOT NULL,\
            nome_int VARCHAR(100) NOT NULL,\
            CONSTRAINT pk_int PRIMARY KEY (matricula, nome_int),\
            CONSTRAINT fk_int FOREIGN KEY (matricula) REFERENCES Membros_equipe (mat_int) ON DELETE CASCADE\
        );
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Int_emails (\
            matricula CHAR(9) NOT NULL,\
            email VARCHAR(50) NOT NULL,\
            CONSTRAINT pk_int_email PRIMARY KEY (matricula, email),\
            CONSTRAINT fk_int_email FOREIGN KEY (matricula) REFERENCES Integrante (matricula) ON DELETE CASCADE\
        );
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Int_tels (\
            matricula CHAR(9) NOT NULL,\
            telefone VARCHAR(15) NOT NULL,\
            CONSTRAINT pk_int_tel PRIMARY KEY (matricula, telefone),\
            CONSTRAINT fk_int_tel FOREIGN KEY (matricula) REFERENCES Integrante (matricula) ON DELETE CASCADE\
        );
        """
db_cursor.execute(query)

# Competition event table
query = """
        CREATE TABLE IF NOT EXISTS Competicao (\
            nome_comp VARCHAR(40) NOT NULL,\
            data DATE NOT NULL,\
            local CHAR(30),\
            nome_equipe VARCHAR(30) NOT NULL,\
            CONSTRAINT unique_comp UNIQUE (nome_comp, data),\
            CONSTRAINT pk_comp PRIMARY KEY (nome_comp, data, nome_equipe),\
            CONSTRAINT fk_comp_equipe FOREIGN KEY (nome_equipe) REFERENCES Equipe (nome_equipe) ON DELETE CASCADE\
        );
        """
db_cursor.execute(query)

# Projects tables
query = """
        CREATE TABLE IF NOT EXISTS Projeto (\
            id_proj INT NOT NULL AUTO_INCREMENT,\
            titulo TEXT NOT NULL,\
            descricao TEXT NOT NULL,\
            nome_comp VARCHAR(40) NOT NULL,\
            data_comp DATE NOT NULL,\
            CONSTRAINT pk_projeto PRIMARY KEY (id_proj, nome_comp, data_comp),\
            CONSTRAINT fk_projeto_comp FOREIGN KEY (nome_comp, data_comp) REFERENCES Competicao (nome_comp, data) ON DELETE NO ACTION\
        )
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Proj_links (\
            id_proj INT NOT NULL,\
            link VARCHAR(255) NOT NULL,\
            CONSTRAINT pk_link PRIMARY KEY (id_proj, link),\
            CONSTRAINT fk_link FOREIGN KEY (id_proj) REFERENCES Projeto (id_proj) ON DELETE CASCADE\
        )
        """
db_cursor.execute(query)

# Contributors to project
query = """
        CREATE TABLE IF NOT EXISTS Integrantes_proj (\
            id_proj INT NOT NULL,\
            matricula CHAR(9) NOT NULL,\
            CONSTRAINT pk_int_proj PRIMARY KEY (id_proj, matricula),\
            CONSTRAINT fk_ip_proj FOREIGN KEY (id_proj) REFERENCES Projeto (id_proj) ON DELETE CASCADE,\
            CONSTRAINT fk_ip_int FOREIGN KEY (matricula) REFERENCES Integrante (matricula) ON DELETE NO ACTION\
        )
        """
db_cursor.execute(query)

# Knowledge area tables
query = """
        CREATE TABLE IF NOT EXISTS Conhecimento (\
            id_con INT NOT NULL AUTO_INCREMENT,\
            nome VARCHAR(40) NOT NULL,\
            area VARCHAR(8) NOT NULL,\
            CONSTRAINT ck_area CHECK (area in ('Mecanica', 'Controle', 'Software', 'Eletrica', 'Gestao')),\
            CONSTRAINT pk_area PRIMARY KEY (id_con)\
        )
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Proj_conhecimento (\
            id_proj INT NOT NULL,\
            id_con INT NOT NULL,\
            nivel TINYINT UNSIGNED NOT NULL,\
            CONSTRAINT pk_proj_con PRIMARY KEY (id_proj, id_con),\
            CONSTRAINT fk_pc_proj FOREIGN KEY (id_proj) REFERENCES Projeto (id_proj) ON DELETE CASCADE,\
            CONSTRAINT fk_pc_con FOREIGN KEY (id_con) REFERENCES Conhecimento (id_con) ON DELETE CASCADE\
        )
        """
db_cursor.execute(query)

query = """
        CREATE TABLE IF NOT EXISTS Integrantes_conhecimento (\
            matricula CHAR(9) NOT NULL,\
            id_con INT NOT NULL,\
            nivel TINYINT UNSIGNED NOT NULL,\
            CONSTRAINT pk_int_con PRIMARY KEY (matricula, id_con),\
            CONSTRAINT fk_ic_int FOREIGN KEY (matricula) REFERENCES Integrante (matricula) ON DELETE CASCADE,\
            CONSTRAINT fk_ic_con FOREIGN KEY (id_con) REFERENCES Conhecimento (id_con) ON DELETE CASCADE\
        )
        """
db_cursor.execute(query)

print(db)
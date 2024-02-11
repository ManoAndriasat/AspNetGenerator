import psycopg2

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def se_connecter(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except psycopg2.Error as e:
            print(f"Erreur de connexion à la base de données : {e}")
            return None

    def obtenir_tables(self, connection):
        tables = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' and table_schema = 'public'")
                tables = [table[0] for table in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des tables : {e}")
        return tables

    def obtenir_vues(self, connection):
        vues = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.views WHERE table_schema='public'")
                vues = [vue[0] for vue in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des vues : {e}")
        return vues

    def obtenir_infos_table(self, connection, table_name):
        infos_table = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
                columns = cursor.fetchall()
                infos_table[table_name] = columns
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des informations de la table {table_name} : {e}")
        return infos_table

    def PK(self, connection, table_name):
        colonne_primaire = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = %s AND column_name IN (
                        SELECT column_name
                        FROM information_schema.table_constraints
                        JOIN information_schema.constraint_column_usage
                        USING (constraint_name, table_schema, table_name)
                        WHERE constraint_type = 'PRIMARY KEY' AND table_name = %s
                    )
                    """,
                    (table_name, table_name)
                )
                colonne_primaire = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération de la clé primaire de la table {table_name} : {e}")
        return colonne_primaire

    def FK(self, connection, table_name):
        cles_etrangeres = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name
			FROM information_schema.columns
			WHERE table_name = %s AND column_name IN (
			    SELECT column_name
			    FROM information_schema.table_constraints
			    JOIN information_schema.key_column_usage
			    USING (constraint_name, table_schema, table_name)
			    WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
                    )
                    """,
                    (table_name, table_name)
                )
                cles_etrangeres = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des clés étrangères de la table {table_name} : {e}")
        return cles_etrangeres


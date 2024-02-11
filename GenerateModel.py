import os

class GenerateModel:
    def __init__(self, database_instance, template_file="Template/Model.template"):
        self.database_instance = database_instance
        self.template_file = template_file

    def load_template(self):
        with open(self.template_file, "r") as template_file:
            return template_file.read()

    def capitalize_first_letter(self, input_string):
        if input_string:
            return input_string[0].upper() + input_string[1:]
        else:
            return input_string

    def generate_csharp_model(self, table_name):
        connection = self.database_instance.se_connecter()
        columns = self.database_instance.obtenir_infos_table(connection, table_name)
        PK_result = self.database_instance.PK(connection, table_name)

        if PK_result is not None and len(PK_result) > 0:
            PK = PK_result[0]
        else:
            PK = "NONE"

        model_template = self.load_template()

        replacement_dict = {
            '{namespace}': "Models",
            '{PK}': PK,
            '{class}': self.capitalize_first_letter(table_name),
            '{class_name}': table_name,
            '{properties}': self.generate_properties(columns[table_name]),
            '{constructor_parameters}': self.generate_constructors_parameters(columns[table_name]),
            '{constructor_assignments}': self.generate_constructors_assignments(columns[table_name]),
            '{insert_assignments}': self.generate_insert_assignments(columns[table_name])
        }

        for placeholder, value in replacement_dict.items():
            model_template = model_template.replace(placeholder, value)

        return model_template

    def generate_properties(self, columns):
        properties = ""
        for column_name, data_type in columns:
            properties += f"\tpublic {self.map_type(data_type)} {column_name} {{ get; set; }}\n"
        return properties

    def generate_constructors_parameters(self, columns):
        constructor_parameters = ""
        for column_name, data_type in columns:
            constructor_parameters += f"{self.map_type(data_type)} {column_name.lower()}, "
        return constructor_parameters.rstrip(", ")  # Supprimer la virgule finale

    def generate_constructors_assignments(self, columns):
        constructor_assignments = ""
        for column_name, data_type in columns:
            constructor_assignments += f"\t\tthis.{column_name} = {column_name.lower()};\n"
        return constructor_assignments

    def generate_insert_assignments(self, columns):
        insert_assignments = ""
        for column_name, data_type in columns:
            insert_assignments += f'\t\t{{"{column_name}", this.{column_name}}},\n'
        return insert_assignments

    def generate_and_save_models(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)

        connection = self.database_instance.se_connecter()

        if connection:
            tables = self.database_instance.obtenir_tables(connection)

            for table_name in tables:
                model_code = self.generate_csharp_model(table_name)
                table_name = self.capitalize_first_letter(table_name)  # Ajout de "self."
                file_path = os.path.join(output_directory, f"{table_name}.cs")
                with open(file_path, "w") as file:
                    file.write(model_code)

            print(f"Les classes C# ont été générées et enregistrées dans le répertoire {output_directory}")

    @staticmethod
    def map_type(postgres_type):
        type_mapping = {
            "integer": "int",
            "character varying": "string",
            "timestamp without time zone": "DateTime",
        }

        return type_mapping.get(postgres_type, "object")


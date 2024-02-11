import os

class GenerateController:
    def __init__(self, database_instance, template_file="Template/Controller.template"):
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


    def generate_csharp_controller(self, table_name):
        connection = self.database_instance.se_connecter()
        columns = self.database_instance.obtenir_infos_table(connection, table_name)
        PK_result = self.database_instance.PK(connection, table_name)
        FK_result = self.database_instance.FK(connection, table_name)

        if FK_result is not None:
            fk_select = self.generate_fk_select(FK_result)
        else:
            fk_select = ""
            
        if PK_result is not None and len(PK_result) > 0:
            PK = PK_result[0]
            next_value = f'string {PK} = DatabaseHelper.GetNextId(connection, "{PK}", "{table_name.upper()}");\n'
        else:
            PK = "NONE"
            next_value = ""

        columns_without_pk = [col for col in columns[table_name] if col[0] != PK]

        controller_template = self.load_template()

        replacement_dict = {
            '{next_value}': next_value,
            '{PK}': PK,
            '{fk_select}': fk_select,
            '{namespace}': "Controller",
            '{abreviation}': table_name.upper(),
            '{class}': self.capitalize_first_letter(table_name),
            '{class_name}': table_name,
            '{insert_parameters}': self.generate_insert_parameters(columns_without_pk),
            '{constructor_parameters}': self.generate_constructor_parameters(columns[table_name])
        }

        for placeholder, value in replacement_dict.items():
            controller_template = controller_template.replace(placeholder, value)

        return controller_template
        
    def generate_fk_select(self, columns):
        constructor_parameters = ""
        for column_name in columns:
            constructor_parameters += f"ViewBag.List{self.capitalize_first_letter(column_name[0][3:])} = {self.capitalize_first_letter(column_name[0][3:])}.SelectAll;\n"
        return constructor_parameters
        
    def generate_insert_parameters(self, columns):
        constructor_parameters = ""
        for column_name, data_type in columns:
            constructor_parameters += f"{self.map_type(data_type)} {column_name.lower()}, "
        return constructor_parameters.rstrip(", ")


    def generate_constructor_parameters(self, columns):
        constructor_parameters = ""
        for column_name, data_type in columns:
            constructor_parameters += f"{column_name.lower()}, "
        return constructor_parameters.rstrip(", ")


    def generate_and_save_controllers(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)

        connection = self.database_instance.se_connecter()

        if connection:
            tables = self.database_instance.obtenir_tables(connection)

            for table_name in tables:
                controller_code = self.generate_csharp_controller(table_name)

                file_path = os.path.join(output_directory, f"{self.capitalize_first_letter(table_name)}Controller.cs")
                with open(file_path, "w") as file:
                    file.write(controller_code)

            print(f"Les controllers C# ont été générés et enregistrés dans le répertoire {output_directory}")

    @staticmethod
    def map_type(postgres_type):
        type_mapping = {
            "integer": "int",
            "character varying": "string",
            "timestamp without time zone": "DateTime",
        }

        return type_mapping.get(postgres_type, "object")
        
        
 


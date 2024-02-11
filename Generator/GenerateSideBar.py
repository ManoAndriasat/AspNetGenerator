import os

class GenerateSideBar:
    def __init__(self, database_instance, template_file="Template/SideBar.template", style_file="Template/Assets/SideBar.template"):
        self.database_instance = database_instance
        self.template_file = template_file
        self.style_file = style_file

    def load_template(self, template):
        with open(template, "r", encoding="utf-8") as template_file:
            return template_file.read()

    @staticmethod
    def capitalize_first_letter(input_string):
        if input_string:
            return input_string[0].upper() + input_string[1:]
        else:
            return input_string

    def generate_Liste(self, columns):
        properties = ""
        for column_name in columns:
            properties += f'<li data-toggle="collapse" data-target="#{column_name}" class="collapsed">\n' \
                        + f'\t<a href="#"> {self.capitalize_first_letter(column_name)} <span class="arrow"></span></a>\n' \
                        + f'</li>\n' \
                        + f'<ul class="sub-menu collapse" id="{column_name}">\n' \
                        + f'\t<li><a href="View{self.capitalize_first_letter(column_name)}.jsp">View</a></li>\n' \
                        + f'\t<li><a href="Insert{self.capitalize_first_letter(column_name)}.jsp">Insert</a></li>\n' \
                        + f'</ul>\n\n'
            print(column_name)
        return properties

    def generate_side_bar(self):
        connection = self.database_instance.se_connecter()
        model_template = self.load_template(self.template_file)
        connection = self.database_instance.se_connecter()

        if connection:
            tables = self.database_instance.obtenir_tables(connection)

        replacement_dict = {
            '{List}' : self.generate_Liste(tables)
        }

        for placeholder, value in replacement_dict.items():
            model_template = model_template.replace(placeholder, value)

        return model_template

    def generate_style(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        style_code = self.load_template(self.style_file)
        file_path = os.path.join(output_directory, "SideBar.css")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(style_code)

    def generate_and_save_SideBar(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        self.generate_style(output_directory)
        connection = self.database_instance.se_connecter()

        model_code = self.generate_side_bar()
        file_path = os.path.join(output_directory, "SideBar.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(model_code)

        print(f"La sidebar a été générée et enregistrée dans le répertoire {output_directory}")

    @staticmethod
    def map_type(postgres_type):
        type_mapping = {
            "integer": "int",
            "character varying": "string",
            "timestamp without time zone": "DateTime",
        }
        return type_mapping.get(postgres_type, "object")

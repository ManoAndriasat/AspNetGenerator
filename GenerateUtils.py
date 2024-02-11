import os

class GenerateUtils:
    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.template_file1 = "Template/Utils/Connection.template"
        self.template_file2 = "Template/Utils/DatabaseHelper.template"

    def load_template(self, template_file):
        with open(template_file, "r") as template_file:
            return template_file.read()

    def generate_csharp_connection(self):
        connection_template = self.load_template(self.template_file1)

        replacement_dict = {
            '{host}': self.host,
            '{database}': self.database,
            '{username}': self.username,
            '{password}': self.password,
        }

        for placeholder, value in replacement_dict.items():
            connection_template = connection_template.replace(placeholder, value)

        return connection_template

    def generate_csharp_database_helper(self):
        database_helper_template = self.load_template(self.template_file2)
        return database_helper_template

    def generate_and_save_connection(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)

        connection_code = self.generate_csharp_connection()
        file_path = os.path.join(output_directory, "Connection.cs")

        with open(file_path, "w") as file:
            file.write(connection_code)

    def generate_and_save_database_helper(self, output_directory):
        os.makedirs(output_directory, exist_ok=True)

        database_helper_code = self.generate_csharp_database_helper()
        file_path = os.path.join(output_directory, "DatabaseHelper.cs")

        with open(file_path, "w") as file:
            file.write(database_helper_code)

    def generate_and_save(self, output_directory):
        self.generate_and_save_connection(output_directory)
        self.generate_and_save_database_helper(output_directory)


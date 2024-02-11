from GenerateModel import GenerateModel
from GenerateController import GenerateController
from GenerateUtils import GenerateUtils
from Database import Database

def main():
    host = "localhost"
    database = "emp"
    user = "postgres"
    password = "Mano-123"

    db_instance = Database(host=host, database=database, user=user, password=password)
    model_generator = GenerateModel(database_instance=db_instance)
    model_generator.generate_and_save_models("/home/mano/Desktop/Employe/Models")
    
    controller_generator = GenerateController(database_instance=db_instance)
    controller_generator.generate_and_save_controllers("/home/mano/Desktop/Employe/Controllers")
    
    generator = GenerateUtils(host, database, user, password)
    generator.generate_and_save("/home/mano/Desktop/Employe/Models/Utils")


if __name__ == "__main__":
    main()


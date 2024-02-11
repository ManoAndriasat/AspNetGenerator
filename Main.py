import os
import subprocess

from Generator.GenerateModel import GenerateModel
from Generator.GenerateController import GenerateController
from Generator.GenerateUtils import GenerateUtils
from Generator.GenerateSideBar import GenerateSideBar
from Database.Database import Database

def main():
    host = "localhost"
    database = "meuble"
    user = "postgres"
    password = "Mano-123"

    if not os.path.exists(database):
        subprocess.run(f"dotnet new mvc -n {database}", shell=True, check=True)
        os.chdir(database)
        subprocess.run("dotnet add package npgsql", shell=True, check=True)
        os.chdir("..")  

    db_instance = Database(host=host, database=database, user=user, password=password)

    model_generator = GenerateModel(database_instance=db_instance)
    model_generator.generate_and_save_models(f"{database}/Models")
    
    controller_generator = GenerateController(database_instance=db_instance)
    controller_generator.generate_and_save_controllers(f"{database}/Controllers")
    
    utils_generator = GenerateUtils(host, database, user, password) 
    utils_generator.generate_and_save(f"{database}/Models/Utils")

    side_bar_generator = GenerateSideBar(database_instance=db_instance) 
    side_bar_generator.generate_and_save_SideBar(f"{database}/Views/Shared")

if __name__ == "__main__":
    main()

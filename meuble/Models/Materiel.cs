using System;
using System.Collections.Generic;
using Npgsql;
using Utils.helper;

namespace Models
{
    public class Materiel
    {
	public string id_materiel { get; set; }
	public string nom { get; set; }

        public Materiel()
        {
        }

        public Materiel(string id_materiel, string nom)
        {
		this.id_materiel = id_materiel;
		this.nom = nom;

	}
	
	public void Insert(NpgsqlConnection connection){
            Dictionary<string, object> data = new Dictionary<string, object>
            {
		{"id_materiel", this.id_materiel},
		{"nom", this.nom},

            };
            DatabaseHelper.Insert(connection, "materiel" , data);
        }
        
	public static List<Materiel> SelectAll(NpgsqlConnection connection){
            return DatabaseHelper.Select<Materiel>(connection, "materiel");
        }

        public static Materiel SelectById(NpgsqlConnection connection, string NONE)
        {
            Dictionary<string, object> data = new Dictionary<string, object>
            {
                { "NONE", NONE }
            };
            List<Materiel> result = DatabaseHelper.Select<Materiel>(connection, "materiel", data);
            return result.FirstOrDefault();
        }
    }
}


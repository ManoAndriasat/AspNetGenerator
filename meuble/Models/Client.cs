using System;
using System.Collections.Generic;
using Npgsql;
using Utils.helper;

namespace Models
{
    public class Client
    {
	public string id_client { get; set; }
	public string nom { get; set; }
	public object date_naissance { get; set; }
	public int sexe { get; set; }

        public Client()
        {
        }

        public Client(string id_client, string nom, object date_naissance, int sexe)
        {
		this.id_client = id_client;
		this.nom = nom;
		this.date_naissance = date_naissance;
		this.sexe = sexe;

	}
	
	public void Insert(NpgsqlConnection connection){
            Dictionary<string, object> data = new Dictionary<string, object>
            {
		{"id_client", this.id_client},
		{"nom", this.nom},
		{"date_naissance", this.date_naissance},
		{"sexe", this.sexe},

            };
            DatabaseHelper.Insert(connection, "client" , data);
        }
        
	public static List<Client> SelectAll(NpgsqlConnection connection){
            return DatabaseHelper.Select<Client>(connection, "client");
        }

        public static Client SelectById(NpgsqlConnection connection, string NONE)
        {
            Dictionary<string, object> data = new Dictionary<string, object>
            {
                { "NONE", NONE }
            };
            List<Client> result = DatabaseHelper.Select<Client>(connection, "client", data);
            return result.FirstOrDefault();
        }
    }
}


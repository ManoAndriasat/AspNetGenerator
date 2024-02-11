using System;
using System.Collections.Generic;
using Npgsql;
using Utils.helper;

namespace Models
{
    public class Style
    {
	public string id_style { get; set; }
	public string nom { get; set; }

        public Style()
        {
        }

        public Style(string id_style, string nom)
        {
		this.id_style = id_style;
		this.nom = nom;

	}
	
	public void Insert(NpgsqlConnection connection){
            Dictionary<string, object> data = new Dictionary<string, object>
            {
		{"id_style", this.id_style},
		{"nom", this.nom},

            };
            DatabaseHelper.Insert(connection, "style" , data);
        }
        
	public static List<Style> SelectAll(NpgsqlConnection connection){
            return DatabaseHelper.Select<Style>(connection, "style");
        }

        public static Style SelectById(NpgsqlConnection connection, string NONE)
        {
            Dictionary<string, object> data = new Dictionary<string, object>
            {
                { "NONE", NONE }
            };
            List<Style> result = DatabaseHelper.Select<Style>(connection, "style", data);
            return result.FirstOrDefault();
        }
    }
}


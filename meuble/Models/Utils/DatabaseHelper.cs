using System;
using System.Collections.Generic;
using Npgsql;

namespace Utils.helper
{
    public class DatabaseHelper
    {
        public static void Insert(NpgsqlConnection conn, string tableName, Dictionary<string, object> data)
        {
            using (NpgsqlCommand cmd = new NpgsqlCommand())
            {
                cmd.Connection = conn;
                string columns = string.Join(", ", data.Keys);
                string placeholders = string.Join(", ", data.Keys.Select(key => "@" + key));

                cmd.CommandText = $"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})";

                foreach (var entry in data)
                {
                    cmd.Parameters.AddWithValue("@" + entry.Key, entry.Value);
                }
                cmd.ExecuteNonQuery();
            }
        }

        public static List<T> Select<T>(NpgsqlConnection conn, string tableName, Dictionary<string, object> parameters)
        {
            List<T> results = new List<T>();

            using (NpgsqlCommand cmd = new NpgsqlCommand())
            {
                cmd.Connection = conn;

                string query = $"SELECT * FROM {tableName} WHERE ";
                
                foreach (var parameter in parameters)
                {
                    query += $"{parameter.Key} = @{parameter.Key} AND ";
                    cmd.Parameters.AddWithValue($"@{parameter.Key}", parameter.Value);
                }

                // Remove the trailing "AND" from the query
                query = query.Remove(query.Length - 5);

                cmd.CommandText = query;

                using (NpgsqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        T entry = Activator.CreateInstance<T>();

                        // Assuming the properties in T match the columns in the database
                        foreach (var prop in typeof(T).GetProperties())
                        {
                            prop.SetValue(entry, Convert.ChangeType(reader[prop.Name], prop.PropertyType), null);
                        }

                        results.Add(entry);
                    }
                        reader.Close();
                }
            }

            return results;
        }


        public static List<T> Select<T>(NpgsqlConnection conn, string tableName)
        {
            List<T> results = new List<T>();

            using (NpgsqlCommand cmd = new NpgsqlCommand())
            {
                cmd.Connection = conn;

                cmd.CommandText = $"SELECT * FROM {tableName}";

                using (NpgsqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        T entry = Activator.CreateInstance<T>();

                        // Assuming the properties in T match the columns in the database
                        foreach (var prop in typeof(T).GetProperties())
                        {
                            prop.SetValue(entry, Convert.ChangeType(reader[prop.Name], prop.PropertyType), null);
                        }

                        results.Add(entry);
                    }
                        reader.Close();
                }
            }

            return results;
        }

        public static string GetNextId(NpgsqlConnection conn, string SeqName , string abreviation)
        {
            using (NpgsqlCommand cmd = new NpgsqlCommand($"SELECT nextval('{SeqName}')", conn))
            {
                object result = cmd.ExecuteScalar();
                int sequenceValue = Convert.ToInt32(result);
                return string.Format("{0}{1}", abreviation, sequenceValue);
            }
        }
    }
}
using Microsoft.AspNetCore.Mvc;
using Npgsql;
using Models;
using System;
using Utils.helper;
using System.Collections.Generic;

public class ClientController : Controller
{
    private readonly NpgsqlConnection connection;

    public ClientController()
    {
        connection = new Connection().GetConnection();
    }
    
    public IActionResult Index()
    {
        if(HttpContext.Session.GetString("NONE") == null){
            ViewBag.ListClient = Client.SelectAll(connection);
        }else{
            String NONE = HttpContext.Session.GetString("NONE");
            ViewBag.ListClient = Client.SelectById(connection,NONE);
        }
    	return View();
    }

    public IActionResult Change(String NONE)
    {
        HttpContext.Session.SetString("NONE",NONE);
        return RedirectToAction("Index");
    }

    public IActionResult InsertForm()
    {
    	
    	return View();
    }
    
    [HttpPost]
    public IActionResult Insert(string id_client, string nom, object date_naissance, int sexe)
    {
	    try{
	    	
	    	Client client = new Client(id_client, nom, date_naissance, sexe);
	    	client.Insert(connection);
	    }catch (Exception ex){
	    	
	    }
	    return RedirectToAction("Index", "Client");
    }
    
    public IActionResult Delete()
    {
        return RedirectToAction("Index");
    }
}

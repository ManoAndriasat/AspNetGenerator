using Microsoft.AspNetCore.Mvc;
using Npgsql;
using Models;
using System;
using Utils.helper;
using System.Collections.Generic;

public class MaterielController : Controller
{
    private readonly NpgsqlConnection connection;

    public MaterielController()
    {
        connection = new Connection().GetConnection();
    }
    
    public IActionResult Index()
    {
        if(HttpContext.Session.GetString("NONE") == null){
            ViewBag.ListMateriel = Materiel.SelectAll(connection);
        }else{
            String NONE = HttpContext.Session.GetString("NONE");
            ViewBag.ListMateriel = Materiel.SelectById(connection,NONE);
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
    public IActionResult Insert(string id_materiel, string nom)
    {
	    try{
	    	
	    	Materiel materiel = new Materiel(id_materiel, nom);
	    	materiel.Insert(connection);
	    }catch (Exception ex){
	    	
	    }
	    return RedirectToAction("Index", "Materiel");
    }
    
    public IActionResult Delete()
    {
        return RedirectToAction("Index");
    }
}

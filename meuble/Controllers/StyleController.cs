using Microsoft.AspNetCore.Mvc;
using Npgsql;
using Models;
using System;
using Utils.helper;
using System.Collections.Generic;

public class StyleController : Controller
{
    private readonly NpgsqlConnection connection;

    public StyleController()
    {
        connection = new Connection().GetConnection();
    }
    
    public IActionResult Index()
    {
        if(HttpContext.Session.GetString("NONE") == null){
            ViewBag.ListStyle = Style.SelectAll(connection);
        }else{
            String NONE = HttpContext.Session.GetString("NONE");
            ViewBag.ListStyle = Style.SelectById(connection,NONE);
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
    public IActionResult Insert(string id_style, string nom)
    {
	    try{
	    	
	    	Style style = new Style(id_style, nom);
	    	style.Insert(connection);
	    }catch (Exception ex){
	    	
	    }
	    return RedirectToAction("Index", "Style");
    }
    
    public IActionResult Delete()
    {
        return RedirectToAction("Index");
    }
}

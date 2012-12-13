package com.yijiaowushu;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class Cwta_websiteServlet extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)  
			throws ServletException, IOException {
		//resp.setContentType("text/plain");
		//resp.getWriter().println("Hello, world");
		
		String requestURL = req.getRequestURI();
		if ("/home".equals(requestURL)) {
			String home = "/home.html";
			ServletContext context = getServletContext();
			RequestDispatcher dispatcher = context.getRequestDispatcher(home);
			dispatcher.forward(req, resp);
		}
	}
}
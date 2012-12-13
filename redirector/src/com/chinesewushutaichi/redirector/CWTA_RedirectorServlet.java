package com.chinesewushutaichi.redirector;

import java.io.IOException;
import javax.servlet.http.*;

@SuppressWarnings("serial")
public class CWTA_RedirectorServlet extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		String path = ((HttpServletRequest) req).getRequestURI();
		
		resp.setStatus(HttpServletResponse.SC_MOVED_PERMANENTLY);
		resp.setHeader("Location", "http://www.chinesewushutaichi.com" + path);
		resp.setHeader("Connection", "close");
		
		//resp.sendRedirect(path);
	}
}

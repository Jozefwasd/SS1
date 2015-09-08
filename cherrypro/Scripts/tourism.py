import cherrypy 
import os, os.path 
import sqlite3 
from jinja2 import Environment, FileSystemLoader 
fileSystemLoader = FileSystemLoader('templates') 
env = Environment(loader = fileSystemLoader)

class Root: 
	@cherrypy.expose 
	def index(self): 
		tmpl = env.get_template('index.html') 
		return tmpl.render(salutation='Tourism in our country')
		
	@cherrypy.expose
	def Slovakia(self):
		tmpl = env.get_template('Slovakia.html') 
		return tmpl.render(salutation='Tourism in Slovakia')
							
	@cherrypy.expose
	def Romania(self):
		tmpl = env.get_template('Romania.html') 
		return tmpl.render(salutation='Tourism in Romania')
							
	@cherrypy.expose
	def Denmark(self):
		tmpl = env.get_template('Denmark.html') 
		return tmpl.render(salutation='Tourism in Denmark',)
	
	
	@cherrypy.expose						
	def Contact(self):
		
		DBcustList = self.getCustomer()
		
		tmpl = env.get_template('Contacts.html')
		return tmpl.render(salutation='Contact information',  
							DBcustList = DBcustList)
													
	def connect(self):						
		self.conn=sqlite3.connect('comments')
		self.cursor=self.conn.cursor()
		
		
		
	def getCustomer(self):	
		self.DBcustList = []
		self.connect() 
		self.cursor.execute(""" 
							SELECT * from comments ;""",)
		self.conn.commit()
		
		for row in self.cursor.fetchall(): # Get tuple of tuples 
			for field in row: # Iterate over "name tuple" 
				self.DBcustList.append(field)
		
		#self.DBcustList = list(self.cursor.fetchall())
		self.cursor.close()
		self.conn.close()
		return self.DBcustList
		
	@cherrypy.expose						
	def insertComment(self, name=None, comment=None):
		self.connect()			
		params = (name, comment)
		self.cursor.execute("""
							INSERT INTO comments VALUES (?,?)""", params)					
		self.conn.commit()
		self.cursor.close()
		self.conn.close()	
		return self.Contact()	
		
# Set cherrypy configurations 
if __name__ == '__main__': 
	current_dir = os.path.dirname(os.path.abspath(__file__))	
	# Set cherrypy configurations 
	cherrypy.config.update({'server.socket_host': '127.0.0.1', 
							'server.socket_port': 8080, 
							}) 
			
	conf = { 
		'/': 		{ 
					'tools.sessions.on': True, 
					'tools.staticdir.root': os.path.abspath(os.getcwd()) 
					}, 
		'/static':  { 
					'tools.staticdir.on': True, 
					'tools.staticdir.dir': './public' 
					},
		'/images': { 
					'tools.staticdir.on': True, 
					'tools.staticdir.dir': os.path.join(current_dir, 'images')	
					},
		'/favicon.ico': 
					{ 
					'tools.staticfile.on': True, 
					'tools.staticfile.filename': '/images/favicon2.ico' 
					}
			} 

	# Start cherrypy 
	cherrypy.quickstart(Root(), '/', conf)
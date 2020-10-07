from src.database import Database
from src.models.menu import Menu

Database.initialize()

menu = Menu()

menu.run_menu()


#from_database = Blog.from_mongo(blog.id)
#print(blog.get_posts())        #Post.from_blog(id)


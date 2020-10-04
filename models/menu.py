from src.database import Database
from src.models.blog import Blog


class Menu:
    def __init__(self):
        self.user = input("Enter your author name: ")                       # Ask user for author name
        self.user_blog = None
        if self._user_has_account():                                        # Check if they've already got an account
            print(f"Welcome back {self.user}")
        else:                                                               # if not, prompt them to create one
            self._prompt_user_for_account()

    def _user_has_account(self):                                            # Verify if user have already got an account
        blog = Database.find_one('blogs', {'author': self.user})            # Find blog with author=self.author <- usr
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['_id'])                    # self.blog = objeto Blog passando o id do blog que foi encontrado para esse usr
            return True
        else:
            return False                                                    # Não existe Blog para esse nome de usr

    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        # User read or write blogs?
        read_or_write = input("Do you want to read (R) or write (W) blogs? ")

        # if read:
        if read_or_write.upper() == 'R':
            # list blogs in database
            # allow user to pick one
            # display posts
            self._list_blogs()
            self._view_blog()
            pass
        # if write
        elif read_or_write.upper() == 'W':
            # Prompt to create new blog
            self.user_blog.new_post()
        else:
            print("Thank you for blogging!")

    def _list_blogs(self):
        blogs = Database.find(collection="blogs",
                              query={})
        for blog in blogs:
            print(f"ID: {blog['_id']}, Title: {blog['title']}, Author: {blog['author']}")

    def _view_blog(self):
        blog_to_see = input("Enter the ID of the blog you'd like to read: ")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print(f"> > > >   < < < <\nDate: {post['created_date']}\nTitle: {post['title']}\n<\n{post['content']}\n>")

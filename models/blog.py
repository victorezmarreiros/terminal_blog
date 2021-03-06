import uuid
import datetime

from src.database import Database
from src.models.post import Post


class Blog:
    def __init__(self, author, title, description, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self):
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        date = input("Enter post date, or leave blank for today (in format DDMMYYYY): ")
        if date == "":
            date = datetime.datetime.utcnow()  # se o usuário nao entrar data -> será a data de agora
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y")  # precisamos parsear essa data .strptime(<date>, "%d%m%Y")  -> .StringParseTime() <%letra-minuscula -> espera 2 digts; %LETRA-MAIUSCULA -> espera 4 digts>

        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection="blogs",
                        data=self.json())

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "_id": self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection="blogs",
                                      query={"_id": _id})

        return cls(**blog_data)

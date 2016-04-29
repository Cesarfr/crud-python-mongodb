from pymongo import MongoClient
import datetime


class DbTest:

    # def __init__(self):  # special method __init__
    #     self.gg = ""

    @staticmethod
    def get_db():
        client = MongoClient(host="localhost", port=27017)
        db = client['test-db']
        return db

    @staticmethod
    def add_post(mydb):
        author = raw_input("Ingresa un nombre\n")
        text = raw_input("Ingresa el texto del post\n")
        post = {"author": author,
                "text": text,
                "date": datetime.datetime.utcnow()}
        posts = mydb.posts
        post_id = posts.insert_one(post).inserted_id
        print post_id

    @staticmethod
    def get_posts(mydb):
        cursor = mydb.posts.find()
        return cursor


def main():
    test = DbTest()
    db = test.get_db()
    while True:
        print """
        1.- Agregar post
        2.- Obtener todos los registros
        3.- Salir
        """
        opcion = raw_input("Escribe la opcion\n")
        if opcion == "1":
            test.add_post(db)
        elif opcion == "2":
            data = test.get_posts(db)
            for document in data:
                print document
        else:
            break

if __name__ == "__main__":
    main()

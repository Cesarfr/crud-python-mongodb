from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId


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
        author = raw_input("Ingresa un nombre para el autor\n")
        text = raw_input("Ingresa el texto del post\n")
        post = {"author": author,
                "text": text,
                "date": datetime.datetime.now(),
                "lastUpdate": datetime.datetime.now()
                }
        posts = mydb.posts
        post_id = posts.insert_one(post).inserted_id
        print("ID del post: %s" % str(post_id))

    @staticmethod
    def get_posts(mydb):
        cursor = mydb.posts.find()
        return cursor

    @staticmethod
    def get_name_post(mydb):
        cursor = mydb.posts.find({}, {"author": 1})
        return cursor

    @staticmethod
    def update_post(mydb, idc):
        author = raw_input("Ingresa el nuevo autor\n")
        text = raw_input("Ingresa el nuevo texto del post\n")
        post_updated = mydb.posts.update_one(
            {"_id": ObjectId(idc)},
            {
                "$set": {
                    "author": author,
                    "text": text,
                    "lastUpdate": datetime.datetime.now()
                }
            }
        )
        print("Post modificados: %s" % str(post_updated.matched_count))

    @staticmethod
    def del_post(mydb, idd):
        post_deleted = mydb.posts.delete_one({"_id": ObjectId(idd)})
        print("Posts eliminados: %s" % str(post_deleted.deleted_count))


def main():
    test = DbTest()
    db = test.get_db()
    while True:
        print """
        1.- Agregar post
        2.- Obtener todos los posts
        3.- Editar un post
        4.- Eliminar un post
        5.- Salir
        """
        opcion = raw_input("Escribe la opcion\n")
        if opcion == "1":
            test.add_post(db)
        elif opcion == "2":
            data = test.get_posts(db)
            for document in data:
                print("id: %s\t author: %s\t text: %s\t date: %s\t lastUpdate: %s" % (str(document['_id']),
                      document['author'], document['text'], str(document['date']), str(document['lastUpdate'])))
        elif opcion == "3":
            data = test.get_name_post(db)
            for document in data:
                print("id: %s\t author: %s\t" % (str(document['_id']), document['author']))
            id_sel = raw_input("\nSelecciona el ID del post a modificar\n")
            test.update_post(db, id_sel)
        elif opcion == "4":
            data = test.get_name_post(db)
            for document in data:
                print("id: %s\t author: %s\t" % (str(document['_id']), document['author']))
            id_del = raw_input("\nSelecciona el ID del post a eliminar\n")
            test.del_post(db, id_del)
        else:
            break

if __name__ == "__main__":
    main()

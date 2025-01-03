from pymongo import MongoClient
import numpy as np

class MongoDB:
    def __init__(self, uri, database_name, collection_name):
        '''
        DB Format: 
        {
            "Name": UsrName,
            "Encodings": [[],[],[]...],
            "AverageEncoding": [],
            "Image": image
        }
        '''
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        print("Connected to MongoDB")

    def get_average_encoding(self, encodings):
        array = np.array(encodings)
        average = np.mean(array, axis=0)
        average_list = average.tolist()
        return average_list

    def add_data(self, name, image, encoding):
        image = image.tolist()
        person = self.collection.find_one({"Name": name})
        if person:
            updated_encodings = person["Encodings"]
            updated_encodings.append(encoding)
            average_encoding = self.get_average_encoding(updated_encodings)
            self.collection.update_one(
                {"Name": name}, 
                {"$set": {
                    "Encodings": updated_encodings,
                    "AverageEncoding": average_encoding,
                    "Image": image
            }})
        else:
            document = {
                "Name": name,
                "Encodings": [encoding],
                "AverageEncoding": encoding,
                "Image": image
            }
            self.collection.insert_one(document)

    def get_all_encodings(self):
        all_encodings = {"Names": [], "Encodings": []}
        cursor = self.collection.find()
        for person in cursor:
            all_encodings['Names'].append(person['Name'])
            all_encodings['Encodings'].append(person['AverageEncoding'])
        return all_encodings

    def close_connection(self):
        self.client.close()
    
from xml.etree.ElementTree import fromstring
from json import dumps, loads
from xmljson import abdera
from xmljson import yahoo
from pymongo import MongoClient
import os


def read_dir(path):
    files = os.listdir(path)

    return files

def convert_xml2json(xml_file):
    with open(xml_file,'r',encoding='utf8') as file:
        xml = file.read()

    json = dumps(yahoo.data(fromstring(xml)))
    json = loads(json)

    return json


def connect_mongodb():
    client = MongoClient()

    return client


def insert_db(db,json):
    result = db.curriculos.insert_one(json)

    return result


def main():
    client = connect_mongodb()
    db = client.lattes
    path = 'dados/xml/'
    files = read_dir(path)

    for file in files:
        try:
            filepath = path + file
            print(filepath)
            json = convert_xml2json(filepath)
            result = insert_db(db,json)
            if result:
                print("Curriculo persistido com sucesso!")
        except Exception as e:
            print(e)
            continue
        

if __name__ == '__main__':
    main()

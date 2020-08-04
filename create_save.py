import json
import os
from .spiders import itcast
def create_file(path1):
    file_path = os.path.abspath(r"/home/pi/Desktop/spider")
    file_name2 = file_path + "//" + str(path1)
    file_name21 = file_name2 + "//" + "source"
    file_name22 = file_name2 + "//" + "rections"
    os.makedirs(file_name2)
    os.makedirs(file_name21)
    os.makedirs(file_name22)
def save(txt,id,source_id):
    with open("/home/pi/Desktop/spider/{}/rections/{}.json".format(source_id, id), "w+") as jsonFile:
        jsonFile.write(json.dumps(txt, ensure_ascii=False))
"""
p2pTorrent Generator and Parser
"""
import json
import hashlib
from uuid import uuid1
from collections import namedtuple


class Torrent:
    def __init__(self, name, uid1, encryption, slice_encryption, size, slice_size):
        self.name = name
        self.uid1 = uid1
        self.encryption = encryption
        self.slice_encryption = slice_encryption
        self.size = size
        self.slice_size = slice_size

    @staticmethod
    def create(file_name, content, slice_size=204800):
        # get data of the file by byte
        ########## content = Torrent.get_data(file_name)

        # get encryption content slices
        slice_encryption = Torrent.get_slices(content, slice_size)

        # get encryption of total data
        sha = hashlib.sha256()
        sha.update(content)
        encryption = sha.hexdigest()

        # get unique id
        uid1 = str(uuid1())

        # create torrent
        t = Torrent(file_name, str(uid1), encryption, slice_encryption, len(content), len(slice_encryption))
        return t

    @staticmethod
    def creates(file_name, slice_size=204800):
        content = Torrent.get_data(file_name)
        Torrent.create(file_name, content, slice_size)


    @staticmethod
    # read the data from the file
    def get_data(file_name):
        with open(file_name, mode="rb") as file:
            return file.read()

    @staticmethod
    # create slices between contents
    def get_slices(content, slice_size):
        temp = []
        result = []
        for number in range(0, len(content), slice_size):
            temp.append(content[number: number + slice_size])

        # encryption
        for i in range(len(temp)):
            sha = hashlib.sha256()
            sha.update(temp[i])
            result.append(sha.hexdigest())
        return result

    def dumps(self):
        return json.dumps(self.__dict__, indent=2)

    def dump(self, filename):
        with open(filename, 'w') as writer:
            writer.write(self.dumps())

    @staticmethod
    def loads(string):
        _dict = json.loads(string)
        return namedtuple('Torrent', _dict.keys())(*_dict.values())

    @staticmethod
    def load(filename):
        with open(filename, 'r') as reader:
            return Torrent.loads(reader.read())

    def __str__(self):
        return self.dumps



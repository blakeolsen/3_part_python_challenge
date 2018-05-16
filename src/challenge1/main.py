
from argparse import ArgumentParser
from flask import Flask, abort, request, Response
from tools.kvstore import DictKVStore

import json
import hashlib
import re

class KVServer:
    """
    Simple Key Value server
    """
    def __init__(self, name="", host="localhost", port=5000, store=DictKVStore()):
        """
        :param name: name of the KVStore
        :param host: the host machine
        :param port: the port hosted on
        """
        self.host = host
        self.port = port

        self.store = DictKVStore()

        self.app = Flask(name)
        self.app.add_url_rule("/messages", "put", self.put, methods=['POST'])
        self.app.add_url_rule("/messages/<string:hash>", "get", self.get, methods=['GET'])

    def run(self):
        """
        :return: None
        """
        self.app.run(host=self.host, port=self.port)

    def _hash(self, value):
        """
        :param value: value to be hashed
        :return: the hashed value
        """
        hasher = hashlib.sha256()
        hasher.update(value.encode('utf-8'))
        return hasher.hexdigest()

    def put(self):
        """
        :return: the hashed value
        """
        value = json.loads(request.data).get('message', None)
        if not value:
            return Response(
                status=400,
                response=json.dumps({ "err_msg":"Missing Parameter: %s" % "message" }),
                mimetype="application/json"
            )

        # Hash the value
        key = self._hash(value)

        try:
            self.store.put(key, value)
        except:
            return Response(
                status=409,
                response=json.dumps({ "err_msg":"Unable to Complete Request" }),
                mimetype="application/json"
            )

        return Response(
            status=200,
            response=json.dumps({ "digest":key }),
            mimetype="application/json"
        )

    def get(self, hash):
        """
        :param hash: the hashed value
        :return: the unhashed value
        """
        value = self.store.get(hash)
        if not value:
            return Response(
                status=404,
                response=json.dumps({ "err_msg":"Message Not Found" }),
                mimetype="application/json"
            )
        return Response(
            status=200,
            response=json.dumps({ "message":value }),
            mimetype="application/json"
        )

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Challenge #1",
        description="Key management server for items, using SHA256 to generate keys"
    )

    parser.add_argument(
        "--port",
        help="port to receive routes on",
        type=int,
        default=5000
    )

    parser.add_argument(
        "--kvstore",
        help="the path to the kvstore adapter",
        default="tools.kvstore.DictKVStore"
    )

    args = vars(parser.parse_args())

    mod_adap = args['kvstore'].rsplit('.', 1)
    adapter = getattr(__import__(mod_adap[0], globals(), locals(), mod_adap[1]), mod_adap[1])()

    KVServer(name="Challenge #1", host="localhost", port=args['port'], store=adapter).run()
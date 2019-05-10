import json

from flask import Response, jsonify, make_response

class Resp:
    def __init__(self, obj, status):
        """Resp
        
        Arguments:
            obj {str} -- message object
            status {int} -- HTTP status code
        """
        self.obj = obj
        self.status = status

    @staticmethod
    def _dict(obj, status):
        """return json messages.
        
        Arguments:
            obj {dict} -- dict messages.
            status {int} -- HTTP status code.
        """
        return Response(json.dumps(obj, ensure_ascii=False).encode("utf8"), mimetype='application/json', status=status)

    @staticmethod
    def _sdict(obj, status):
        """ return sort of json messages.
        
        Arguments:
            obj {dict} -- dict messages.
            status {int} -- HTTP status code.
        """
        return make_response(jsonify(obj), status)

    @staticmethod
    def _text(obj, status):
        """return string messages.
        
        Arguments:
            obj {any} -- messages
            status {int} -- HTTP status code.
        """
        return Response(obj, status=status)
    
    @property
    def _dict(self):
        return Response(json.dumps(self.obj, ensure_ascii=False).encode("utf8"), mimetype='application/json', status=self.status)
    
    @property
    def _sdict(self):
        return make_response(jsonify(self.obj), self.status)

    @property
    def _text(self):
        return Response(self.obj, status=self.status)

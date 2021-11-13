"""
Extended controller to add gql query and pdf export.
"""

import base64
import logging
from xmlrpc.client import dumps, loads

from odoo import http
from odoo.http import request
from odoo.service import wsgi_server
from werkzeug.wrappers import Response

from .serializers import Serializer

_logger = logging.getLogger(__name__)


class CwsAPI(http.Controller):

    def _loads(self):
        """ db, uid, passwd = params[0], int(params[1]), params[2]
        """
        data = request.httprequest.get_data()
        params, _ = loads(data)

        model, method, args, kwargs = params[3:6]
        query = kwargs.pop('query', {'id'})
        return model, params, query, args, kwargs

    @http.route("/cws_gql", auth='none', methods=["POST"], csrf=False, save_session=False)
    def cws_gql(self):
        """Entry to retrieve data with GraphQL syntax."""
        try:
            model, params, query, args, kwargs = self._loads()
            result = http.dispatch_rpc("object", "search", params)
            rec = request.env[model].browse(result)
            serializer = Serializer(rec, query, many=True)
            data = serializer.data

            response = dumps(({"result": data},), methodresponse=True, allow_none=False)
            return Response(response=response, mimetype='application/json')
        except Exception as error:
            response = wsgi_server.xmlrpc_handle_exception_int(error)
        return Response(response=response, mimetype='text/xml')

    @http.route('/cws_pdf/<int:rec_id>', auth='none', methods=["POST"], csrf=False, save_session=False)
    def cws_pdf(self, rec_id, **post):
        try:
            model, params, query, args, kwargs = self._loads()
            obj = self._get_model('ir.actions.report').browse(rec_id).ensure_one()
            res_ids = kwargs.get('res_ids')
            data = kwargs.get('data', '{}')
            content, _ = getattr(obj, 'render_qweb_pdf')(res_ids, data)
            return base64.b64encode(content)
        except Exception as error:
            response = wsgi_server.xmlrpc_handle_exception_int(error)
        return Response(response=response, mimetype='text/xml')

# Copyright 2018 ACSONE SA/NV
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request
from werkzeug.exceptions import BadRequest

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_api_key(cls):
        api_key = request.httprequest.headers.get('Authorization')
        if not api_key:
            raise BadRequest('Access token missing')

        if api_key.startswith('Bearer '):
            access_token = api_key[7:]

        user_id = request.env["res.users.apikeys"]._check_credentials(scope='neorezo', key=api_key)
        if not user_id:
            raise AccessDenied()

        # take the identity of the API key user
        request.uid = user_id
        request.auth_api_key = api_key
        return user_id

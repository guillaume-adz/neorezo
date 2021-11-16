from odoo import models, fields


class Tenant(models.Model):
    _name = 'res.company'
    _inherit = ['res.company']

    tenant_prefix = fields.Char(string="Référence du tenant")

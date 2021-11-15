from odoo import models, fields


class ProductTemplate(models.Model):
    _name = 'res.company'
    _inherit = ['res.company']

    tenant_prefix = fields.Char(string='Prefix des commandes')

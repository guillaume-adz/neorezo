from odoo import models, fields


class Tenant(models.Model):
    _name = 'res.company'
    _inherit = ['res.company']
    _sql_constraints = [
        ('tenant_prefix', 'unique(tenant_prefix)', "A tenant prefix must be unique.")
    ]

    tenant_prefix = fields.Char(
        string="Tenant prefix",
        help="This prefix will be added on all invoices"
    )

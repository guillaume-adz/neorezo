from odoo import models, fields


class Tenant(models.Model):
    _name = 'res.company'
    _inherit = ['res.company']
    _sql_constraints = [
        ('tenant_prefix', 'unique(tenant_prefix)', "A tenant prefix must be unique.")
    ]

    tenant_prefix = fields.Char(
        string="Tenant prefix",
        help="This prefix will be added on all invoices."
    )
    tenant_parent = fields.Many2one(
        comodel_name="res.company",
        auto_join=True,
        string="Tenant parent",
        help="This tenant is attached to this parent."
    )

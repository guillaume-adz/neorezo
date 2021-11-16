from odoo import models, fields


class Invoice(models.Model):
    _name = 'account.move'
    _inherit = ['account.move']

    billing_address1 = fields.Char(string="Adresse (ligne1)")
    billing_address2 = fields.Char(string="Adresse (ligne2)")
    billing_company = fields.Char(string="Société")
    billing_country = fields.Char(string="Pays")
    billing_email = fields.Char(string="Courriel")
    billing_first_name = fields.Char(string="Prénom")
    billing_last_name = fields.Char(string="Nom")
    billing_phone = fields.Char(string="Téléphone")
    billing_zip = fields.Char(string="Code postal")

    billing_purchase_margin = fields.Float(string="Marge d'achat")
    billing_sale_margin = fields.Float(string="Marge de vente")

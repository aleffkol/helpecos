from odoo import models, fields

class Res_Partner(models.Model):
    _inherit = 'res.partner'

    responsavel = fields.Char(string="Responsável")

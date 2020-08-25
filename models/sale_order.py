from odoo import models, fields

class Sale_Order(models.Model):
    _inherit = 'sale.order'

    chamado_id = fields.Many2one('chamado.chamado', string="Chamado") # ok
    departamento = fields.Many2one('hr.department', string="Departamento", required=True)  # ok
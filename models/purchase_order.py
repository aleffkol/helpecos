from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    chamado_id = fields.Many2one('chamado.chamado', string="Chamado") # ok
    departamento = fields.Many2one('hr.department', string="Departamento", required=True)  # ok
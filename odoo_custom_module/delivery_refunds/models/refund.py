from odoo import models, fields, api

class DeliveryRefund(models.Model):
    _name = 'delivery.refund'
    _description = 'Handles Order Refunds'

    order_id = fields.Many2one('sale.order', string='Order')
    customer_id = fields.Many2one('res.partner', string='Customer')
    refund_amount = fields.Float(string='Amount')
    status = fields.Selection([
        ('requested', 'Refund Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ], default='requested')

    def approve_refund(self):
        """Approve and process refund."""
        self.write({'status': 'processed'})
        # Trigger actual refund via payment gateway

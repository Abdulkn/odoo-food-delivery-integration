from odoo import models, fields, api

class CourierSettlement(models.Model):
    _name = 'courier.settlement'
    _description = 'Courier Weekly Payouts'

    courier_id = fields.Many2one('res.partner', string='Courier')
    week_start_date = fields.Date(string='Week Start')
    total_orders = fields.Integer(string='Orders Delivered')
    total_earnings = fields.Float(string='Earnings (60%)')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
    ], default='draft')

    def confirm_payout(self):
        """Mark settlement as paid."""
        self.write({'status': 'paid'})

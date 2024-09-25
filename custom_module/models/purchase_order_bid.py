from odoo import models, fields, api

class PurchaseOrderBid(models.Model):
    _name = 'purchase.order.bid'
    _description = 'Vendor Bids'

    purchase_order_id = fields.Many2one('purchase.order', string='Request for Quotation', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, domain="[('supplier_rank', '>', 0)]")
    bid_amount = fields.Float(string='Bid Amount', required=True)
    delivery_date = fields.Date(string='Delivery Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    @api.model
    def submit_bid(self):
        self.write({'state': 'submitted'})

    @api.model
    def accept_bid(self):
        self.write({'state': 'accepted'})
        # Logic to update the RFQ with the selected bid
        self.purchase_order_id.write({
            'partner_id': self.vendor_id.id,
            'amount_total': self.bid_amount,
            'date_planned': self.delivery_date,
        })
        # Mark other bids as rejected
        other_bids = self.search([('purchase_order_id', '=', self.purchase_order_id.id), ('id', '!=', self.id)])
        other_bids.write({'state': 'rejected'})

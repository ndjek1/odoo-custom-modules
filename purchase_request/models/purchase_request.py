from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string="Request Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    requestor_id = fields.Many2one('res.users', string="Requestor", default=lambda self: self.env.user, readonly=True)
    department_id = fields.Many2one('hr.department', string="Department")
    date_request = fields.Datetime(string="Request Date", default=fields.Datetime.now, readonly=True)
    date_needed = fields.Date(string="Date Needed")
    item_description = fields.Text(string="Item Description", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    reason = fields.Text(string="Reason for Request")
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected'),
                              ('rfq_created', 'RFQ Created')], 
                              default='draft', string="Status")
    
    # Relationship with purchase orders for integration with RFQ
    purchase_order_id = fields.Many2one('purchase.order', string="RFQ", readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or _('New')
        return super(PurchaseRequest, self).create(vals)

    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

    def action_create_rfq(self):
        # Create an RFQ from the approved request
        purchase_order = self.env['purchase.order'].create({
            'partner_id': False,  # Procurement will set vendors
            'date_order': fields.Datetime.now(),
            'order_line': [(0, 0, {
                'name': self.item_description,
                'product_qty': self.quantity,
                'price_unit': 0.0,  # No price at this stage
                'date_planned': self.date_needed,
            })],
        })
        self.purchase_order_id = purchase_order.id
        self.state = 'rfq_created'


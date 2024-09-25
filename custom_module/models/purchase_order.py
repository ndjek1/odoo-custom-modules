# models/purchase_order.py
from odoo import models, fields, api,_

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_field = fields.Many2many('res.partner', string='Vendors')
    bid_ids = fields.One2many('purchase.order.bid', 'purchase_order_id', string='Vendor Bids')
    selected_bid_id = fields.Many2one('purchase.order.bid', string='Selected Bid', readonly=True)

    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the purchase RFQ email template loaded by default,
        allowing the user to send the RFQ to multiple vendors.
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']

        try:
            # Use a specific template for sending the RFQ or the PO
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data._xmlid_lookup('your_module.email_template_rfq')[1]
            else:
                template_id = ir_model_data._xmlid_lookup('your_module.email_template_rfq_done')[1]
        except ValueError:
            template_id = False

        try:
            # Use the standard email composition form
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        # Prepare the context for sending the email to multiple vendors
        ctx = dict(self.env.context or {})

        # Extract vendor emails from the custom field `vendor_ids` (custom_field)
        vendor_emails = self.mapped(
            'custom_field.email')  # Assuming `custom_field` is one-to-many relation to res.partner
        ctx.update({
            'default_model': 'purchase.order',
            'default_res_ids': self.ids,
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_partner_ids': self.custom_field.ids,  # Ensure the emails are associated with the vendors
            'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        # Handle the translation and set the correct language context for the email
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self = self.with_context(lang=lang)

        # Customize the "View..." button based on the state of the RFQ or PO
        if self.state in ['draft', 'sent']:
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Order')

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


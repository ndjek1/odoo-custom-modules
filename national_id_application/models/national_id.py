from odoo import models, fields, api
from odoo.cli.scaffold import env


class NationalIdApplication(models.Model):
    _name = 'national.id.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'A model for national id application'

    name = fields.Char(string="Name")
    dob = fields.Date(string="Date of Birth")
    nationality = fields.Char(string="Nationality")
    address = fields.Char(string="Address")
    email = fields.Char(string="Email")
    picture = fields.Binary(string="Picture")
    lc_reference_letter = fields.Binary(string="LC Reference Letter", attachment=True)
    approval_stage = fields.Selection([
        ('draft', 'Draft'),
        ('stage1', 'Stage 1'),
        ('stage2', 'Stage 2'),
        ('approved', 'Approved'),
    ], string='Approval Stage', default='draft', tracking=True)

    # Fields to control button visibility
    move_to_stage1_visible = fields.Boolean(compute='_compute_button_visibility', store=True)
    move_to_stage2_visible = fields.Boolean(compute='_compute_button_visibility', store=True)
    approve_visible = fields.Boolean(compute='_compute_button_visibility', store=True)

    @api.depends('approval_stage')
    def _compute_button_visibility(self):
        for rec in self:
            rec.move_to_stage1_visible = (rec.approval_stage == 'draft')
            rec.move_to_stage2_visible = (rec.approval_stage == 'stage1')
            rec.approve_visible = (rec.approval_stage == 'stage2')

    def move_to_stage1(self):
        self.write({'approval_stage': 'stage1'})

    def move_to_stage2(self):
        self.write({'approval_stage': 'stage2'})

    def approve(self):
        self.write({'approval_stage': 'approved'})

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(NationalIdApplication, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self:
            res['context'] = dict(res.get('context', {}), approval_stage=self.approval_stage)
        return res



# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EngagementCancelled(models.TransientModel):
    _name = 'engagement.cancelled'
    _description = 'Get Lost Reason'

    cancel_reason_id = fields.Many2one('engagement.cancel.reason', 'Cancel Reason')

    @api.multi
    def action_cancel_reason_apply(self):
        engagement = self.env['volunteer.engagement'].browse(self.env.context.get('active_id'))
        engagement.write({
            'cancel_reason': self.cancel_reason_id.id,
            'state': 'cancel',
            'end_date': fields.Date.today()
        })        

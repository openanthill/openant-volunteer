# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EngagementCancelled(models.TransientModel):
    _name = 'engagement.cancelled'
    _description = 'Get Lost Reason'

    cancel_reason_id = fields.Many2one('engagement.cancel.reason', 'Cancel Reason')

    @api.multi
    def action_cancel_reason_apply(self):
        for res in self:
            engagement = res.env['volunteer.engagement'].browse(res.env.context.get('active_id'))
            engagement.write({
                'cancel_reason': res.cancel_reason_id.id,
                'state': '50-cancel',
                'end_date': fields.Date.today()
            })

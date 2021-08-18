# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EngagementOnhold(models.TransientModel):
    _name = 'engagement.onhold'
    _description = 'Get On hold Reason'

    onhold_reason_id = fields.Many2one('engagement.onhold.reason', 'On hold Reason')

    @api.multi
    def action_onhold_reason_apply(self):
        for res in self:
            engagement = res.env['volunteer.engagement'].browse(res.env.context.get('active_id'))
            engagement.write({
                'onhold_reason': res.onhold_reason_id.id,
                'state': 'onhold'
            })        

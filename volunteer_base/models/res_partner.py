# © 2021 humanilog (https://www.humanilog.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    volunteer = fields.Boolean(
        string='Is a Volunteer',
        help="Check this box if this contact is a volunteer.",
    )
    engagement_ids = fields.One2many(
        comodel_name='volunteer.engagement',
        inverse_name='partner_id',
        string='Engagements',
    )
    engagement_count = fields.Integer(
        string='Engagement Count',
        compute='_compute_engagement_count',
    )

    @api.depends('engagement_ids')
    def _compute_engagement_count(self):
        for partner in self:
            partner.engagement_count = len(partner.engagement_ids.ids)

    @api.model
    def _cron_update_volunteer(self):
        partners = self.search([('is_company', '=', 'False'), ('volunteer', '=', 'False')])
        
        for partner in partners:
            if partner.engagement_ids:
                partner.write({"volunteer": True})      

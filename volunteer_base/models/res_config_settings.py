# © 2021 humanilog (https://www.humanilog.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    engagement_onhold_days = fields.Integer(
        string='On hold default days',
        required=True,
        default=60,
        help="Enter the default amount of days for engagement on hold timeframes here.\n"
             "The amount of days will be used to compute the onhold until date in \n"
             "engagements when the onhold button is clicked."
    )

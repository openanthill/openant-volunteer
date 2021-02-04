# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class VolunteerProject(models.Model):
    _name = 'volunteer.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Volunteer Projects'

    # FIELDS
    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the project without removing it."
    )
    name = fields.Char(
        string='Name',
        index=True,
        required=True,
        tracking=True,
        track_visibility='always',
        help="Name of the volunteer project",
    )
    timeframe = fields.Selection(
        string='Timeframe',
        selection = [
            ('ongoing', 'Ongoing'),
            ('period', 'Time Period'),
        ],
        default='ongoing',
        required=True,
        tracking=True,
        track_visibility='always',
        help="Select wether the project has a conrete period with a start end end date or is ongoing",
    )
    date_start = fields.Date(string='Start Date'
    )
    date_end = fields.Date(string='End Date'
    )

    @api.constrains('date_start', 'date_end')
    def _check_default_date_start_ends(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            raise ValidationError(_(
                "Start Date should be before or be the "
                "same as End Date for Projects '%s'.")
                % self.display_name)

    @api.onchange('date_start')
    def date_start_change(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            self.date_end = self.date_start

    @api.onchange('date_end')
    def date_end_change(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            self.date_start = self.date_end    

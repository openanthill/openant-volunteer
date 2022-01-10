# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class VolunteerProject(models.Model):
    _name = 'volunteer.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Volunteer Projects'
    _order = 'sequence, name, id'    

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
        translate=True,
        help="Name of the volunteer project",
    )
    sequence = fields.Char(
        string='Reference',
        default="/",
        help="Sequence to identify volunteer projects easily",
    )
    description = fields.Html(
        string='Project Description',
        translate=True,
    )
    timeframe = fields.Selection(
        string='Timeframe',
        selection = [
            ('ongoing', 'Ongoing'),
            ('period', 'Time Period'),],
        default='ongoing',
        required=True,
        tracking=True,
        track_visibility='always',
        help="Select wether the project has a conrete period with a start end end date or is ongoing",
    )
    date_start = fields.Date(
        string='Start Date'
    )
    date_end = fields.Date(
        string='End Date'
    )
    engagement_default_duration = fields.Integer(
        default=1,
        string='Default Duration',
        help="Default duration for engagements created for this project.\n"
             "This timeframe will be used for computation of start and end dates",
    )
    engagement_default_duration_type = fields.Selection([
        ('daily', 'Day(s)'),
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)')],
        default='monthly',
        string='Duration Type',
        help="Specify duration type for engagement default duration.",
    )
    engagement_ids = fields.One2many(
        comodel_name='volunteer.engagement',
        inverse_name='volunteer_project_id',
        string='Engagements',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', '/') == '/':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('volunteer.project')
        return super(VolunteerProject, self).create(vals_list)
    
    @api.multi
    def copy(self, default=None):
        for res in self:
            if default is None:
                default = {}
            default['sequence'] = res.env['ir.sequence'].next_by_code('volunteer.project')
            return super(VolunteerProject, res).copy(default)

    @api.constrains('date_start', 'date_end')
    def _check_default_date_start_ends(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            raise ValidationError(_(
                "Start Date should be before or be the "
                "same as End Date for Projects '%s'.")
                % self.display_name)

    @api.onchange('date_start')
    def _onchange_date_start(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            self.date_end = self.date_start

    @api.onchange('date_end')
    def _onchange_date_end(self):
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            self.date_start = self.date_end    

# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VolunteerEngagement(models.Model):
    _name = 'volunteer.engagement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Volunteer Engagements'

    name = fields.Char(
        string='Engagement Reference',
        required=True,
        default="/",
        readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Volunteer',
        required=True,
        index=True,
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},
        track_visibility='onchange',
        ondelete='restrict',
        help="The volunteer which is supporting the organisation with an engagement."
    )
    volunteer_project_id = fields.Many2one(
        string='Project',   
        comodel_name='volunteer.project',
        required=True,
        tracking=True,
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},
        track_visibility='always'
    )
    state = fields.Selection(
        string='State',
        selection = [
            ('10-new', 'New'),
            ('20-active', 'Active'),
            ('30-onhold', 'On Hold'),
            ('40-success', 'Sucessful'),
            ('50-cancel', 'Cancelled')],
        default='10-new',
        required=True,
        tracking=True,
        track_visibility='always',
        help=" * The 'New' status is the default when an engagement is created.\n"
             " * The 'Active' status is used when the volunteer is actively working in the engagement.\n"
             " * The 'On Hold' status is used when the volunteer is pausing his activities in an engagemen.\n"
             " * The 'Successful' status is set when the volunteer has successfully ended to engagement.\n"
             " * The 'Cancelled' status is used when a volunteer has aborted an engagnement befor successfully ending it."
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible Person',
        track_visibility='onchange',
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},        
        default=lambda self: self.env.user
    )
    start_date = fields.Date(
        string='Start date',
        tracking=True,
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},
        track_visibility='always',
        help="In this field the start date of an engagement can be saved."
    )
    end_date = fields.Date(
        string='End date',
        tracking=True,
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},
        track_visibility='always',
        help="In this field the end date of an engagement can be saved."
    )
    state_onhold_until = fields.Date(
        string='On hold until',
        tracking=True,
        track_visibility='always',
        states={'40-success': [('readonly', True)],
                '50-cancel': [('readonly', True)]},        
        help="In this field that date when a volunteering engagmeent was set on hold"
    )
    date_cancel = fields.Date(
        string='Cancel date',
        help="Date when Volunteer requested to cancel the engagement"
    )
    cancel_reason_id = fields.Many2one(
        string='Cancel reason',
        comodel_name='engagement.cancel.reason',
        index=True,
        track_visibility='onchange',
        help="The reason why a volunteer caneceled an engagement"
    )
    onhold_reason_id = fields.Many2one(
        string='On hold reason',
        comodel_name='engagement.onhold.reason',
        index=True,
        track_visibility='onchange',
        help="The reason why a volunteer puts an engagement on hold"
    )

    filterable_groupable_fields = ['state','state_onhold_until','start_date','end_date']

    _sql_constraints = [
        ('volunteer_engagement_unique_name', 'UNIQUE (name)',
         'The Engagement Reference must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        new_volunteer_engagements = super(VolunteerEngagement, self).create(vals_list)
        for volunteer_engagement in new_volunteer_engagements:
            if volunteer_engagement.name is False or volunteer_engagement.name == "/":
                volunteer_engagement.name = self.env['ir.sequence'].next_by_code('volunteer.engagement')
        return new_volunteer_engagements

    @api.multi
    def copy(self, default=None):
        for res in self:
            if default is None:
                default = {}
            default['name'] = res.env['ir.sequence'].next_by_code('volunteer.engagement')
            return super(VolunteerEngagement, res).copy(default)

    @api.multi
    def action_volunteer_engagement_active(self):
        for res in self:
            if res.state == '10-new':
                project = res.volunteer_project_id
                if project.timeframe == 'ongoing':
                    if not res.start_date:
                        date_start = fields.Date.today()
                    else:
                        date_start = res.start_date
                    date_end = date_start + res.get_relative_delta(
                    project.engagement_default_duration_type, project.engagement_default_duration)
                elif project.timeframe == 'period':
                    date_start = datetime.combine(project.date_start, time.min)
                    date_end = datetime.combine(project.date_end, time.min)

                res.write({
                    'state': '20-active',
                    'start_date': date_start,
                    'end_date': date_end})
            
            elif res.state == '30-onhold':
                res.write({
                    'state': '20-active',
                    'state_onhold_until': fields.Date.today()})

    @api.multi
    def action_volunteer_engagement_success(self):
        for res in self:
            if not res.end_date:
                date_end = fields.Date.today()
            else:
                date_end = res.end_date

            res.write({
                'state': '40-success',
                'end_date': date_end
            })
        
    @api.multi
    def action_volunteer_engagement_reopen(self):
        for res in self:
            return res.write({'state': '20-active'})

    @api.onchange('start_date', 'end_date')
    def _onchange_start_end_date(self):
        if self.start_date is not False and self.end_date is not False:
            if self.end_date < self.start_date:
                raise ValidationError('The End Date must be after the Start Date.')

    @api.onchange('volunteer_project_id')
    def _onchange_volunteer_project_id(self):
        if not self.volunteer_project_id:
            self.start_date = False
            self.end_date = False            
        else:
            if self.volunteer_project_id.timeframe == 'ongoing':
                self.start_date = False
                self.end_date = False
            elif self.volunteer_project_id.timeframe == 'period':
                self.update({
                    'start_date': self.volunteer_project_id.date_start,
                    'end_date': self.volunteer_project_id.date_end,
                })
        
        return

    @api.model
    def get_relative_delta(self, default_duration_type, default_duration):
        if default_duration_type == 'daily':
            return relativedelta(days=default_duration)
        elif default_duration_type == 'weekly':
            return relativedelta(weeks=default_duration)
        elif default_duration_type == 'monthly':
            return relativedelta(months=default_duration)
        else:
            return relativedelta(years=default_duration)

class EngagementCancelReason(models.Model):
    _name = "engagement.cancel.reason"
    _description = "Reasons for Volunteers to cancel engagements"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean('Active', default=True)

class EngagementOnholdReason(models.Model):
    _name = "engagement.onhold.reason"
    _description = "Reasons for Volunteers to put engagements on hold"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean('Active', default=True)

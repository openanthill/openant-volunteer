# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class VolunteerEngagement(models.Model):
    _name = 'volunteer.engagement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Volunteer Engagements'

    volunteer_id = fields.Many2one(
        comodel_name='volunteer.volunteer',
        string='Volunteer',
        required=True,
        index=True,
        states={'finished': [('readonly', True)]},
        track_visibility='onchange',
        ondelete='restrict'
    )    
    volunteer_project_id = fields.Many2one(
        string='Projekt',
        comodel_name='volunteer.project',
        required=True,
        tracking=True,
        states={'finished': [('readonly', True)]},
        track_visibility='always'
    )
    state = fields.Selection(
        string='State',
        selection = [
            ('new', 'New'),
            ('onboarding', 'Onboarding'),
            ('active', 'Active'),
            ('onhold', 'On Hold'),
            ('success', 'Sucessful'),
            ('cancel', 'Cancelled')],
        default='new',
        required=True,
        tracking=True,
        track_visibility='always',
        help=" * The 'Onboarding' status is used when a volunteer is in the onboarding process for a certain engagement.\n"
             " * The 'Active' status is used when the volunteer is actively working in the engagement.\n"
             " * The 'On Hold' status is used when the volunteer is pausing his activities in an engagemen.\n"
             " * The 'Successful' status is set when the volunteer has successfully ended to engagement.\n"
             " * The 'Cancelled' status is used when a volunteer has aborted an engagnement befor successfully ending it."
    )
    start_date = fields.Date(
        string='Start date',
        tracking=True,
        states={'finished': [('readonly', True)]},
        track_visibility='always',
        help="In this field the start date of an engagement can be saved."
    )
    end_date = fields.Date(
        string='End date',
        tracking=True,
        states={'finished': [('readonly', True)]},
        track_visibility='always',
        help="In this field the end date of an engagement can be saved."
    )
    state_onhold_until = fields.Date(
        string='On hold until',
        tracking=True,
        track_visibility='always',
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

    filerable_groupable_fields = ['state','state_onhold_until','start_date','end_date']
    
    # BUTTON ACTIONS
    @api.multi
    def action_volunteer_engagement_active(self):
        if self.state == 'new':
            self.write({
                'state': 'active',
                'start_date': fields.Date.today()
            })

    @api.multi
    def action_volunteer_engagement_on_hold(self):
        return self.write({'state': 'onhold'})

    @api.multi
    def action_volunteer_engagement_success(self):
        self.write({
            'state': 'success',
            'end_date': fields.Date.today()
        })
        
    @api.multi
    def action_volunteer_engagement_reset(self):
        return self.write({'state': 'new'})

    # ONCHANGE EVENT HANDLERS

    @api.onchange('start_date', 'end_date')
    def _onchange_start_end_date(self):
        if self.start_date != False and self.end_date != False:
            if self.end_date < self.start_date:
                raise ValidationError('The End Date must be after the Start Date.')

class EngagementCancelReason(models.Model):
    _name = "engagement.cancel.reason"
    _description = "Reasons for Volunteers to cancel engagements"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean('Active', default=True)

# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError

class VolunteerVolunteer(models.Model):
    _name = 'volunteer.volunteer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Volunteers'
    _inherits = {'res.partner': 'partner_id'}
    _order = 'name'

    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        required=True,
        ondelete='restrict',
        auto_join=True,
        help='Enter here the partner details of the volunteer.'
    )
    active = fields.Boolean(
        default=True,
        help="The active field allows you set an Volunteer to active/inactive. Inactive Volunteers"
             "are only displayed when explictly filtered for"
    )
    active_partner = fields.Boolean(
        related='partner_id.active',
        readonly=True,
        string="Partner is Active"
    )
    name = fields.Char(
        related='partner_id.name',
        inherited=True,
        readonly=False
    )
    phone = fields.Char(
        related='partner_id.email',
        inherited=True,
        readonly=False
    )
    mobile = fields.Char(
        related='partner_id.email',
        inherited=True,
        readonly=False
    )    
    email = fields.Char(
        related='partner_id.email',
        inherited=True,
        readonly=False
    )
    lang = fields.Char(
        related='partner_id.email',
        inherited=True,
        readonly=False
    )
    engagement_ids = fields.One2many(
        'volunteer.engagement',
        'volunteer_id',
        string='Engagements',
        readonly=True
    )
# image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        string='Photo',
        attachment=True,
        help="This field holds the image used as photo for the employee, limited to 1024x1024px."
    )
    image_medium = fields.Binary(
        string='Medium-sized photo',
        attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views."
    )
    image_small = fields.Binary(
        string='Small-sized photo',
        attachment=True,
        help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required."
    )

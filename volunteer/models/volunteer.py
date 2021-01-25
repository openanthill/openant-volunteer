# Copyright 2020 humanilog (https://www.humanilog.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class VolunteerSkills(models.Model):
    _name = 'volunteer.skills'
    _description = 'Skills for Volunteers to match with projects'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True
    )
    profession_ids = fields.Many2many(
        comodel_name='volunteer.profession',
        column1='skills_id',
        column2='profession_id',
        string='Professions'
    )
    # volunteer_project_ids = fields.Many2many(
    #     comodel_name='volunteer.project',
    #     column1='skills_id',
    #     column2='volunteer_project_id',
    #     string='Volunteer Projects'
    # )    

class VolunteerProfession(models.Model):
    _name = 'volunteer.profession'
    _description = 'Professions for Volunteers to derive skills'
    _order = 'name'

    name = fields.Char(
        string='Name',
        translate=True,
        required=True
    )
    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the profession without removing it."
    )
    skills_id = fields.Many2many(
        comodel_name='volunteer.skills',
        column1='profession_id',
        column2='skills_id',
        translate=True,
        string='Skills',
    )

# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Volunteer',
    'version': '12.0.1.0.0',
    'category': 'openant',
    'license': 'AGPL-3',
    'summary': 'openAnt Volunteers',
    'author': 'humanilog',
    'website': 'https://github.com/openanthill',
    'depends': [
        'volunteer_base',
    ],
    'data': [
        'security/volunteer_security.xml',
        'security/ir.model.access.csv',
        'views/volunteer_menu.xml',
    ],
    'demo': [
        'demo/res_user_demo.xml',
        'demo/res_partner_demo.xml',
        'demo/volunteer_demo.xml',
        'demo/volunteer_project_demo.xml',
        'demo/volunteer_engagement_demo.xml',
    ],
    'installable': True,
}

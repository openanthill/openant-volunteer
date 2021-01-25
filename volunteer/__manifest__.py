# Copyright 2020  humanilog <www.humanilog.org>
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
        # 'views/volunteer_profession.xml',
        # 'views/volunteer_skills.xml',
        ],
    'demo': [
        # 'demo/donation_demo.xml'
    ],
    'installable': True,
}

# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Volunteer Base',
    'version': '12.0.2.0.0',
    'category': 'openant base',
    'license': 'AGPL-3',
    'summary': 'Volunteer base module',
    'author': 'humanilog',
    'website': 'https://github.com/openanthill',
    'depends': [
        'base',
        'mail',        
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',
        'data/reason_data.xml',
        'data/volunteer_data.xml',

        'wizard/engagement_cancel_views.xml',
        'wizard/engagement_onhold_views.xml',

        'views/res_partner.xml',
        'views/volunteer_engagement.xml',
        'views/volunteer_project.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/volunteer_project_demo.xml',
        'demo/volunteer_engagement_demo.xml',
    ],
    'installable': True,
}

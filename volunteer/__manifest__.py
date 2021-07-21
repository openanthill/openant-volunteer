# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Volunteer',
    'version': '12.0.1.0.0',
    'category': 'openant',
    'license': 'AGPL-3',
    'summary': 'Volunteers management',
    'author': 'humanilog',
    'website': 'https://github.com/openanthill',
    'depends': [
        'volunteer_base',
    ],
    'data': [
        'security/volunteer_security.xml',
        'security/ir.model.access.csv',
        
        'views/res_partner.xml',
        'views/volunteer_menu.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [
        'demo/res_user_demo.xml',
    ],
    'installable': True,
}

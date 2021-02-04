# © 2021 humanilog (https://www.humanilog.org)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Volunteer Base',
    'version': '12.0.1.0.0',
    'category': 'openant base',
    'license': 'AGPL-3',
    'summary': 'openAnt Volunteer base',
    'author': 'humanilog',
    'website': 'https://github.com/openanthill',
    'depends': [
        'base',
        'mail',        
    ],
    'data': [

        'wizard/engagement_cancel_views.xml',

        'views/volunteer_engagement.xml',
        'views/volunteer_project.xml',
        'views/volunteer_volunteer.xml',
        ],
    'demo': [
    ],
    'installable': True,
}

{
    'name': 'FPT SMS Integration',
    'version': '1.0',
    'summary': 'CuongLV Send SMS via FPT Brandname and manage templates',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/fpt_sms_template_views.xml',
        'data/fpt_config.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}

# -*- coding: utf-8 -*-
{
    'name': "national_id_application",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "",
 'license': 'LGPL-3',  # Add this line

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/national_id.xml',
        'views/national_id_webform.xml',
        'views/thank_you_page.xml',
    ],
'controllers': [
    'controllers/controllers.py',
],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


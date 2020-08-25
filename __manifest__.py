# -*- coding: utf-8 -*-
{
    'name': "helpecos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'note', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/chamado.xml',
        'views/sequence_os.xml',
        'views/res_partner_inherit_form_view.xml',
        'views/sale_order_inherit_form_view.xml',
        'views/purchase_order_inherit_form_view.xml',
        'views/sede.xml',
        'views/os_subcategoria.xml',
        'views/os_categoria.xml',
        'views/execucao.xml',
        'views/holiday.xml',
        'reports/report_chamado.xml',
        'reports/report_execucao.xml',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

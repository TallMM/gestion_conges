# -*- coding: utf-8 -*-
{
    'name': "gestion_conges",

    'summary': "Automatise la gestion des congés à partir du recrutement jusqu'au planning",

    'description': """
                Ce module permet de gérer de manière fluide :
            - Le recrutement et la conversion automatique en employé
            - La génération automatique du planning de congés
            - Le suivi des dates de départ et de retour
            - La gestion des reliquats de congés
            - Les rapports PDF personnalisés
    """,

    'author': "Mamoudou Tall",
    'website': "https://www.smartsa.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'RH',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_holidays', 'hr_recruitment', 'hr_contract', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/conge_views.xml',
        'views/employe_views.xml',
        'views/contrat_views.xml',
        'views/templates.xml',
        'data/employee_matricule_sequence.xml',
        'report/report_planning_conge.xml',  # Template QWeb en premier
        'report/rapports.xml', # Déclaration du rapport après
        'data/ir_model_data.xml',               
        'data/cron.xml',
          
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {

        'web.assets_backend': [
            'gestion_conges/static/src/js/conge_nombre_jours.js',
        ],

    #'web.assets_backend':['gestion_conges/static/src/assets.xml',],
}
}


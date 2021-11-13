{
    'name': "Odoo CWS API",
    'summary': "Odoo CWS API",
    'description': """
        Odoo Controller with GraphQL query and PDF export.
    """,
    'author': "G. Doumenc",
    'category': 'developers',
    'version': '0.1',
    'depends': ['base'],

    "application": True,
    "installable": True,
    "auto_install": False,

    'external_dependencies': {
        'python': ['pypeg2', 'requests']
    }
}

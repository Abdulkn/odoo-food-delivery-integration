{
    'name': 'Delivery Settlement',
    'version': '1.0',
    'summary': 'Handles courier & restaurant payouts',
    'depends': ['account', 'sale'],
    'data': [
        'views/settlement_views.xml',
    ],
    'installable': True,
    'application': True,
}

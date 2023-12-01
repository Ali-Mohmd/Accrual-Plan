# -*- coding: utf-8 -*-
{
    'name': "Accrual Plan Enhancement",
    'summary': """Accrual Plan Enhancement""",
    'description': """Accrual Plan Enhancement""",
    'author': "ZAD SOLUTIONS Ali Khalil akhalil@zadsolutions.com",
    'website': "http://www.zadsolutions.net",
    'category': 'HR',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_holidays', 'hr_enhancement'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_leave_allocation_view.xml',
        'views/hr_leave_accrual_level_view.xml',
        'views/hr_employee_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# -*- coding: utf-8 -*-
{'name': "Employee  tax_deductions ",
 'summary': """
       Multiple tax_deductions for employee""",
 'description': """
            Add many tax_deductions to any employee, include in payroll and END of Service Reward calculation
    """,
 'author': "I VALUE solutions",
 'website': "https://ivalue-s.com",
 'email': "info@ivalue-s.com",
 'license': "OPL-1",
 'category': 'HR',
 'version': '0.1',
 'images': ['static/description/Banner.png'],
 'depends': ['base', 'mail', 'hr_contract', 'hr_payroll'],
 'data': [
     'data/data.xml',
     'security/ir.model.access.csv',
     'views/hr_tax_deduction_views.xml',
 ],
 'demo': []
 }

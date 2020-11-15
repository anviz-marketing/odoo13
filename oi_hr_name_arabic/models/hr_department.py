'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Department(models.Model):
    _inherit = "hr.department"

    name = fields.Char(translate = True)
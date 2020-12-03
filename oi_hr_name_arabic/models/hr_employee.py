'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    #name = fields.Char(translate = True)
    name = fields.Char(string="Employee Name", related='resource_id.name', store=True, readonly=False, tracking=True, translate = True)

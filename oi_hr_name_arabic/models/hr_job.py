'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Job(models.Model):
    _inherit = "hr.job"

    name = fields.Char(translate = True)
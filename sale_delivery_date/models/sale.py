'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Sale(models.Model):
    _inherit = "sale.order"

    commitment_date = fields.Datetime('Delivery Date',
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'done': [('readonly', False)]},
                                      copy=False, readonly=True, track_visibility='onchange',
                                      help="This is the delivery date promised to the customer. "
                                           "If set, the delivery order will be scheduled based on "
                                           "this date rather than product lead times.")
# -*- coding: utf-8 -*-

import time
from datetime import datetime, date
from dateutil import relativedelta
from odoo import models, fields, api, _


class EmployeePromotion(models.Model):
    _name = 'hr.promotion'
    _description = 'HR Promotion'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    name = fields.Char(string='Promotion', required=True, help='the promotion name')
    previous_salary = fields.Integer(string='Previous Salary', required=True, help='the previous salary')
    new_salary = fields.Integer(string='New Salary', required=True, help='the new salary')
    previous_job_position = fields.Many2one('hr.job', string='Previous Job Postion', required=True, Help='Previous job position')
    new_job_position = fields.Many2one('hr.job', string='New Job Postion', required=True, Help='New job position')
    date = fields.Date(string='Date',
                            default=time.strftime('%Y-%m-%d'), readonly=False, help="promotion date")
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)

class HrPromotion(models.Model):
    _inherit = 'hr.employee'

    promotion = fields.One2many('hr.promotion', 'employee_id', string="Promotion", help="Promotion")
    promotion_salary = fields.Float(string='Promotion Salary', required=False, help='the promotion salary')
    def get_insure_subtotal(self):
        current_date = datetime.now()
        current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
        for emp in self:
            ins_amount = 0
            for ins in emp.insurance:
                x = str(ins.date_from)
                y = str(ins.date_to)
                if x < current_datetime:
                    if y > current_datetime:

                        ins_amount = ins_amount + ins.new_salary - ins.previous_salary

        emp.promotion_salary = ins_amount





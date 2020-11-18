# -*- coding: utf-8 -*-

import time
from datetime import datetime,date
from dateutil import relativedelta
from odoo import models, fields, api, _


class EmployeePerformanceBonus(models.Model):
    _name = 'hr.bonus'
    _description = 'HR Bonus'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    #policy_id = fields.Many2one('insurance.policy', string='Policy', required=True, help="Policy")
    #name = fields.Char(string='Insurance Name', required=True, help='the insurance name')
    base = fields.Float(string='Month Base', required=True, help="bonus base")
    ratio = fields.Float(string="Month Ratio", required=True, help="bonus ratio")
    bonus = fields.Float(string="Month Bonus", required=True, help="month bonus")
    policy_coverage = fields.Selection([('monthly', 'Monthly'), ('seasonly', 'Seasonly')],
                                       required=True, default='monthly',
                                       string='Policy Coverage', help="During of the policy")

    date_from = fields.Date(string='Date From',
                            default=time.strftime('%Y-%m-%d'), readonly=False, help="Start date")
    date_to = fields.Date(string='Date To',   readonly=False, help="End date",
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired'), ],
                             default='active', string="State",compute='get_status')
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)

    @api.onchange('base', 'ratio', 'bonus')
    def onchange_field(self):
        if self.base or self.ratio or self.bonus:
            self.bonus = self.base * self.ratio


    def get_status(self):
        current_datetime = datetime.now()
        current_date = datetime.strftime(current_datetime, "%Y-%m-%d ")
        for i in self:
            x = str(i.date_from)
            y = str(i.date_to)
            if x <= current_date:
                if y >= current_date:
                    i.state = 'active'
                else:
                    i.state = 'expired'

    @api.constrains('policy_coverage')
    @api.onchange('policy_coverage')
    def get_policy_period(self):
        if self.policy_coverage == 'monthly':
            self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
        if self.policy_coverage == 'seasonly':
            self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+3))[:10]


class HrBouns(models.Model):
    _inherit = 'hr.employee'

    bonus_amount= fields.Float(string="Performance Bonus", default=0, compute="get_bonus")
    bonus = fields.One2many('hr.bonus', 'employee_id', string="Bonus", help="Bonus",
                                domain=[('state', '=', 'active')])

    def get_bonus(self):
        current_date = datetime.now()
        current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
        for emp in self:

            bonus_sum= 0
            for ins in emp.bonus:
                x = str(ins.date_from)
                y = str(ins.date_to)
                if x < current_datetime:
                    if y > current_datetime:
                        bonus_sum = ins.bonus

        emp.bonus_amount = bonus_sum




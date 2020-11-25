# -*- coding: utf-8 -*-

import time
from datetime import datetime, date
from dateutil import relativedelta
from odoo import models, fields, api, _


class EmployeeInsurance(models.Model):
    _name = 'hr.insurance'
    _description = 'HR Insurance'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    # policy_id = fields.Many2one('insurance.policy', string='Policy', required=True, help="Policy")
    # name = fields.Char(string='Insurance Name', required=True, help='the insurance name')
    name = fields.Selection(
        [('养老', 'Pesion'), ('医疗', 'Medical'), ('失业', 'Unemployment'), ('生育', 'Fertility'), ('工伤', 'Work Injury'), ('住房公积金', 'House Fund')],
        required=True, default='养老',
        string='种类', help="保险种类")
    #amount = fields.Float(string='Premium', required=True, help="Policy amount")
    sum_personal_insured = fields.Float(string="Sum Personal Insured", required=True, help="Insured sum")
    sum_company_insured = fields.Float(string="Sum Company Insured", required=True, help="Insured sum")
    cardinal_number = fields.Float(string='Cardinal Number', required=True, help="the cardinal number")
    company_ratio = fields.Float(string='Company Ratio', required=True, help='the company ratio')
    personal_ratio = fields.Float(string='Personal Ratio', required=True, help='the personal ratio')

    policy_coverage = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                       required=True, default='monthly',
                                       string='Policy Coverage', help="During of the policy")
    date_from = fields.Date(string='Date From',
                            default=time.strftime('%Y-%m-%d'), readonly=False, help="Start date")
    date_to = fields.Date(string='Date To', readonly=False, help="End date",
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired'), ],
                             default='active', string="State", compute='get_status')
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)

    @api.onchange('cardinal_number', 'company_ratio', 'personal_ratio')
    def onchange_field(self):
        if self.cardinal_number or self.company_ratio or self.personal_ratio:
            self.sum_company_insured = self.cardinal_number * self.company_ratio
            self.sum_personal_insured = self.cardinal_number * self.personal_ratio

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
        if self.policy_coverage == 'yearly':
            self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+12))[:10]


class HrInsurance(models.Model):
    _inherit = 'hr.employee'


    insurance_percentage = fields.Float(string="Company Percentage ", help="Company insurance percentage")
    insurance = fields.One2many('hr.insurance', 'employee_id', string="Insurance", help="Insurance",
                                domain=[('state', '=', 'active')])
    insurance_pesion_personal = fields.Float(string="pesion personal", compute="get_insure_subtotal")
    insurance_medical_personal = fields.Float(string="medical personal", compute="get_insure_subtotal")
    insurance_unemployment_personal = fields.Float(string="unemployment personal", compute="get_insure_subtotal")
    insurance_hf_personal = fields.Float(string="house fund personal", compute="get_insure_subtotal")
    insurance_fertility_personal = fields.Float(string="fertility personal", compute="get_insure_subtotal")
    insurance_injury_personal = fields.Float(string="injury personal", compute="get_insure_subtotal")
    insurance_pesion_company = fields.Float(string="pesion company", compute="get_insure_subtotal")
    insurance_medical_company = fields.Float(string="medical company", compute="get_insure_subtotal")
    insurance_unemployment_company = fields.Float(string="unemployment company", compute="get_insure_subtotal")
    insurance_hf_company = fields.Float(string="house fund company", compute="get_insure_subtotal")
    insurance_fertility_company = fields.Float(string="fertility company", compute="get_insure_subtotal")
    insurance_injury_company = fields.Float(string="injury company", compute="get_insure_subtotal")
    length_of_service = fields.Integer(string="Length of service", default=False, compute='compute_service_years')

    @api.onchange('self.joining_date')
    def compute_service_years(self):
        self.length_of_service = 0
        for rec in self:
            if rec.joining_date:
                join = rec.joining_date
                current_date = datetime.now()
                self.length_of_service = relativedelta.relativedelta(current_date, join).years

    def get_insure_subtotal(self):
        current_date = datetime.now()
        current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
        for emp in self:
            ins_amount_pesion_personal = 0
            ins_amount_pesion_company = 0
            ins_amount_medical_personal = 0
            ins_amount_medical_company = 0
            ins_amount_fertility_personal = 0
            ins_amount_fertility_company = 0
            ins_amount_hf_personal = 0
            ins_amount_hf_company = 0
            ins_amount_unemployment_personal = 0
            ins_amount_unemployment_company = 0
            ins_amount_injury_personal = 0
            ins_amount_injury_company = 0
            for ins in emp.insurance:
                x = str(ins.date_from)
                y = str(ins.date_to)
                if x < current_datetime:
                    if y > current_datetime:
                        if ins.name == "养老":
                            ins_amount_pesion_personal = ins_amount_pesion_personal + ins.sum_personal_insured
                            ins_amount_pesion_company = ins_amount_pesion_company + ins.sum_company_insured
                        elif ins.name == "医疗":
                            ins_amount_medical_personal = ins_amount_medical_personal + ins.sum_personal_insured
                            ins_amount_medical_company = ins_amount_medical_company + ins.sum_company_insured
                        elif ins.name == "失业":
                            ins_amount_unemployment_personal = ins_amount_unemployment_personal + ins.sum_personal_insured
                            ins_amount_unemployment_company = ins_amount_unemployment_company + ins.sum_company_insured
                        elif ins.name == "生育":
                            ins_amount_fertility_personal = ins_amount_fertility_personal + ins.sum_personal_insured
                            ins_amount_fertility_company = ins_amount_fertility_company + ins.sum_company_insured
                        elif ins.name == "工伤":
                            ins_amount_injury_personal = ins_amount_injury_personal + ins.sum_personal_insured
                            ins_amount_injury_company = ins_amount_injury_company + ins.sum_company_insured
                        elif ins.name == "住房公积金":
                            ins_amount_hf_personal = ins_amount_hf_personal + ins.sum_personal_insured
                            ins_amount_hf_company = ins_amount_hf_company + ins.sum_company_insured

        emp.insurance_pesion_personal = ins_amount_pesion_personal
        emp.insurance_pesion_company = ins_amount_pesion_company
        emp.insurance_medical_personal = ins_amount_medical_personal
        emp.insurance_medical_company = ins_amount_medical_company
        emp.insurance_fertility_personal = ins_amount_fertility_personal
        emp.insurance_fertility_company = ins_amount_fertility_company
        emp.insurance_unemployment_personal = ins_amount_unemployment_personal
        emp.insurance_unemployment_company = ins_amount_unemployment_company
        emp.insurance_injury_personal = ins_amount_injury_personal
        emp.insurance_injury_company = ins_amount_injury_company
        emp.insurance_hf_personal = ins_amount_hf_personal
        emp.insurance_hf_company = ins_amount_hf_company



class HrInsurance(models.Model):
    _inherit = 'hr.contract'
    other_wage = fields.Integer(string="Other Wage")
    trial_wage = fields.Integer(string='Trial Wage')

    # def get_deduced_amount(self):
    #     current_date = datetime.now()
    #     current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
    #     for emp in self:
    #         ins_amount = 0
    #         for ins in emp.insurance:
    #             x = str(ins.date_from)
    #             y = str(ins.date_to)
    #             if x < current_datetime:
    #                 if y > current_datetime:
    #                     if ins.policy_coverage == 'monthly':
    #                         ins_amount = ins_amount + (ins.amount * 12)
    #                     else:
    #                         ins_amount = ins_amount + ins.amount
    #         emp.deduced_amount_per_year = ins_amount - ((ins_amount * emp.insurance_percentage) / 100)
    #         emp.deduced_amount_per_month = emp.deduced_amount_per_year / 12


# class InsuranceRuleInput(models.Model):
#     _inherit = 'hr.payslip'
#
#     def get_inputs(self, contract_ids, date_from, date_to):
#         res = super(InsuranceRuleInput, self).get_inputs(contract_ids, date_from, date_to)
#         contract_obj = self.env['hr.contract']
#         for i in contract_ids:
#             if contract_ids[0]:
#                 emp_id = contract_obj.browse(i[0].id).employee_id
#                 for result in res:
#                     if emp_id.deduced_amount_per_month != 0:
#                         if result.get('code') == 'INSUR':
#                             result['amount'] = emp_id.deduced_amount_per_month
#         return res

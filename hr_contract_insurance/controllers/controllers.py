# -*- coding: utf-8 -*-
# from odoo import http


# class HrContractInsurance(http.Controller):
#     @http.route('/hr_contract_insurance/hr_contract_insurance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_contract_insurance/hr_contract_insurance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_contract_insurance.listing', {
#             'root': '/hr_contract_insurance/hr_contract_insurance',
#             'objects': http.request.env['hr_contract_insurance.hr_contract_insurance'].search([]),
#         })

#     @http.route('/hr_contract_insurance/hr_contract_insurance/objects/<model("hr_contract_insurance.hr_contract_insurance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_contract_insurance.object', {
#             'object': obj
#         })

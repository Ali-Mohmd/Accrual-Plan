from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    joining_date = fields.Date(string="Joining Date", required=True,
                               help="The Date Employee start working in the company", )

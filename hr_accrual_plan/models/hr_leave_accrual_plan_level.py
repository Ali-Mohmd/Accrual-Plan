from odoo import api, fields, models, _


class AccrualPlanLevel(models.Model):
    _inherit = "hr.leave.accrual.level"

    months_after = fields.Integer(string="Number Of Months", help="Holds Holidays for the employee for x months.", )
    is_based_on_previous = fields.Boolean(string="Based on Previous", help="If checked this means that after holding holidays for x months in month x + 1 will give the employee x + 1 * holiday rate.", )

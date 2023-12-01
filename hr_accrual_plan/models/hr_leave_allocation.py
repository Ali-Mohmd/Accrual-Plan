from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.addons.resource.models.resource import HOURS_PER_DAY


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    joining_date_start = fields.Date(related="employee_id.joining_date")

    def _process_accrual_plan_level(self, level, start_period, start_date, end_period, end_date):
        """
        Returns the added days for that level
        """
        self.ensure_one()
        if level.is_based_on_worked_time:
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.min.time())
            worked = \
                self.employee_id._get_work_days_data_batch(start_dt, end_dt,
                                                           calendar=self.employee_id.resource_calendar_id) \
                    [self.employee_id.id]['hours']
            if start_period != start_date or end_period != end_date:
                start_dt = datetime.combine(start_period, datetime.min.time())
                end_dt = datetime.combine(end_period, datetime.min.time())
                planned_worked = self.employee_id._get_work_days_data_batch(start_dt, end_dt,
                                                                            calendar=self.employee_id.resource_calendar_id) \
                    [self.employee_id.id]['hours']
            else:
                planned_worked = worked
            left = self.employee_id.sudo()._get_leave_days_data_batch(start_dt, end_dt,
                                                                      domain=[('time_type', '=', 'leave')])[
                self.employee_id.id]['hours']
            work_entry_prorata = worked / (left + planned_worked) if (left + planned_worked) else 0
            added_value = work_entry_prorata * level.added_value
        else:
            added_value = level.added_value
        # Convert time in hours to time in days in case the level is encoded in hours
        if level.added_value_type == 'hours':
            added_value = added_value / (self.employee_id.sudo().resource_id.calendar_id.hours_per_day or HOURS_PER_DAY)
        period_prorata = 1
        if (start_period != start_date or end_period != end_date) and not level.is_based_on_worked_time:
            period_days = (end_period - start_period)
            call_days = (end_date - start_date)
            period_prorata = min(1, call_days / period_days) if period_days else 1

        # Customization
        # If There is Newcomers in Current Year
        for rec in self:
            after = self.env['hr.leave.accrual.level'].search([])
            joining_relative = rec.joining_date_start + relativedelta(months=after.months_after)

            if rec.date_from <= start_period <= joining_relative and rec.date_from <= end_period <= joining_relative:
                period_prorata = 0

            # based on previous holding months
            if after.is_based_on_previous:
                pre_months = after.months_after + 1
                if after.action_with_unused_accruals == 'lost':
                    if start_date.year == rec.joining_date_start.year:
                        pre_months = after.months_after + 1
                    elif start_date.year - 1 == rec.joining_date_start.year:
                        if joining_relative.year == start_date.year:
                            pre_months = (after.months_after + 1) - (13 - rec.joining_date_start.month)

                if start_period.day == joining_relative.day:
                    if start_period <= joining_relative + relativedelta(days=1) <= end_period:
                        period_prorata = pre_months
                else:
                    if start_period <= joining_relative <= end_period:
                        period_prorata = pre_months

        return added_value * period_prorata

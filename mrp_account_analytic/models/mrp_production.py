# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class WorkOrder(models.Model):
    _inherit = "mrp.production"

    time_cost_type = fields.Selection([('wc', 'Base on Work Centers'), ('user', 'Base on Employees')], default='wc', tracking=True,
                                      help='This allows the choice of time value calculation based on timesheet of employee or based on work centers. ')

    def _delete_old_analytic_acc(self):
        AnalyticLine = self.env["account.analytic.line"].sudo()
        # Remove old Analytic account
        recs_need_delete = AnalyticLine.search([('ref', 'ilike', 'Hours'),
                                                ('manufacturing_order_id', '=', self.id),
                                                ('account_id', '=', self.analytic_account_id.id)])
        if len(recs_need_delete):
            for i in recs_need_delete:
                i.unlink()

    def generate_hours_cost_by_work_center(self):
        self.ensure_one()
        self._delete_old_analytic_acc()
        # Generate rec in Analytic account
        AnalyticLine = self.env["account.analytic.line"].sudo()
        for rec in self.workorder_ids:
            if rec.date_planned_finished:
                hours = rec.duration / 60
                dic = {
                    "name": "{}/{}-(Hours cost base on work centers)".format(self.name, rec.name),
                    "account_id": self.analytic_account_id.id,
                    "date": fields.Date.today(),
                    "ref": rec.workcenter_id.name + " / " + "Hours",
                    "company_id": self.company_id.id,
                    "manufacturing_order_id": self.id,
                    "product_id": self.product_id.id,
                    "unit_amount": hours,
                    "amount": -(hours * rec.workcenter_id.costs_hour),
                    "product_uom_id": self.product_id.uom_id.id,
                }
                AnalyticLine.create(dic)

    def generate_hours_cost_by_employee(self):
        self.ensure_one()
        self._delete_old_analytic_acc()
        # Generate rec in Analytic account
        AnalyticLine = self.env["account.analytic.line"].sudo()
        for rec in self.workorder_ids:
            for line in rec.time_ids:
                if line.date_end:
                    dic = {
                        "name": "{}/{}-(Hours cost base on timesheet employee)".format(self.name, rec.name),
                        "account_id": self.analytic_account_id.id,
                        "date": fields.Date.today(),
                        "ref": rec.workcenter_id.name + " / " + "Hours",
                        "company_id": self.company_id.id,
                        "manufacturing_order_id": self.id,
                        "product_id": self.product_id.id,
                        "unit_amount": line.duration / 60,  # convert minutes to hours
                        "amount": -(line.duration / 60) * line.user_id.employee_id.timesheet_cost,
                        "product_uom_id": self.product_id.uom_id.id,
                    }
                    AnalyticLine.create(dic)

    def action_cancel(self):
        res = super(WorkOrder, self).action_cancel()
        if self.analytic_account_id:
            self._delete_old_analytic_acc()
        return res

    def button_mark_done(self):
        res = super(WorkOrder, self).button_mark_done()
        if self.analytic_account_id and self.time_cost_type == "wc":
            self.generate_hours_cost_by_work_center()
        elif self.analytic_account_id and self.time_cost_type == "user":
            self.generate_hours_cost_by_employee()
        return res

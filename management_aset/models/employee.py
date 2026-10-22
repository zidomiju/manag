from odoo import fields,models

class EngineerName(models.Model):
    _name="employee.name"
    _description="Define Engineer Name"
    _rec_name="employee_name"

    employee_name=fields.Char(string="Employee")
    job_title=fields.Char(string="Job Title")
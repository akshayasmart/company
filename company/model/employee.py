from odoo import  models,fields


class Emp(models.Model):
    _name = "emp.emp"

    name = fields.Char(string="First_Name", translate=True, domain="[('name','like', name)]")
    last_name = fields.Char(string="Last_Name")
    age = fields.Integer(string="Age")
    emp_id = fields.Integer(string="Id")
    emp_date_of_birth = fields.Date(string="Date of Birth")
    emp_feedback = fields.Text(string="FeedBack")
    emp_attendance = fields.Text(string='Attendance')
    emp_present = fields.Boolean(string="Present")
    emp_absent = fields.Boolean(string="Absent")
    emp_work = fields.Selection([('sales', 'Sales'),
                                 ('packing','Packing'),
                                 ('casher', 'Casher'),
                                 ('supervisor', 'Supervisor')])
    emp_gender = fields.Selection([('male', 'Male'),('female', 'Female')],'Gender')



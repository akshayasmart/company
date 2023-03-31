from odoo import models, fields


class Product(models.Model):

    _name = 'product.product'

    name = fields.Char(string="Product Name", help="Enter the Name")
    product_id = fields.Integer(string="Product_Id")
    exp_date = fields.Date(string="Exp_Date")
    product_price = fields.Float(string="Product_Price")
    status = fields.Selection([('available', 'Available'),
                               ('not-available', 'NotAvailable')])
    category = fields.Selection([('fruits', 'Fruits'),
                                 ('meat','Meat')],
                                 'Category')
    emp_work = fields.Selection([('sales', 'Sales'),
                                 ('packing', 'Packing'),
                                 ('casher', 'Casher'),
                                 ('supervisor', 'Supervisor')])
    image = fields.Image(string='Images')
    customer_details = fields.One2many(
        'customer.customer',
        'product_id',
        string='Customer_details',
    )
    color = fields.Integer(string='Color')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    offers_details = fields.Char(string='Offer Details')



from odoo import models, fields


class Product(models.Model):

    _name = 'product.product'

    product_name = fields.Char(string="Product_Name", help="Enter the Name")
    product_id = fields.Integer(string="Product_Id")
    exp_date = fields.Date(string="Exp_Date")
    product_price = fields.Float(string="Product_Price")
    status = fields.Selection([('available', 'Available'),
                               ('not-available', 'NotAvailable')])
    category = fields.Selection([('fruits', 'Fruits'),
                                 ('meat','Meat')],
                                 'Category')
    image = fields.Image(string='Images')


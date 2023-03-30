from odoo import models,fields


class Customer(models.Model):
    _name = "customer.customer"

    name = fields.Char(string="Name")
    category = fields.Selection([
        ('fruits', 'Fruits'),
        ('meat', 'Meat')],
        'Category'
    )
    product_id = fields.Many2one('product.product', string="Product")
    product_details_ids = fields.Many2many(
        'product.product',
        string="Product Details", domain="[('category','=',category)]"

    )
    product_exp_date = fields.Date(related='product_id.exp_date', string='Product Details')
    customer_id = fields.Integer(string='Customer ID')


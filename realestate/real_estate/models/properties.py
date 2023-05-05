from odoo import _,models ,fields,api
from datetime import timedelta
from odoo.exceptions import UserError



class Properties(models.Model):
    _name = 'estate.properties'
    @api.model
    def _get_default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    @api.model
    def _get_default_buyer(self):
        return self.env.context.get('buyer_id', self.env.user.id)

    @api.depends('living_area', 'garden_area')
    def total_area(self):
        for rec in self:
            rec.total = 0
            rec.total = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            best_offer = 0
            for child_record in rec.offer_ids:
                if child_record.price > rec.best_offer:
                    best_offer = child_record.price
            rec.best_offer = best_offer

    @api.constrains('expected_price')
    def constrains_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                    raise UserError(_(' The the unexpected Price must be strictly Positive'))


    # garden will set a default area of 10 and an orientation to North.

    @api.onchange('garden')
    def onchange_orientation(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orientation = 'south'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # You should be able to cancel and sold:

    def action_cancel(self):
        if self.status == 'sold':
            raise UserError('A sold property cannot be canceled.')
        else:
            self.status = 'cancel'

    def action_sold(self):
        if self.status == 'cancel':
            raise UserError('A canceled property cannot be set as sold.')
        else:
            self.status = 'sold'

    def accept_button(self):
        for record in self:
            for rec in record.offer_ids:
                rec.status = 'accepted'
                if rec.status == 'accepted':
                    self.write({
                        'selling_price': rec.price,
                        'buyer_id': rec.partner_id.id
                })

    def refused_button(self):
        for record in self:
            for rec in record.offer_ids:
                rec.status = 'refused'
                if rec.status == 'refused':
                    self.write({
                        'selling_price': 0,
                        'buyer_id' : [('buyer_id', '=', '')]
                })


    name = fields.Char(string='Title')
    tag_ids = fields.Many2many('estate.property.tag',string='Tags')
    properties_type_id = fields.Many2one('estate.property.type',string='Properties Type')
    post_code = fields.Char(string='Post Code')
    expected_price = fields.Float(string='Expected Price')
    available_from = fields.Date(string='Available From')
    best_offer = fields.Integer(string='Best Offer',compute='_compute_best_price')
    selling_price = fields.Float(string='Selling Price')
    description = fields.Text(string='Description')
    bedroom = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(stringt='Garden Area(sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    status = fields.Selection([('new', 'New'),
        ('cancel', 'Canceled'),
        ('sold', 'Sold')
    ], string='Status',default='new', readonly=True)

    total= fields.Integer(string='Total Area(sqm)' , compute='total_area')
    offer_ids = fields.One2many('estate.property.offer','properties_id',string='Properties')
    color = fields.Integer('Color Index', default=0)
    user_id = fields.Many2one('res.users',string='Salesman',default=_get_default_user)
    buyer_id = fields.Many2one('res.partner',string='Buyer',default=_get_default_buyer)

class Offer(models.Model):
    _name = 'estate.property.offer'

    @api.depends('validity')
    def _compute_validity_date(self):
        for rec in self:
            rec.deadline = fields.Date.today() + timedelta(days=rec.validity)

    def _set_deadline(self):
        for rec in self:
            rec.validity = (rec.deadline - fields.Date.today()).days

    @api.onchange('validity')
    def onchange_validity_days(self):
        self.deadline = fields.Date.today() + timedelta(days=self.validity)

    # def accept_offer(self):
    #     for rec in self:
    #         rec.status = 'accepted'
    #
    # def refused_offer(self):
    #     for rec in self:
    #         rec.status = 'refused'

    @api.constrains('selling_price', 'expected_price')
    def constrains_price(self):
        for rec in self:
            if rec.selling_price < rec.expected_price * 0.9:
                raise UserError(_(' The selling price cannot be lower than 90% of the expected price.'))

    properties_id = fields.Many2one('estate.properties',string='Offers')
    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner',string='Partner')
    validity = fields.Integer(string='validity(days)')
    status = fields.Selection([('refused','Refused'),
        ('accepted','Accepted')],string='Status'
        )
    deadline = fields.Date(string='Deadline',compute='_compute_validity_date', inverse='_set_deadline', store=True)




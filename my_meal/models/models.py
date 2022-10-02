# -*- coding: utf-8 -*-

from odoo import models, fields, api

class test_field_module(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    _description = 'test module'

    product_weight = fields.Integer('وزن الوجبة')
    calories = fields.Integer('عدد السعرات الحرارية')
    expiry_date = fields.Date('تاريخ إنتهاء الصلاحية')


class partner_meals(models.Model):
    _name = 'partners.meals'
    _description = 'meal group for partners'

    meal_name = fields.Selection([
        ('breakfast','وجبات الفطور'),
        ('lunch','وجبات الغداء'),
        ('dinner','وجبات العشاء')
    ],string='اسم الوجبة')

    partner_id = fields.Many2one('res.partner', string='اسم العميل')

    meal_datetime = fields.Datetime('وقت الوجبة')
    meal_note = fields.Text('ملاحظات')
    item_ids = fields.One2many('partners.meals.item', 'meal_id')
    total_price = fields.Float(string='المبلغ الأجمالي', compute='_calctotalprice', store=True)

    @api.depends('item_ids.meal_item_price')
    def _calctotalprice(self):
        for record in self:
            currentprice = 0
            for i in record.item_ids:
                currentprice = currentprice + i.meal_item_price
            record.total_price = currentprice

class partners_meals_items(models.Model):
    _name = 'partners.meals.item'
    _description = 'partners meals items'

    product_id = fields.Many2one('product.template', 'عنصر الوجبة')
    meal_id = fields.Many2one('partners.meals')
    meals_number = fields.Integer('عدد عناصر الوجبة')
    product_price = fields.Float(related="product_id.list_price", string='سعر عنصر الوجبة', readonly=False, store=False)
    calories = fields.Integer(related='product_id.calories', string='عدد السعرات الحرارية')
    weight = fields.Integer(related='product_id.product_weight', string='وزن الوجبة')
    meal_item_price = fields.Float(string='سعر عناصر الوجبات', compute='_calcprice', store=True)

    @api.depends('meals_number', 'product_price')
    def _calcprice(self):
        for record in self:
            record.meal_item_price = record.meals_number * record.product_price
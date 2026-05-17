from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    review_ids = fields.One2many(
        'product.review', 'product_id', string='Reviews',
        domain=[('state', '=', 'approved')],
    )
    review_count = fields.Integer(
        compute='_compute_review_stats', string='Reviews',
    )
    avg_rating = fields.Float(
        compute='_compute_review_stats', string='Avg Rating', digits=(3, 1),
    )
    allow_reviews = fields.Boolean(
        string='Allow Reviews', default=True,
    )

    @api.depends('review_ids', 'review_ids.state', 'review_ids.rating_int')
    def _compute_review_stats(self):
        for product in self:
            approved = product.review_ids.filtered(lambda r: r.state == 'approved')
            product.review_count = len(approved)
            if approved:
                product.avg_rating = sum(approved.mapped('rating_int')) / len(approved)
            else:
                product.avg_rating = 0.0

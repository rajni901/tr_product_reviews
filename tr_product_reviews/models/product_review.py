from odoo import api, fields, models


class ProductReview(models.Model):
    _name = 'product.review'
    _description = 'Product Review & Rating'
    _order = 'create_date desc'
    _rec_name = 'title'

    product_id = fields.Many2one(
        'product.template', string='Product',
        required=True, ondelete='cascade', index=True,
    )
    partner_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, ondelete='cascade',
    )
    title = fields.Char(string='Review Title', required=True)
    review = fields.Text(string='Review')
    rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    ], string='Rating', required=True, default='5')
    rating_int = fields.Integer(compute='_compute_rating_int', store=True)
    state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending', index=True)
    create_date = fields.Datetime(string='Date', readonly=True)

    @api.depends('rating')
    def _compute_rating_int(self):
        for rec in self:
            rec.rating_int = int(rec.rating) if rec.rating else 0

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_pending(self):
        self.write({'state': 'pending'})

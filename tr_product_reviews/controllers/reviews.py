from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError


class ProductReviewController(http.Controller):

    @http.route('/shop/product/review/submit', type='json',
                auth='user', website=True)
    def submit_review(self, product_id, rating, title, review='', **kwargs):
        try:
            product = request.env['product.template'].sudo().browse(int(product_id))
            if not product.exists() or not product.allow_reviews:
                return {'success': False, 'error': _('Reviews not allowed for this product.')}

            partner = request.env.user.partner_id
            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                return {'success': False, 'error': _('You have already reviewed this product.')}

            if not title:
                return {'success': False, 'error': _('Review title is required.')}

            if str(rating) not in ('1', '2', '3', '4', '5'):
                return {'success': False, 'error': _('Please select a rating.')}

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': str(rating),
                'title': title,
                'review': review,
                'state': 'pending',
            })
            return {'success': True, 'message': _('Thank you! Your review is pending approval.')}

        except Exception as e:
            return {'success': False, 'error': str(e)}

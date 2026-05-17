import json
from odoo import http, _
from odoo.http import request


class ProductReviewController(http.Controller):

    @http.route('/shop/product/review/submit', type='http',
                auth='user', website=True, methods=['POST'], csrf=False)
    def submit_review(self, **kwargs):
        try:
            product_id = int(kwargs.get('product_id', 0))
            rating = str(kwargs.get('rating', '0'))
            title = (kwargs.get('title') or '').strip()
            review = (kwargs.get('review') or '').strip()

            if not product_id:
                return self._resp(False, _('Invalid product.'))

            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists() or not product.allow_reviews:
                return self._resp(False, _('Reviews not allowed for this product.'))

            partner = request.env.user.partner_id
            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                return self._resp(False, _('You have already reviewed this product.'))

            if not title:
                return self._resp(False, _('Review title is required.'))

            if rating not in ('1', '2', '3', '4', '5'):
                return self._resp(False, _('Please select a valid rating.'))

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': rating,
                'title': title,
                'review': review,
                'state': 'pending',
            })
            return self._resp(True, _('Thank you! Your review is pending approval.'))

        except Exception as e:
            return self._resp(False, str(e))

    def _resp(self, success, message):
        data = json.dumps({
            'success': success,
            'message': message if success else None,
            'error': message if not success else None,
        })
        return request.make_response(
            data, headers=[('Content-Type', 'application/json')]
        )

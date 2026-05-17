import json
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class ProductReviewController(http.Controller):

    @http.route('/shop/product/review/submit', type='http',
                auth='user', website=True, methods=['POST'], csrf=False)
    def submit_review(self, **kwargs):
        _logger.info('TR Review Submit received: %s', kwargs)
        try:
            product_id = int(kwargs.get('product_id') or 0)
            rating = str(kwargs.get('rating') or '0')
            title = (kwargs.get('title') or '').strip()
            review = (kwargs.get('review') or '').strip()

            if not product_id:
                return self._resp(False, 'Invalid product ID.')

            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                return self._resp(False, 'Product not found.')

            partner = request.env.user.partner_id

            if not title:
                return self._resp(False, 'Review title is required.')

            if rating not in ('1', '2', '3', '4', '5'):
                return self._resp(False, 'Please select a valid rating (1-5).')

            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                return self._resp(False, 'You have already reviewed this product.')

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': rating,
                'title': title,
                'review': review,
                'state': 'pending',
            })
            _logger.info('TR Review created for %s by %s', product.name, partner.name)
            return self._resp(True, 'Thank you! Your review is pending approval.')

        except Exception as e:
            _logger.exception('TR Review Error: %s', str(e))
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

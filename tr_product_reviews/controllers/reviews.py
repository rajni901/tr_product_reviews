import json
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class ProductReviewController(http.Controller):

    @http.route('/shop/product/review/submit', type='http',
                auth='user', website=True, methods=['POST'], csrf=False)
    def submit_review(self, **kwargs):
        is_ajax = request.httprequest.headers.get('X-Requested-With') == 'XMLHttpRequest'
        redirect_url = request.httprequest.referrer or '/shop'

        try:
            product_id = int(kwargs.get('product_id') or 0)
            rating = str(kwargs.get('rating') or '0')
            title = (kwargs.get('title') or '').strip()
            review = (kwargs.get('review') or '').strip()

            if not product_id:
                return self._respond(is_ajax, False, 'Invalid product.', redirect_url)

            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                return self._respond(is_ajax, False, 'Product not found.', redirect_url)

            partner = request.env.user.partner_id

            if not title:
                return self._respond(is_ajax, False, 'Review title is required.', redirect_url)

            if rating not in ('1', '2', '3', '4', '5'):
                return self._respond(is_ajax, False, 'Please select a valid rating.', redirect_url)

            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                return self._respond(is_ajax, False, 'You have already reviewed this product.', redirect_url)

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': rating,
                'title': title,
                'review': review,
                'state': 'pending',
            })
            return self._respond(is_ajax, True,
                                 'Thank you! Your review is pending approval.', redirect_url)

        except Exception as e:
            _logger.exception('TR Review Error: %s', str(e))
            return self._respond(is_ajax, False, str(e), redirect_url)

    def _respond(self, is_ajax, success, message, redirect_url):
        if is_ajax:
            data = json.dumps({
                'success': success,
                'message': message if success else None,
                'error': message if not success else None,
            })
            return request.make_response(
                data, headers=[('Content-Type', 'application/json')]
            )
        # Regular form POST — redirect back to product page
        return request.redirect(redirect_url)

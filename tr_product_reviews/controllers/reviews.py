import json
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class ProductReviewController(http.Controller):

    @http.route('/shop/product/review/submit', type='http',
                auth='user', website=True, methods=['POST'], csrf=False)
    def submit_review(self, **kwargs):
        redirect_url = request.httprequest.referrer or '/shop'

        try:
            product_id = int(kwargs.get('product_id') or 0)
            rating = str(kwargs.get('rating') or '0')
            title = (kwargs.get('title') or '').strip()
            review = (kwargs.get('review') or '').strip()

            if not product_id:
                return request.redirect(redirect_url + '?review_error=Invalid+product')

            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                return request.redirect(redirect_url + '?review_error=Product+not+found')

            partner = request.env.user.partner_id

            if not title:
                return request.redirect(redirect_url + '?review_error=Title+required')

            if rating not in ('1', '2', '3', '4', '5'):
                return request.redirect(redirect_url + '?review_error=Select+a+rating')

            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                return request.redirect(redirect_url + '?review_error=Already+reviewed')

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': rating,
                'title': title,
                'review': review,
                'state': 'pending',
            })
            _logger.info('TR Review created for product %s by %s', product_id, partner.name)
            return request.redirect(redirect_url + '?review_success=1')

        except Exception as e:
            _logger.exception('TR Review Error: %s', str(e))
            return request.redirect(redirect_url + '?review_error=' + str(e)[:50])

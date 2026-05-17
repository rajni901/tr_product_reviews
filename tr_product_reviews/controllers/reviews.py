import json
import logging
from urllib.parse import urlencode

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class ProductReviewController(http.Controller):

    def _build_redirect(self, base_url, **params):
        separator = '&' if '?' in base_url else '?'
        return base_url + separator + urlencode(params)

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
                request.session['review_msg'] = ('danger', 'Invalid product.')
                return request.redirect(redirect_url)

            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                request.session['review_msg'] = ('danger', 'Product not found.')
                return request.redirect(redirect_url)

            partner = request.env.user.partner_id

            if not title:
                request.session['review_msg'] = ('warning', 'Please enter a review title.')
                return request.redirect(redirect_url)

            if rating not in ('1', '2', '3', '4', '5'):
                request.session['review_msg'] = ('warning', 'Please select a star rating.')
                return request.redirect(redirect_url)

            existing = request.env['product.review'].sudo().search([
                ('product_id', '=', product.id),
                ('partner_id', '=', partner.id),
            ], limit=1)

            if existing:
                request.session['review_msg'] = ('warning', 'You have already reviewed this product.')
                return request.redirect(redirect_url)

            request.env['product.review'].sudo().create({
                'product_id': product.id,
                'partner_id': partner.id,
                'rating': rating,
                'title': title,
                'review': review,
                'state': 'pending',
            })
            request.session['review_msg'] = ('success', 'Thank you! Your review is pending approval.')
            _logger.info('TR Review created for product %s', product_id)
            return request.redirect(redirect_url)

        except Exception as e:
            _logger.exception('TR Review Error: %s', str(e))
            request.session['review_msg'] = ('danger', str(e))
            return request.redirect(redirect_url)

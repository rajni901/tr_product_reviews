{
    'name': 'Website Product Reviews & Ratings',
    'version': '19.0.1.0.0',
    'category': 'Website/eCommerce',
    'summary': 'Allow customers to rate and review products on your Odoo eCommerce website',
    'description': """
Website Product Reviews & Ratings — by Vayu Sharma
=======================================================
Let customers rate and review your products directly on your website.

Features:
- Star rating (1-5 stars) on product pages
- Customer review with title and description
- Login required to submit review
- Admin approval before review goes live
- Average rating display on product page
- Review count display
- Backend view to manage all reviews
- Show reviewer name and date
    """,
    'author': 'Vayu Sharma',
    'website': '',
    'license': 'OPL-1',
    'depends': ['website_sale', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_review_views.xml',
        'views/product_views.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tr_product_reviews/static/src/css/reviews.css',
            'tr_product_reviews/static/src/js/reviews.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 12.00,
    'currency': 'USD',
}

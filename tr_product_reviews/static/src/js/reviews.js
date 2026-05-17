/** @odoo-module **/

import { jsonrpc } from '@web/core/network/rpc';

document.addEventListener('DOMContentLoaded', function () {
    const starInput = document.getElementById('tr_star_input');
    const ratingInput = document.getElementById('tr_rating_value');
    const form = document.getElementById('tr_review_form');
    const msgDiv = document.getElementById('tr_review_message');

    if (!starInput) return;

    const stars = starInput.querySelectorAll('.tr-star-btn');

    // Star hover and click
    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            const val = parseInt(star.dataset.value);
            stars.forEach(s => {
                s.classList.toggle('active', parseInt(s.dataset.value) <= val);
            });
        });

        star.addEventListener('click', () => {
            const val = star.dataset.value;
            ratingInput.value = val;
            stars.forEach(s => {
                s.classList.toggle('active', parseInt(s.dataset.value) <= parseInt(val));
            });
        });
    });

    starInput.addEventListener('mouseleave', () => {
        const selected = parseInt(ratingInput.value) || 0;
        stars.forEach(s => {
            s.classList.toggle('active', parseInt(s.dataset.value) <= selected);
        });
    });

    // Form submit
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const productId = document.getElementById('tr_product_id')?.value;
            const rating = ratingInput.value;
            const title = document.getElementById('tr_review_title')?.value.trim();
            const review = document.getElementById('tr_review_body')?.value.trim();
            const btn = document.getElementById('tr_submit_review');

            if (!rating || rating === '0') {
                showMsg('Please select a star rating.', 'warning');
                return;
            }
            if (!title) {
                showMsg('Please enter a review title.', 'warning');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Submitting...';

            try {
                const result = await jsonrpc('/shop/product/review/submit', {
                    product_id: productId,
                    rating: parseInt(rating),
                    title: title,
                    review: review,
                });

                if (result.success) {
                    showMsg(result.message, 'success');
                    form.reset();
                    ratingInput.value = '0';
                    stars.forEach(s => s.classList.remove('active'));
                    btn.textContent = 'Review Submitted';
                } else {
                    showMsg(result.error || 'Something went wrong.', 'danger');
                    btn.disabled = false;
                    btn.textContent = 'Submit Review';
                }
            } catch (err) {
                showMsg('Error submitting review. Please try again.', 'danger');
                btn.disabled = false;
                btn.textContent = 'Submit Review';
            }
        });
    }

    function showMsg(msg, type) {
        msgDiv.style.display = 'block';
        msgDiv.className = `mb-3 alert alert-${type}`;
        msgDiv.textContent = msg;
    }
});

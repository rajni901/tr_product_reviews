(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const form = document.getElementById('tr_review_form');
        const msgDiv = document.getElementById('tr_review_message');

        if (!form) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const productId = (document.getElementById('tr_product_id') || {}).value || '';
            const ratingInput = form.querySelector('input[name="tr_rating"]:checked');
            const rating = ratingInput ? ratingInput.value : '0';
            const title = ((document.getElementById('tr_review_title') || {}).value || '').trim();
            const review = ((document.getElementById('tr_review_body') || {}).value || '').trim();
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

            fetch('/shop/product/review/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        product_id: productId,
                        rating: parseInt(rating),
                        title: title,
                        review: review,
                    },
                }),
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                const result = data.result || {};
                if (result.success) {
                    showMsg(result.message || 'Review submitted! Pending approval.', 'success');
                    form.reset();
                    btn.textContent = 'Review Submitted';
                } else {
                    showMsg(result.error || 'Something went wrong.', 'danger');
                    btn.disabled = false;
                    btn.textContent = 'Submit Review';
                }
            })
            .catch(function () {
                showMsg('Error submitting. Please try again.', 'danger');
                btn.disabled = false;
                btn.textContent = 'Submit Review';
            });
        });

        function showMsg(msg, type) {
            if (!msgDiv) return;
            msgDiv.style.display = 'block';
            msgDiv.className = 'mb-3 alert alert-' + type;
            msgDiv.textContent = msg;
        }
    });
})();

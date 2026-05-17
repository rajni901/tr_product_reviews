(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const starInput = document.getElementById('tr_star_input');
        const ratingInput = document.getElementById('tr_rating_value');
        const form = document.getElementById('tr_review_form');
        const msgDiv = document.getElementById('tr_review_message');

        if (!starInput) return;

        const stars = starInput.querySelectorAll('.tr-star-btn');

        // Hover effect
        stars.forEach(function (star) {
            star.addEventListener('mouseover', function () {
                const val = parseInt(star.dataset.value);
                stars.forEach(function (s) {
                    s.classList.toggle('active', parseInt(s.dataset.value) <= val);
                });
            });

            // Click to select
            star.addEventListener('click', function () {
                const val = star.dataset.value;
                ratingInput.value = val;
                stars.forEach(function (s) {
                    s.classList.toggle('active', parseInt(s.dataset.value) <= parseInt(val));
                });
            });
        });

        // Keep selected stars on mouse leave
        starInput.addEventListener('mouseleave', function () {
            const selected = parseInt(ratingInput.value) || 0;
            stars.forEach(function (s) {
                s.classList.toggle('active', parseInt(s.dataset.value) <= selected);
            });
        });

        if (!form) return;

        // Form submit
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const productId = (document.getElementById('tr_product_id') || {}).value || '';
            const rating = ratingInput.value;
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
                    ratingInput.value = '0';
                    stars.forEach(function (s) { s.classList.remove('active'); });
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

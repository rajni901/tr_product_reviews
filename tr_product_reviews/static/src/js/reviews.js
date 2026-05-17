(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var form = document.getElementById('tr_review_form');
        var msgDiv = document.getElementById('tr_review_message');

        if (!form) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var productIdEl = document.getElementById('tr_product_id');
            var productId = productIdEl ? productIdEl.value : '';
            var ratingInput = form.querySelector('input[name="rating"]:checked');
            var rating = ratingInput ? ratingInput.value : '0';
            var titleEl = document.getElementById('tr_review_title');
            var bodyEl = document.getElementById('tr_review_body');
            var title = titleEl ? titleEl.value.trim() : '';
            var review = bodyEl ? bodyEl.value.trim() : '';
            var btn = document.getElementById('tr_submit_review');

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

            var formData = new FormData();
            formData.append('product_id', productId);
            formData.append('rating', rating);
            formData.append('title', title);
            formData.append('review', review);

            fetch('/shop/product/review/submit', {
                method: 'POST',
                body: formData,
            })
            .then(function (res) { return res.json(); })
            .then(function (result) {
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
            .catch(function (err) {
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

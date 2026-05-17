(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        // ── Flash Messages from URL params ──
        var params = new URLSearchParams(window.location.search);
        var success = params.get('review_success');
        var error = params.get('review_error');
        var flash = document.getElementById('tr_review_flash');
        var flashMsg = document.getElementById('tr_review_flash_msg');

        if (flash && flashMsg) {
            if (success) {
                flash.style.display = 'block';
                flashMsg.className = 'alert alert-success';
                flashMsg.textContent = '✓ Thank you! Your review has been submitted and is pending approval.';
                flash.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else if (error) {
                flash.style.display = 'block';
                flashMsg.className = 'alert alert-danger';
                flashMsg.textContent = '✗ ' + decodeURIComponent(error.replace(/\+/g, ' '));
                flash.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        // ── Review Form Submit ──
        var form = document.getElementById('tr_review_form');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            var ratingInput = form.querySelector('input[name="rating"]:checked');
            var rating = ratingInput ? ratingInput.value : '0';
            var titleEl = document.getElementById('tr_review_title');
            var title = titleEl ? titleEl.value.trim() : '';

            if (!rating || rating === '0') {
                e.preventDefault();
                if (flashMsg) {
                    flash.style.display = 'block';
                    flashMsg.className = 'alert alert-warning';
                    flashMsg.textContent = '⚠ Please select a star rating.';
                    flash.scrollIntoView({ behavior: 'smooth' });
                }
                return;
            }
            if (!title) {
                e.preventDefault();
                if (flashMsg) {
                    flash.style.display = 'block';
                    flashMsg.className = 'alert alert-warning';
                    flashMsg.textContent = '⚠ Please enter a review title.';
                    flash.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
})();

// Auto-dismiss toast after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    var toast = document.getElementById('tr_review_toast');
    if (toast) {
        setTimeout(function () {
            toast.style.transition = 'opacity 0.5s';
            toast.style.opacity = '0';
            setTimeout(function () { toast.remove(); }, 500);
        }, 5000);
    }
});

// Student-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize booking controls
    initializeBookingControls();
    
    // Initialize complaint controls
    initializeComplaintControls();
    
    // Initialize payment controls
    initializePaymentControls();
    
    // Initialize profile controls
    initializeProfileControls();
});

function initializeBookingControls() {
    // Hostel selection changes room type options
    const hostelSelect = document.getElementById('hostel_id');
    const roomTypeSelect = document.getElementById('room_type');
    
    if (hostelSelect && roomTypeSelect) {
        hostelSelect.addEventListener('change', function() {
            const hostelId = this.value;
            
            // In a full implementation, this would fetch available room types for the selected hostel
            // For the MVP, we'll just update the UI with a notification
            showAlert('Selected hostel: ' + hostelSelect.options[hostelSelect.selectedIndex].text, 'info');
        });
    }
    
    // Date validation for booking
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (startDateInput && endDateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        startDateInput.min = today;
        
        startDateInput.addEventListener('change', function() {
            // End date must be after start date
            endDateInput.min = this.value;
            
            // If end date is before new start date, reset it
            if (endDateInput.value && endDateInput.value < this.value) {
                endDateInput.value = this.value;
            }
        });
    }
    
    // Handle booking form submission
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            const resetLoading = showLoading(submitButton, 'Submitting...');
            
            // The form will submit normally as per server-side rendering approach
            // If we were using AJAX, we would prevent default and handle it here
            
            // After brief timeout, reset button state
            // This will only be visible if the form has validation errors
            setTimeout(() => {
                if (resetLoading) resetLoading();
            }, 1000);
        });
    }
}

function initializeComplaintControls() {
    // Category selection updates placeholder text
    const categorySelect = document.getElementById('category');
    const descriptionTextarea = document.getElementById('description');
    
    if (categorySelect && descriptionTextarea) {
        const placeholders = {
            'Electrical': 'Describe the electrical issue (e.g., power outage, faulty outlet)...',
            'Plumbing': 'Describe the plumbing issue (e.g., leaking tap, clogged drain)...',
            'Furniture': 'Describe the furniture issue (e.g., broken chair, damaged table)...',
            'Cleanliness': 'Describe the cleanliness issue (e.g., unclean common area, pest problem)...',
            'Security': 'Describe the security issue (e.g., broken lock, suspicious activity)...',
            'Internet': 'Describe the internet issue (e.g., slow connection, no connectivity)...',
            'Other': 'Describe your issue in detail...'
        };
        
        categorySelect.addEventListener('change', function() {
            const category = this.value;
            descriptionTextarea.placeholder = placeholders[category] || 'Describe your issue in detail...';
        });
        
        // Set initial placeholder
        const initialCategory = categorySelect.value;
        descriptionTextarea.placeholder = placeholders[initialCategory] || 'Describe your issue in detail...';
    }
    
    // Handle complaint form submission
    const complaintForm = document.getElementById('complaint-form');
    if (complaintForm) {
        complaintForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            const resetLoading = showLoading(submitButton, 'Submitting...');
            
            // The form will submit normally as per server-side rendering approach
            
            // After brief timeout, reset button state
            // This will only be visible if the form has validation errors
            setTimeout(() => {
                if (resetLoading) resetLoading();
            }, 1000);
        });
    }
}

function initializePaymentControls() {
    // Payment type affects amount field
    const paymentTypeSelect = document.getElementById('payment_type');
    const amountInput = document.getElementById('amount');
    
    if (paymentTypeSelect && amountInput) {
        const suggestedAmounts = {
            'Hostel Fee': 50000,
            'Security Deposit': 10000,
            'Late Fee': 1000,
            'Other': ''
        };
        
        paymentTypeSelect.addEventListener('change', function() {
            const paymentType = this.value;
            amountInput.value = suggestedAmounts[paymentType] || '';
        });
    }
    
    // Payment method affects transaction ID field
    const paymentMethodSelect = document.getElementById('payment_method');
    const transactionIdInput = document.getElementById('transaction_id');
    const transactionIdGroup = document.getElementById('transaction_id_group');
    
    if (paymentMethodSelect && transactionIdInput && transactionIdGroup) {
        paymentMethodSelect.addEventListener('change', function() {
            const paymentMethod = this.value;
            
            if (paymentMethod === 'Cash') {
                transactionIdGroup.style.display = 'none';
                transactionIdInput.removeAttribute('required');
            } else {
                transactionIdGroup.style.display = 'block';
                transactionIdInput.setAttribute('required', 'required');
            }
        });
        
        // Set initial state
        const initialMethod = paymentMethodSelect.value;
        if (initialMethod === 'Cash') {
            transactionIdGroup.style.display = 'none';
            transactionIdInput.removeAttribute('required');
        }
    }
    
    // Handle payment form submission
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            const resetLoading = showLoading(submitButton, 'Processing...');
            
            // The form will submit normally as per server-side rendering approach
            
            // After brief timeout, reset button state
            // This will only be visible if the form has validation errors
            setTimeout(() => {
                if (resetLoading) resetLoading();
            }, 1000);
        });
    }
}

function initializeProfileControls() {
    // Profile image upload preview
    const profileImageInput = document.getElementById('profile_image');
    const profileImagePreview = document.getElementById('profile_image_preview');
    
    if (profileImageInput && profileImagePreview) {
        profileImageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    profileImagePreview.src = e.target.result;
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Handle profile form submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            const resetLoading = showLoading(submitButton, 'Updating...');
            
            // The form will submit normally as per server-side rendering approach
            
            // After brief timeout, reset button state
            // This will only be visible if the form has validation errors
            setTimeout(() => {
                if (resetLoading) resetLoading();
            }, 1000);
        });
    }
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('student-alert-container');
    if (!alertContainer) return;
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHtml;
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

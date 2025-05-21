// Admin-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Room management functionality
    initializeRoomControls();
    
    // Application handling
    initializeApplicationControls();
    
    // Complaint management
    initializeComplaintControls();
    
    // Payment management
    initializePaymentControls();
});

function initializeRoomControls() {
    // Room availability toggle
    const availabilityToggles = document.querySelectorAll('.availability-toggle');
    
    availabilityToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const roomId = this.getAttribute('data-room-id');
            const isAvailable = this.checked;
            
            // Display the change visually
            const statusDisplay = document.querySelector(`#room-status-${roomId}`);
            if (statusDisplay) {
                statusDisplay.textContent = isAvailable ? 'Available' : 'Occupied';
                statusDisplay.className = isAvailable 
                    ? 'badge bg-success' 
                    : 'badge bg-danger';
            }
            
            // Here you would typically send an AJAX request to update the database
            // For this MVP, we're just updating the UI
            showAlert(`Room status updated to ${isAvailable ? 'available' : 'occupied'}`, 'success');
        });
    });
    
    // Room type filter
    const roomTypeFilter = document.getElementById('room-type-filter');
    if (roomTypeFilter) {
        roomTypeFilter.addEventListener('change', function() {
            const selectedType = this.value;
            const roomCards = document.querySelectorAll('.room-card');
            
            roomCards.forEach(card => {
                if (selectedType === 'all' || card.getAttribute('data-room-type') === selectedType) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Hostel filter
    const hostelFilter = document.getElementById('hostel-filter');
    if (hostelFilter) {
        hostelFilter.addEventListener('change', function() {
            const selectedHostel = this.value;
            const roomCards = document.querySelectorAll('.room-card');
            
            roomCards.forEach(card => {
                if (selectedHostel === 'all' || card.getAttribute('data-hostel-id') === selectedHostel) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

function initializeApplicationControls() {
    // Application status update
    const applicationStatusForms = document.querySelectorAll('.application-status-form');
    
    applicationStatusForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const applicationId = this.getAttribute('data-application-id');
            const statusSelect = this.querySelector('select[name="status"]');
            const notesInput = this.querySelector('textarea[name="admin_notes"]');
            
            if (!statusSelect || !notesInput) return;
            
            const status = statusSelect.value;
            const notes = notesInput.value;
            
            // Update UI
            const statusDisplay = document.querySelector(`#application-status-${applicationId}`);
            if (statusDisplay) {
                statusDisplay.textContent = status.charAt(0).toUpperCase() + status.slice(1);
                statusDisplay.className = `badge status-${status}`;
            }
            
            // Submit the form normally after updating UI
            this.submit();
        });
    });
    
    // Application search
    const applicationSearch = document.getElementById('application-search');
    if (applicationSearch) {
        applicationSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const applicationRows = document.querySelectorAll('.application-row');
            
            applicationRows.forEach(row => {
                const studentName = row.getAttribute('data-student-name').toLowerCase();
                const rollNumber = row.getAttribute('data-roll-number').toLowerCase();
                
                if (studentName.includes(searchTerm) || rollNumber.includes(searchTerm)) {
                    row.style.display = 'table-row';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

function initializeComplaintControls() {
    // Complaint status update
    const complaintStatusForms = document.querySelectorAll('.complaint-status-form');
    
    complaintStatusForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const complaintId = this.getAttribute('data-complaint-id');
            const statusSelect = this.querySelector('select[name="status"]');
            const notesInput = this.querySelector('textarea[name="admin_notes"]');
            
            if (!statusSelect || !notesInput) return;
            
            const status = statusSelect.value;
            const notes = notesInput.value;
            
            // Update UI
            const statusDisplay = document.querySelector(`#complaint-status-${complaintId}`);
            if (statusDisplay) {
                statusDisplay.textContent = status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                statusDisplay.className = `badge status-${status}`;
            }
            
            // Submit the form normally after updating UI
            this.submit();
        });
    });
    
    // Complaint filter
    const complaintFilter = document.getElementById('complaint-filter');
    if (complaintFilter) {
        complaintFilter.addEventListener('change', function() {
            const selectedStatus = this.value;
            const complaintRows = document.querySelectorAll('.complaint-row');
            
            complaintRows.forEach(row => {
                if (selectedStatus === 'all' || row.getAttribute('data-status') === selectedStatus) {
                    row.style.display = 'table-row';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Complaint category filter
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const complaintRows = document.querySelectorAll('.complaint-row');
            
            complaintRows.forEach(row => {
                if (selectedCategory === 'all' || row.getAttribute('data-category') === selectedCategory) {
                    row.style.display = 'table-row';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

function initializePaymentControls() {
    // Payment status update
    const paymentStatusButtons = document.querySelectorAll('.payment-status-btn');
    
    paymentStatusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const paymentId = this.getAttribute('data-payment-id');
            const status = this.getAttribute('data-status');
            
            // Update UI first
            const statusDisplay = document.querySelector(`#payment-status-${paymentId}`);
            if (statusDisplay) {
                statusDisplay.textContent = status.charAt(0).toUpperCase() + status.slice(1);
                statusDisplay.className = `badge status-${status}`;
            }
            
            // Here you would typically send an AJAX request to update the database
            // For this MVP, we're just updating the UI and redirecting
            window.location.href = `/admin/payment/${paymentId}/update-status/${status}`;
        });
    });
    
    // Payment filter
    const paymentFilter = document.getElementById('payment-filter');
    if (paymentFilter) {
        paymentFilter.addEventListener('change', function() {
            const selectedStatus = this.value;
            const paymentRows = document.querySelectorAll('.payment-row');
            
            paymentRows.forEach(row => {
                if (selectedStatus === 'all' || row.getAttribute('data-status') === selectedStatus) {
                    row.style.display = 'table-row';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('admin-alert-container');
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

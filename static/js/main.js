// Main JavaScript for Smart Canteen System

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Set minimum pickup time to 1 hour from now
    const pickupTimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    pickupTimeInputs.forEach(input => {
        const now = new Date();
        now.setHours(now.getHours() + 1);
        const minTime = now.toISOString().slice(0, 16);
        input.min = minTime;

        if (!input.value) {
            input.value = minTime;
        }
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
});

// Confirm before deleting
function confirmDelete(message = 'Are you sure you want to delete this?') {
    return confirm(message);
}

// Format currency
function formatCurrency(amount) {
    return '£' + parseFloat(amount).toFixed(2);
}

// Show loading spinner
function showLoading(element, text = 'Loading...') {
    element.innerHTML = `<span class="spinner"></span> ${text}`;
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(element, text) {
    element.innerHTML = text;
    element.disabled = false;
}

// Toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Real-time stock update
function updateStockDisplay(mealId, newStock) {
    const stockBadges = document.querySelectorAll(`[data-meal-id="${mealId}"] .stock-badge`);
    stockBadges.forEach(badge => {
        badge.textContent = newStock;
        if (newStock === 0) {
            badge.classList.remove('bg-success', 'bg-warning');
            badge.classList.add('bg-danger');
        } else if (newStock < 10) {
            badge.classList.remove('bg-success');
            badge.classList.add('bg-warning');
        }
    });
}

// Search functionality
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');

    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent || row.innerText;

            if (text.toLowerCase().indexOf(filter) > -1) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// Validate reservation form
function validateReservationForm(form) {
    const pickupTime = new Date(form.pickup_time.value);
    const now = new Date();
    now.setHours(now.getHours() + 1);

    if (pickupTime < now) {
        alert('Pickup time must be at least 1 hour from now');
        return false;
    }

    const quantity = parseInt(form.quantity.value);
    if (quantity < 1) {
        alert('Quantity must be at least 1');
        return false;
    }

    return true;
}

// Print reservation token
function printToken(token) {
    const printWindow = window.open('', '', 'width=400,height=300');
    printWindow.document.write(`
        <html>
        <head>
            <title>Reservation Token</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                }
                .token { 
                    font-size: 48px; 
                    font-weight: bold; 
                    padding: 20px; 
                    border: 3px solid #000; 
                    display: inline-block;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <h2>Your Reservation Token</h2>
            <div class="token">${token}</div>
            <p>Please show this token when collecting your meal</p>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

console.log('Smart Canteen System - JavaScript Loaded');

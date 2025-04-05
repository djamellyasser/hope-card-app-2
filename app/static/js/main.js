/**
 * Hope Card - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add automatic table search functionality
    const tableSearchInputs = document.querySelectorAll('.table-search-input');
    tableSearchInputs.forEach(input => {
        const tableId = input.dataset.tableTarget;
        const tableRows = document.querySelectorAll(`#${tableId} tbody tr`);
        
        input.addEventListener('input', () => {
            const searchTerm = input.value.toLowerCase();
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Patient ID validation
    const patientIdInputs = document.querySelectorAll('input[name="patient_id"]');
    patientIdInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            // Enforce only alphanumeric characters
            e.target.value = e.target.value.replace(/[^a-zA-Z0-9]/g, '');
        });
    });

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Auto-close alerts after 5 seconds
    const autoCloseAlerts = document.querySelectorAll('.alert.auto-close');
    autoCloseAlerts.forEach(alert => {
        setTimeout(() => {
            // Add fade-out class
            alert.classList.add('fade');
            
            // Remove the alert after animation completes
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}); 
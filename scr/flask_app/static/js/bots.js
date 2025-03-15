// Global variables
let currentDeleteId = null;

// Reset validation errors when modals are opened
document.addEventListener('DOMContentLoaded', function () {
    // Initialize animations for bot cards
    const botCards = document.querySelectorAll('.bot-card');
    botCards.forEach((card, index) => {
        card.classList.add('fadeInUp');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add ripple effect to all buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            createRippleEffect(e, this);
        });
    });

    // Add bounce animation to copy buttons
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const token = this.getAttribute('data-token');
            copyToClipboard(token);

            this.classList.add('bounce-animation');
            setTimeout(() => {
                this.classList.remove('bounce-animation');
            }, 1000);
        });
    });

    // Add entrance animations to modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function () {
            setTimeout(() => {
                const modalDialog = this.querySelector('.modal-dialog');
                modalDialog.classList.add('scale-in-animation');
            }, 150);
        });

        modal.addEventListener('hide.bs.modal', function () {
            const modalDialog = this.querySelector('.modal-dialog');
            modalDialog.classList.remove('scale-in-animation');
        });
    });

    // Reset validation errors when modal is opened
    document.getElementById('addBotModal').addEventListener('show.bs.modal', function () {
        resetValidationErrors('addBotForm');
        document.getElementById('botName').value = '';
        document.getElementById('botToken').value = '';
    });

    document.getElementById('editBotModal').addEventListener('show.bs.modal', function (event) {
        resetValidationErrors('editBotForm');

        const button = event.relatedTarget;
        const botId = button.getAttribute('data-bot-id');
        const botTitle = button.getAttribute('data-bot-name');
        const botToken = button.getAttribute('data-bot-token');

        document.getElementById('editBotId').value = botId;
        document.getElementById('editBotName').value = botTitle;
        document.getElementById('editBotToken').value = botToken;
    });

    document.getElementById('deleteBotModal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const botId = button.getAttribute('data-bot-id');
        const botTitle = button.getAttribute('data-bot-name');

        document.getElementById('deleteBotName').textContent = botTitle;
        document.getElementById('confirmDeleteBtn').setAttribute('data-bot-id', botId);
    });

    // Reset validation errors when input changes
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('input', function () {
            this.classList.remove('is-invalid');
            const feedbackElement = this.nextElementSibling;
            if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                feedbackElement.textContent = '';
            }
        });
    });

    // Log page view activity
    logActivity('PAGE_VIEW', 'Bots management page viewed');

    // Add Bot Form Submission
    document.getElementById('addBotForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const titleInput = document.getElementById('botName');
        const tokenInput = document.getElementById('botToken');
        const addBotBtn = document.getElementById('addBotBtn');
        const spinner = addBotBtn.querySelector('.spinner-border');

        // Validate inputs
        let isValid = true;

        if (!titleInput.value.trim()) {
            showValidationError(titleInput, 'nameError', 'Bot title is required');
            isValid = false;
        }

        if (!tokenInput.value.trim()) {
            showValidationError(tokenInput, 'tokenError', 'Bot token is required');
            isValid = false;
        }

        if (!isValid) return;

        // Show loading state
        addBotBtn.disabled = true;
        spinner.classList.remove('d-none');

        // Send request to server
        fetch('/bots', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: titleInput.value.trim(),
                token: tokenInput.value.trim()
            })
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading state
                addBotBtn.disabled = false;
                spinner.classList.add('d-none');

                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addBotModal'));
                    modal.hide();

                    // Show success message
                    showToast('successToast', 'Bot added successfully!');

                    // Reload page to show new bot
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Show error message
                    if (data.errors) {
                        if (data.errors.title) {
                            showValidationError(titleInput, 'nameError', data.errors.title);
                        }
                        if (data.errors.token) {
                            showValidationError(tokenInput, 'tokenError', data.errors.token);
                        }
                    } else {
                        showToast('errorToast', data.message || 'Failed to add bot. Please try again.');
                    }
                }
            })
            .catch(error => {
                // Hide loading state
                addBotBtn.disabled = false;
                spinner.classList.add('d-none');

                // Show error message
                showToast('errorToast', 'An error occurred. Please try again.');
                console.error('Error:', error);
            });
    });

    // Edit Bot Form Submission
    document.getElementById('editBotForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const botId = document.getElementById('editBotId').value;
        const titleInput = document.getElementById('editBotName');
        const tokenInput = document.getElementById('editBotToken');
        const editBotBtn = document.getElementById('editBotBtn');
        const spinner = editBotBtn.querySelector('.spinner-border');

        // Validate inputs
        let isValid = true;

        if (!titleInput.value.trim()) {
            showValidationError(titleInput, 'editNameError', 'Bot title is required');
            isValid = false;
        }

        if (!tokenInput.value.trim()) {
            showValidationError(tokenInput, 'editTokenError', 'Bot token is required');
            isValid = false;
        }

        if (!isValid) return;

        // Show loading state
        editBotBtn.disabled = true;
        spinner.classList.remove('d-none');

        // Send request to server
        fetch('/bots', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: botId,
                title: titleInput.value.trim(),
                token: tokenInput.value.trim()
            })
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading state
                editBotBtn.disabled = false;
                spinner.classList.add('d-none');

                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editBotModal'));
                    modal.hide();

                    // Show success message
                    showToast('successToast', 'Bot updated successfully!');

                    // Reload page to show updated bot
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    // Show error message
                    if (data.errors) {
                        if (data.errors.title) {
                            showValidationError(titleInput, 'editNameError', data.errors.title);
                        }
                        if (data.errors.token) {
                            showValidationError(tokenInput, 'editTokenError', data.errors.token);
                        }
                    } else {
                        showToast('errorToast', data.message || 'Failed to update bot. Please try again.');
                    }
                }
            })
            .catch(error => {
                // Hide loading state
                editBotBtn.disabled = false;
                spinner.classList.add('d-none');

                // Show error message
                showToast('errorToast', 'An error occurred. Please try again.');
                console.error('Error:', error);
            });
    });

    // Delete Bot Confirmation
    document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
        const botId = this.getAttribute('data-bot-id');
        const deleteBtn = this;
        const spinner = deleteBtn.querySelector('.spinner-border');

        // Show loading state
        deleteBtn.disabled = true;
        spinner.classList.remove('d-none');

        // Send request to server
        fetch(`/bots/${botId}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading state
                deleteBtn.disabled = false;
                spinner.classList.add('d-none');

                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteBotModal'));
                    modal.hide();

                    // Show success message
                    showToast('successToast', 'Bot deleted successfully!');

                    // Animate the deletion of the bot card
                    const botCard = document.querySelector(`.bot-card[data-bot-id="${botId}"]`);
                    if (botCard) {
                        const parentCol = botCard.closest('.col-md-6');
                        botCard.style.transition = 'all 0.5s ease';
                        botCard.style.transform = 'translateX(20px)';
                        botCard.style.opacity = '0';

                        setTimeout(() => {
                            parentCol.style.transition = 'all 0.3s ease';
                            parentCol.style.maxHeight = '0';
                            parentCol.style.opacity = '0';
                            parentCol.style.overflow = 'hidden';

                            setTimeout(() => {
                                // Reload page after animation
                                window.location.reload();
                            }, 300);
                        }, 500);
                    } else {
                        // Reload page if card not found
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    }
                } else {
                    // Show error message
                    showToast('errorToast', data.message || 'Failed to delete bot. Please try again.');
                }
            })
            .catch(error => {
                // Hide loading state
                deleteBtn.disabled = false;
                spinner.classList.add('d-none');

                // Show error message
                showToast('errorToast', 'An error occurred. Please try again.');
                console.error('Error:', error);
            });
    });
});

// Functions that need to be globally accessible
function prepareEditBot(id, title, token) {
    document.getElementById('editBotId').value = id;
    document.getElementById('editTitle').value = title;
    document.getElementById('editToken').value = token;

    const editModal = new bootstrap.Modal(document.getElementById('editBotModal'));
    editModal.show();
}

function confirmDeleteBot(id, title) {
    currentDeleteId = id;
    document.getElementById('deleteConfirmMessage').textContent = `Are you sure you want to delete "${title}"?`;

    const deleteModal = new bootstrap.Modal(document.getElementById('deleteBotModal'));
    deleteModal.show();
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            showToast('successToast', 'Token copied to clipboard!');

            // Log the activity
            logActivity('TOKEN_COPY', 'Bot token was copied to clipboard');
        })
        .catch(err => {
            showToast('errorToast', 'Failed to copy token');
            console.error('Could not copy text: ', err);
        });
}

function showToast(toastId, message) {
    const toastElement = document.getElementById(toastId);
    const toastBody = toastElement.querySelector('.toast-body');
    toastBody.textContent = message;

    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
}

// Helper function to show validation error
function showValidationError(inputElement, errorElementId, errorMessage) {
    inputElement.classList.add('is-invalid');
    document.getElementById(errorElementId).textContent = errorMessage;
}

// Helper function to reset validation errors
function resetValidationErrors(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.classList.remove('is-invalid');
    });

    const feedbacks = form.querySelectorAll('.invalid-feedback');
    feedbacks.forEach(feedback => {
        feedback.textContent = '';
    });
}

// Create ripple effect for buttons
function createRippleEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const circle = document.createElement('span');
    const diameter = Math.max(rect.width, rect.height);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${x - radius}px`;
    circle.style.top = `${y - radius}px`;
    circle.classList.add('ripple');

    const ripple = element.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }

    element.appendChild(circle);

    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Function to log activity
function logActivity(activityType, description) {
    fetch('/api/activities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            activity_type: activityType,
            description: description
        })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error logging activity:', data.message);
            }
        })
        .catch(error => {
            console.error('Error logging activity:', error);
        });
}

// Debug function
function logServerResponse(data) {
    console.log('Server response:', data);
    if (data.message) {
        console.log('Error message:', data.message);
    }
}

// Login page animations and interactions
document.addEventListener('DOMContentLoaded', function () {
    // Form elements animation
    const formElements = document.querySelectorAll('.form-group, .form-check, .btn-primary');

    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';

        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });

    // Password visibility toggle
    const passwordField = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');

    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function () {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);

            // Toggle icon
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    }

    // Input focus effects
    const inputs = document.querySelectorAll('.form-control');

    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('input-focused');
        });

        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('input-focused');
        });
    });

    // Button hover effect
    const loginButton = document.querySelector('.btn-primary');

    if (loginButton) {
        loginButton.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            this.style.background = `radial-gradient(circle at ${x}px ${y}px, var(--primary-color), var(--secondary-color))`;
        });

        loginButton.addEventListener('mouseleave', function () {
            this.style.background = 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))';
        });
    }

    // Form validation
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            let isValid = true;

            if (!usernameInput.value.trim()) {
                showError(usernameInput, 'Username is required');
                isValid = false;
            } else {
                clearError(usernameInput);
            }

            if (!passwordInput.value.trim()) {
                showError(passwordInput, 'Password is required');
                isValid = false;
            } else {
                clearError(passwordInput);
            }

            if (!isValid) {
                e.preventDefault();

                // Shake the form on validation error
                const formContainer = document.querySelector('.login-container');
                formContainer.classList.add('shake-animation');

                setTimeout(() => {
                    formContainer.classList.remove('shake-animation');
                }, 500);
            }
        });
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const errorElement = formGroup.querySelector('.text-danger') || document.createElement('div');

        errorElement.className = 'text-danger';
        errorElement.textContent = message;

        if (!formGroup.querySelector('.text-danger')) {
            formGroup.appendChild(errorElement);
        }

        input.classList.add('is-invalid');
    }

    function clearError(input) {
        const formGroup = input.closest('.form-group');
        const errorElement = formGroup.querySelector('.text-danger');

        if (errorElement) {
            formGroup.removeChild(errorElement);
        }

        input.classList.remove('is-invalid');
    }
}); 
document.addEventListener('DOMContentLoaded', function() {
    // Password toggle functionality
    const togglePassword = document.querySelector('.toggle-password');
    const passwordField = document.getElementById('id_password1');
    
    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Password strength indicator
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const strengthMeter = document.querySelector('.strength-meter');
            const strengthText = document.getElementById('strength-text');
            const sections = document.querySelectorAll('.strength-section');
            
            const password = this.value;
            let strength = 0;
            
            // Check password length
            if (password.length >= 8) strength += 1;
            if (password.length >= 12) strength += 1;
            
            // Check for mixed case
            if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 1;
            
            // Check for numbers
            if (/\d/.test(password)) strength += 1;
            
            // Check for special chars
            if (/[^a-zA-Z0-9]/.test(password)) strength += 1;
            
            // Update UI
            sections.forEach((section, index) => {
                section.style.backgroundColor = index < strength ? getColorForStrength(strength) : '#e9ecef';
            });
            
            strengthText.textContent = getStrengthText(strength);
            strengthText.style.color = getColorForStrength(strength);
        });
    }

    function getColorForStrength(strength) {
        if (strength < 2) return '#dc3545'; // Red
        if (strength < 4) return '#fd7e14'; // Orange
        return '#28a745'; // Green
    }

    function getStrengthText(strength) {
        if (strength < 2) return 'Weak';
        if (strength < 4) return 'Medium';
        return 'Strong';
    }

    // Form validation
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate email
            const email = document.getElementById('id_email').value;
            const emailError = document.getElementById('email-error');
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                emailError.textContent = 'Please enter a valid email address';
                emailError.style.display = 'block';
                isValid = false;
            } else {
                emailError.style.display = 'none';
            }
            
            // Validate password
            const password = document.getElementById('id_password1').value;
            const passwordError = document.getElementById('password-error');
            if (!password || password.length < 8) {
                passwordError.textContent = 'Password must be at least 8 characters';
                passwordError.style.display = 'block';
                isValid = false;
            } else {
                passwordError.style.display = 'none';
            }
            
            // Validate password confirmation
            const confirmPassword = document.getElementById('id_password2').value;
            const confirmError = document.getElementById('confirm-error');
            if (password !== confirmPassword) {
                confirmError.textContent = 'Passwords do not match';
                confirmError.style.display = 'block';
                isValid = false;
            } else {
                confirmError.style.display = 'none';
            }
            
            // Validate terms checkbox
            const terms = document.getElementById('terms');
            if (!terms.checked) {
                alert('You must agree to the terms and conditions');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});
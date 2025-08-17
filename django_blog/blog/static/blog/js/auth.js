document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = loginForm.querySelector('input[name="username"]');
            const password = loginForm.querySelector('input[name="password"]');
            
            if (!username.value.trim() || !password.value.trim()) {
                e.preventDefault();
                alert('Please fill in all fields');
            }
        });
    }
});
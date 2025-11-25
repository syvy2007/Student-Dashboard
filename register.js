document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const msg = document.getElementById('msg');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value.trim();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const confirm = document.getElementById('confirm').value;

        if (!username || !password) {
            msg.textContent = 'Username and password are required.';
            return;
        }
        if (password !== confirm) {
            msg.textContent = 'Passwords do not match.';
            return;
        }

        // Load users map from localStorage
        const usersJson = localStorage.getItem('sd_users') || '{}';
        const users = JSON.parse(usersJson);

        if (users[username]) {
            msg.textContent = 'Username already exists. Choose another.';
            return;
        }

        // Save user (note: plain text password — acceptable for demo/static project)
        users[username] = { name, password };
        localStorage.setItem('sd_users', JSON.stringify(users));

        // Create session and redirect to user dashboard
        localStorage.setItem('sd_session', username);
        window.location.href = 'user_dashboard.html';
    });
});

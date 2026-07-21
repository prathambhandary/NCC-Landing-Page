function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }

    return null;
}

async function api(url, options = {}) {

    const csrf = getCookie("csrf_access_token");

    options.credentials = "same-origin";

    options.headers = {
        ...(options.headers || {}),
        "X-CSRF-TOKEN": csrf
    };

    return fetch(url, options);
}   

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}

async function api(url, options = {}) {
    const csrf = getCookie("csrf_access_token");
    options.credentials = "same-origin";
    options.headers = {
        ...(options.headers || {}),
        "X-CSRF-TOKEN": csrf
    };
    return fetch(url, options);
}

// Check if user is logged in (for page load)
function checkAuth() {
    fetch('/api/admin/verify')
        .then(r => r.json())
        .then(data => {
            if (!data.valid) {
                window.location.href = '/admin/login';
            }
        })
        .catch(() => {
            window.location.href = '/admin/login';
        });
}

// Logout function (call from dashboard)
function logout() {
    if (!confirm('Sign out?')) return;
    fetch('/api/admin/logout', { method: 'POST' })
        .finally(() => {
            window.location.href = '/admin/login';
        });
}

// Helper to show toast (already defined in templates)
function showToast(message, type) {
    // ... existing toast logic (if not present, add it)
}
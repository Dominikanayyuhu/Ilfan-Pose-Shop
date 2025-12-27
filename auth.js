// Система аккаунтов для Ильфана
let loggedInUser = JSON.parse(localStorage.getItem('session_user')) || null;

function checkSessionTimeout() {
    const lastVisit = localStorage.getItem('last_visit_time');
    const now = new Date().getTime();
    const fourDaysInMs = 4 * 24 * 60 * 60 * 1000; 

    if (loggedInUser && lastVisit) {
        if (now - lastVisit > fourDaysInMs) {
            localStorage.removeItem('session_user');
            loggedInUser = null;
            alert("Session expired (4 days inactivity). Please login again.");
            location.reload();
        }
    }
    localStorage.setItem('last_visit_time', now);
}

function handleAuth() {
    const u = document.getElementById('auth-user').value.trim();
    const p = document.getElementById('auth-pass').value.trim();
    const currentTab = document.getElementById('tab-reg').classList.contains('active') ? 'reg' : 'login';

    if(!u || !p) return alert("Fill all fields");

    let users = JSON.parse(localStorage.getItem('site_users') || '{}');

    if(currentTab === 'reg') {
        if(users[u]) return alert("User already exists");
        users[u] = { password: p, avatar: u.charAt(0).toUpperCase() };
        localStorage.setItem('site_users', JSON.stringify(users));
        alert("Registered! Now Login.");
        switchTab('login');
    } else {
        if(users[u] && users[u].password === p) {
            loggedInUser = { name: u, avatar: users[u].avatar };
            localStorage.setItem('session_user', JSON.stringify(loggedInUser));
            localStorage.setItem('last_visit_time', new Date().getTime());
            location.reload();
        } else {
            alert("Wrong username or password");
        }
    }
}

function logout() {
    localStorage.removeItem('session_user');
    location.reload();
}

function updateUI() {
    checkSessionTimeout();
    if(loggedInUser) {
        document.getElementById('nav-username').innerText = loggedInUser.name;
        document.getElementById('nav-avatar').innerText = loggedInUser.avatar;
        document.getElementById('writing-status').innerText = "Signed in as: " + loggedInUser.name;
        if(loggedInUser.name.toLowerCase() === 'ilfan') {
            document.getElementById('rev-content-area').classList.add('admin-active');
        }
    }
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    updateUI();
});

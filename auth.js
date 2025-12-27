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
            alert("Сессия истекла (4 дня). Войдите снова.");
            location.reload();
        }
    }
    localStorage.setItem('last_visit_time', now);
}

function handleAuth() {
    const u = document.getElementById('auth-user').value.trim();
    const p = document.getElementById('auth-pass').value.trim();
    const currentTab = document.getElementById('tab-reg').classList.contains('active') ? 'reg' : 'login';

    if(!u || !p) return alert("Введите ник и пароль!");

    let users = JSON.parse(localStorage.getItem('site_users') || '{}');

    if(currentTab === 'reg') {
        if(users[u]) return alert("Такой ник уже занят!");
        users[u] = { password: p };
        localStorage.setItem('site_users', JSON.stringify(users));
        alert("Регистрация успешна! Теперь войдите.");
        if (typeof switchTab === 'function') switchTab('login');
    } else {
        if(users[u] && users[u].password === p) {
            loggedInUser = { name: u };
            localStorage.setItem('session_user', JSON.stringify(loggedInUser));
            localStorage.setItem('last_visit_time', new Date().getTime());
            location.reload();
        } else {
            alert("Неверный ник или пароль!");
        }
    }
}

function logout() {
    localStorage.removeItem('session_user');
    location.reload();
}

function updateUI() {
    checkSessionTimeout();
    // Синхронизация с кнопкой в index.html
    if (typeof syncUI === 'function') {
        syncUI(); 
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateUI();
});

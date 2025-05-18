// Check if user is logged in as admin
if (!localStorage.getItem('isLoggedInAsAdmin')) {
    // Redirect to login page
    window.location.href = '../login.html';
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Handle logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            // Clear admin login state
            localStorage.removeItem('isLoggedInAsAdmin');
            
            // Redirect to login page
            window.location.href = '../login.html';
        });
    }
}); 
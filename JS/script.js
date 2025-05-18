document.addEventListener('DOMContentLoaded', function() {
  // Initialize database if it doesn't exist
  initializeDatabase();
  
  // Mobile menu toggle
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const mobileNav = document.querySelector('.mobile-nav');
  
  if (mobileMenuBtn && mobileNav) {
    mobileMenuBtn.addEventListener('click', function() {
      mobileNav.classList.toggle('active');
      
      // Toggle icon between bars and times
      const icon = mobileMenuBtn.querySelector('i');
      if (icon.classList.contains('fa-bars')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
      } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });
  }
  
  // Theme toggle
  const themeToggleButtons = document.querySelectorAll('.theme-toggle');
  
  themeToggleButtons.forEach(button => {
    button.addEventListener('click', function() {
      document.body.classList.toggle('dark-theme');
      
      // Toggle icon between sun and moon
      const icons = document.querySelectorAll('.theme-toggle i');
      icons.forEach(icon => {
        if (icon.classList.contains('fa-sun')) {
          icon.classList.remove('fa-sun');
          icon.classList.add('fa-moon');
        } else {
          icon.classList.remove('fa-moon');
          icon.classList.add('fa-sun');
        }
      });
      
      // Save theme preference to localStorage
      const isDarkTheme = document.body.classList.contains('dark-theme');
      localStorage.setItem('darkTheme', isDarkTheme);
    });
  });
  
  // Load saved theme preference
  const savedTheme = localStorage.getItem('darkTheme');
  if (savedTheme === 'true') {
    document.body.classList.add('dark-theme');
    const icons = document.querySelectorAll('.theme-toggle i');
    icons.forEach(icon => {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-moon');
    });
  }
  
  // Authentication state handling
  function updateAuthUI() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    
    // Desktop auth buttons
    const signInBtn = document.querySelector('.sign-in-btn');
    const signUpBtn = document.querySelector('.sign-up-btn');
    const logoutBtn = document.querySelector('.logout-btn');
    
    // Mobile auth buttons
    const mobileSignIn = document.querySelector('.mobile-sign-in');
    const mobileSignUp = document.querySelector('.mobile-sign-up');
    const mobileLogout = document.querySelector('.mobile-logout');
    
    if (isLoggedIn) {
      // User is logged in - show logout button, hide login/signup
      if (signInBtn) signInBtn.style.display = 'none';
      if (signUpBtn) signUpBtn.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'inline-block';
      
      if (mobileSignIn) mobileSignIn.style.display = 'none';
      if (mobileSignUp) mobileSignUp.style.display = 'none';
      if (mobileLogout) mobileLogout.style.display = 'block';
    } else {
      // User is logged out - show login/signup, hide logout
      if (signInBtn) signInBtn.style.display = 'inline-block';
      if (signUpBtn) signUpBtn.style.display = 'inline-block';
      if (logoutBtn) logoutBtn.style.display = 'none';
      
      if (mobileSignIn) mobileSignIn.style.display = 'block';
      if (mobileSignUp) mobileSignUp.style.display = 'block';
      if (mobileLogout) mobileLogout.style.display = 'none';
    }
  }
  
  // Handle logout button click
  const logoutBtns = document.querySelectorAll('.logout-btn, .mobile-logout');
  logoutBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      // Clear authentication state
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('user');
      
      // Update UI
      updateAuthUI();
      
      // Redirect to home page
      window.location.href = 'index.html';
    });
  });
  
  // Check authentication state on page load
  updateAuthUI();

  // Category filter
  const filterButtons = document.querySelectorAll('.filter-btn');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      filterButtons.forEach(btn => btn.classList.remove('active'));
      
      // Add active class to clicked button
      this.classList.add('active');
      
      // Get category to filter by
      const category = this.dataset.category;
      
      // Filter logic would go here
      console.log('Filter by:', category);
    });
  });
});

// Database initialization
function initializeDatabase() {
  // Initialize users if they don't exist
  if (!localStorage.getItem('users')) {
    const defaultUsers = [
      {
        email: 'admin@admin.com',
        password: '1234', // In a real app, this would be hashed
        name: 'Admin User',
        role: 'admin'
      },
      {
        email: 'test@gmail.com',
        password: '5678',
        name: 'Test User',
        role: 'user'
      }
    ];
    
    localStorage.setItem('users', JSON.stringify(defaultUsers));
  }
  
  // Initialize events array if it doesn't exist
  if (!localStorage.getItem('events')) {
    localStorage.setItem('events', JSON.stringify([]));
  }
}
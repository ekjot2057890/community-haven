document.addEventListener('DOMContentLoaded', function() {
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
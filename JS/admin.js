document.addEventListener('DOMContentLoaded', function() {
  // Sidebar toggle for mobile
  const menuToggle = document.getElementById('menu-toggle');
  const adminSidebar = document.querySelector('.admin-sidebar');
  
  if (menuToggle && adminSidebar) {
    menuToggle.addEventListener('click', function() {
      adminSidebar.classList.toggle('active');
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
  
  // Select all checkbox
  const selectAllCheckbox = document.getElementById('select-all');
  const rowCheckboxes = document.querySelectorAll('.row-checkbox');
  
  if (selectAllCheckbox && rowCheckboxes.length > 0) {
    selectAllCheckbox.addEventListener('change', function() {
      rowCheckboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
      });
    });
    
    // Update select all checkbox when individual checkboxes change
    rowCheckboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
        const someChecked = Array.from(rowCheckboxes).some(cb => cb.checked);
        
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = someChecked && !allChecked;
      });
    });
  }
  
  // Modal functionality
  const viewButtons = document.querySelectorAll('.view-btn');
  const eventDetailModal = document.getElementById('event-detail-modal');
  const userDetailModal = document.getElementById('user-detail-modal');
  const closeModalButtons = document.querySelectorAll('.close-modal');
  
  if (viewButtons.length > 0) {
    viewButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Determine which modal to show based on context
        const isEventView = this.closest('tr')?.querySelector('td:nth-child(2)')?.textContent.includes('Event') || 
                           this.closest('tr')?.querySelector('td:nth-child(1)')?.textContent.includes('Event');
        
        if (isEventView && eventDetailModal) {
          eventDetailModal.classList.add('active');
        } else if (userDetailModal) {
          userDetailModal.classList.add('active');
        }
      });
    });
  }
  
  if (closeModalButtons.length > 0) {
    closeModalButtons.forEach(button => {
      button.addEventListener('click', function() {
        const modal = this.closest('.modal');
        if (modal) {
          modal.classList.remove('active');
        }
      });
    });
  }
  
  // Close modal when clicking outside
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        this.classList.remove('active');
      }
    });
  });
  
  // Action buttons functionality
  const approveButtons = document.querySelectorAll('.approve-btn');
  const rejectButtons = document.querySelectorAll('.reject-btn');
  const flagButtons = document.querySelectorAll('.flag-btn');
  const deleteButtons = document.querySelectorAll('.delete-btn');
  const verifyButtons = document.querySelectorAll('.verify-btn');
  const banButtons = document.querySelectorAll('.ban-btn');
  const unbanButtons = document.querySelectorAll('.unban-btn');
  
  // Example implementation for approve buttons
  if (approveButtons.length > 0) {
    approveButtons.forEach(button => {
      button.addEventListener('click', function() {
        const row = this.closest('tr');
        if (row) {
          const statusCell = row.querySelector('td:nth-child(6)');
          if (statusCell) {
            const statusSpan = statusCell.querySelector('.badge');
            if (statusSpan) {
              statusSpan.className = 'badge badge-success';
              statusSpan.textContent = 'Approved';
            }
          }
        }
      });
    });
  }
  
  // Example implementation for reject buttons
  if (rejectButtons.length > 0) {
    rejectButtons.forEach(button => {
      button.addEventListener('click', function() {
        const row = this.closest('tr');
        if (row) {
          const statusCell = row.querySelector('td:nth-child(6)');
          if (statusCell) {
            const statusSpan = statusCell.querySelector('.badge');
            if (statusSpan) {
              statusSpan.className = 'badge badge-danger';
              statusSpan.textContent = 'Rejected';
            }
          }
        }
      });
    });
  }
  
  // Example implementation for delete buttons
  if (deleteButtons.length > 0) {
    deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this item?')) {
          const row = this.closest('tr');
          if (row) {
            row.remove();
          }
        }
      });
    });
  }
  
  // Example implementation for verify buttons
  if (verifyButtons.length > 0) {
    verifyButtons.forEach(button => {
      button.addEventListener('click', function() {
        const row = this.closest('tr');
        if (row) {
          const statusCell = row.querySelector('td:nth-child(6)');
          if (statusCell) {
            const statusSpan = statusCell.querySelector('.badge');
            if (statusSpan) {
              statusSpan.className = 'badge badge-primary';
              statusSpan.textContent = 'Verified Organizer';
            }
          }
        }
      });
    });
  }
  
  // Example implementation for ban buttons
  if (banButtons.length > 0) {
    banButtons.forEach(button => {
      button.addEventListener('click', function() {
        if (confirm('Are you sure you want to ban this user?')) {
          const row = this.closest('tr');
          if (row) {
            const statusCell = row.querySelector('td:nth-child(6)');
            if (statusCell) {
              const statusSpan = statusCell.querySelector('.badge');
              if (statusSpan) {
                statusSpan.className = 'badge badge-danger';
                statusSpan.textContent = 'Banned';
              }
            }
          }
        }
      });
    });
  }
});
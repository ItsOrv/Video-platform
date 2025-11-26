// Force Dark Mode Only (No Toggle Button)
(function() {
    // Always apply dark theme
    const theme = 'dark';
    
    // Apply dark theme
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update meta theme-color
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.content = '#0a0a0f';
    }
    
    // Remove any existing theme toggle button
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
        toggleBtn.remove();
    }
    
    // Override any theme preference in localStorage
    localStorage.setItem('theme', 'dark');
})();


document.addEventListener('DOMContentLoaded', () => {
  const scrapeForm = document.getElementById('scrape-form');
  const loaderOverlay = document.getElementById('loader-overlay');
  const loaderText = document.getElementById('loader-text');

  if (scrapeForm && loaderOverlay && loaderText) {
    const loadingTexts = [
      "Initializing OSINT engine...",
      "Resolving network endpoints...",
      "Scraping public GitHub API...",
      "Extracting digital footprints...",
      "Compiling intelligence profiles...",
      "Formatting data structure...",
      "Writing CSV registry file..."
    ];

    scrapeForm.addEventListener('submit', (e) => {
      // Show overlay
      loaderOverlay.classList.add('active');
      
      // Rotate messages to keep the user engaged
      let textIndex = 0;
      loaderText.textContent = loadingTexts[textIndex];

      const interval = setInterval(() => {
        textIndex = (textIndex + 1) % loadingTexts.length;
        loaderText.textContent = loadingTexts[textIndex];
      }, 1200);

      // Store interval so we can clear if needed (though page will redirect anyway)
      window.scrapeInterval = interval;
    });
  }

  // Handle Delete Confirmation
  const deleteForms = document.querySelectorAll('.delete-form');
  deleteForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const targetName = form.getAttribute('data-target-name') || 'this target';
      if (!confirm(`Are you sure you want to delete the intelligence profile for "${targetName}"? This action cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });
});

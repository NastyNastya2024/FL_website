(() => {
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  // Smooth scroll for same-page links
  const links = document.querySelectorAll('a[href^="#"]');
  for (const link of links) {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href') || '';
      const id = href.startsWith('#') ? href.slice(1) : '';
      const target = id ? document.getElementById(id) : null;
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  // Contact form functionality
  const contactForm = document.getElementById('contactForm');
  const contactMessage = document.getElementById('contactMessage');
  const charCount = document.getElementById('charCount');
  
  // Character counter for message field
  if (contactMessage && charCount) {
    contactMessage.addEventListener('input', () => {
      const length = contactMessage.value.length;
      charCount.textContent = length;
      
      // Change color when approaching limit
      if (length > 900) {
        charCount.style.color = '#dc3545';
      } else if (length > 800) {
        charCount.style.color = '#ffc107';
      } else {
        charCount.style.color = '#6c757d';
      }
    });
  }
  
  // Form submission
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const submitButton = contactForm.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      
      // Show loading state
      submitButton.textContent = 'Отправка...';
      submitButton.disabled = true;
      
      try {
        const formData = new FormData(contactForm);
        
        const response = await fetch(contactForm.action, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          // Success
          alert('Спасибо за обращение! Ваше сообщение отправлено.');
          
          // Close modal
          const modal = bootstrap.Modal.getInstance(document.getElementById('contactModal'));
          if (modal) {
            modal.hide();
          }
          
          // Reset form
          contactForm.reset();
          charCount.textContent = '0';
          charCount.style.color = '#6c757d';
        } else {
          throw new Error('Ошибка отправки');
        }
      } catch (error) {
        alert('Произошла ошибка при отправке. Попробуйте еще раз.');
        console.error('Form submission error:', error);
      } finally {
        // Reset button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
      }
    });
  }
})();
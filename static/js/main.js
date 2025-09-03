const cards = document.querySelectorAll('.card');
const maxHeight = Math.max(...Array.prototype.map.call(cards, card => card.offsetHeight));
cards.forEach(card => card.style.height = `${maxHeight}px`);
/* Плавный скролл по якорям */
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});
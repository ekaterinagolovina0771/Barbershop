const cards = document.querySelectorAll('.card');
const maxHeight = Math.max(...Array.prototype.map.call(cards, card => card.offsetHeight));
cards.forEach(card => card.style.height = `${maxHeight}px`);
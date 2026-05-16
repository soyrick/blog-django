document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.detail.target.id === 'comments') {
      const container = document.querySelector('#comments');
      if (container) {
        container.lastElementChild?.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

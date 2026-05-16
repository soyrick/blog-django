function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('htmx:configRequest', function (event) {
    const token = getCookie('csrftoken');
    if (token) {
      event.detail.headers['X-CSRFToken'] = token;
    }
  });

  document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.detail.target.id === 'comments') {
      const container = document.querySelector('#comments');
      if (container) {
        container.lastElementChild?.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

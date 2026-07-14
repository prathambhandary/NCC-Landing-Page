document.addEventListener('DOMContentLoaded', function () {

  var tabs = document.querySelectorAll('.gallery-tab');
  var yearSelect = document.getElementById('yearSelect');
  var monthSelect = document.getElementById('monthSelect');
  var groupsEl = document.getElementById('galleryGroups');
  var countEl = document.getElementById('resultCount');

  var MONTH_NAMES = [
    '',
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  var state = {
    category: 'all',
    year: 'all',
    month: 'all'
  };

  function formatDate(iso) {
    if (!iso) return '';

    var parts = iso.split('-');
    var y = parts[0];
    var m = parseInt(parts[1], 10);
    var d = parseInt(parts[2], 10);

    return d + ' ' + MONTH_NAMES[m].slice(0, 3).toUpperCase() + ' ' + y;
  }

  function render(items) {
    groupsEl.innerHTML = '';

    if (!items.length) {
      var empty = document.createElement('div');
      empty.className = 'gallery-empty';
      empty.textContent =
        'No entries found for this selection. Try a different year, month or activity type.';
      groupsEl.appendChild(empty);
      countEl.textContent = '0 entries';
      return;
    }

    countEl.textContent =
      items.length + (items.length === 1 ? ' entry' : ' entries');

    items.forEach(function (item) {

      var event = document.createElement('article');
      event.className = 'gallery-event category-' + item.category;

      // Header
      var head = document.createElement('div');
      head.className = 'gallery-event-head';

      var h3 = document.createElement('h3');
      h3.textContent = item.title;
      head.appendChild(h3);

      var sub = document.createElement('span');
      sub.className = 'ge-sub';
      sub.textContent = item.subcategory || '';
      head.appendChild(sub);

      var dateStamp = document.createElement('span');
      dateStamp.className = 'log-date';
      dateStamp.textContent = formatDate(item.date);
      head.appendChild(dateStamp);

      event.appendChild(head);

      // Description
      if (item.description) {
        var desc = document.createElement('p');
        desc.className = 'ge-desc';
        desc.textContent = item.description;
        event.appendChild(desc);
      }

      // Images
      var strip = document.createElement('div');
      strip.className = 'gallery-strip';

      (item.images || []).forEach(function (img) {

        var slot = document.createElement('div');
        slot.className = 'photo-slot';

        var image = document.createElement('img');
        image.src = img.src;
        image.alt = img.note || item.title;
        image.loading = 'lazy';

        // Optional: show placeholder if image fails
        image.onerror = function () {
          this.src = '/static/images/no-image.png';
        };

        slot.appendChild(image);

        if (img.note) {
          var caption = document.createElement('p');
          caption.className = 'photo-caption';
          caption.textContent = img.note;
          slot.appendChild(caption);
        }

        strip.appendChild(slot);
      });

      event.appendChild(strip);
      groupsEl.appendChild(event);
    });
  }

  function fetchAndRender() {
    groupsEl.innerHTML =
      '<p style="font-family: var(--font-mono); color: var(--ink-soft);">Loading gallery...</p>';

    var params = new URLSearchParams(state);

    fetch('/api/gallery?' + params.toString())
      .then(function (res) {
        if (!res.ok) {
          throw new Error('Failed to load gallery');
        }
        return res.json();
      })
      .then(render)
      .catch(function () {
        groupsEl.innerHTML =
          '<div class="gallery-empty">Could not load the gallery right now. Please refresh the page.</div>';
      });
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) {
        t.classList.remove('active');
      });

      tab.classList.add('active');
      state.category = tab.getAttribute('data-category');
      fetchAndRender();
    });
  });

  yearSelect.addEventListener('change', function () {
    state.year = yearSelect.value;
    fetchAndRender();
  });

  monthSelect.addEventListener('change', function () {
    state.month = monthSelect.value;
    fetchAndRender();
  });

  fetchAndRender();
});
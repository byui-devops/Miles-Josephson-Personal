/* JDM Legacy — app.js */
(function () {
  'use strict';

  const grid        = document.getElementById('carGrid');
  const eraLabel    = document.getElementById('eraLabel');
  const carCount    = document.getElementById('carCount');
  const eraBtns     = document.querySelectorAll('.era-btn');
  const forzaToggle = document.getElementById('forzaToggle');
  const overlay     = document.getElementById('modalOverlay');
  const modalClose  = document.getElementById('modalClose');

  let currentEra   = 'all';
  let forzaOnly    = false;
  let allCars      = [];

  // ── Fetch all cars once ──────────────────────────────
  async function fetchCars() {
    try {
      const res  = await fetch('/api/cars');
      allCars    = await res.json();
      updateCounters(allCars);
      render(allCars);
    } catch (err) {
      grid.innerHTML = '<p style="color:#E8262A;padding:4rem 2rem;font-family:monospace">Failed to load vehicles. Please refresh.</p>';
    }
  }

  // ── Filter & render ──────────────────────────────────
  function applyFilters() {
    let cars = allCars;
    if (currentEra !== 'all') cars = cars.filter(c => c.era === currentEra);
    if (forzaOnly)            cars = cars.filter(c => c.forza_available);
    render(cars);
  }

  function render(cars) {
    const eraNames = { all: 'ALL ERAS', past: 'PAST — THE LEGENDS', present: 'PRESENT — THE ICONS', future: 'FUTURE — THE VISIONS' };
    eraLabel.textContent = eraNames[currentEra];
    carCount.textContent = `${cars.length} VEHICLE${cars.length !== 1 ? 'S' : ''}`;

    if (!cars.length) {
      grid.innerHTML = '<p style="color:#5A5650;padding:4rem 2rem;font-family:monospace;grid-column:1/-1">No vehicles match this filter.</p>';
      return;
    }

    grid.innerHTML = '';
    cars.forEach((car, i) => {
      const card = buildCard(car, i);
      grid.appendChild(card);
    });
  }

  // ── Build card DOM ───────────────────────────────────
  function buildCard(car, index) {
    const card = document.createElement('article');
    card.className = `car-card era-${car.era}`;
    card.style.animationDelay = `${index * 60}ms`;
    card.innerHTML = `
      <div class="card-image-wrap">
        <img class="card-image" src="${car.image_url || ''}" alt="${car.make} ${car.model}" loading="lazy" onerror="this.style.display='none'"/>
        <div class="card-overlay"></div>
        <div class="card-era-stripe"></div>
        ${car.forza_available ? '<div class="card-forza">FH6</div>' : ''}
      </div>
      <div class="card-body">
        <div class="card-era-badge">${car.era}</div>
        <div class="card-make">${car.make}</div>
        <h2 class="card-model">${car.model}</h2>
        <div class="card-meta">
          <div class="card-meta-item">
            <span class="card-meta-label">YEAR</span>
            <span class="card-meta-val">${car.year}</span>
          </div>
          <div class="card-meta-item">
            <span class="card-meta-label">POWER</span>
            <span class="card-meta-val">${car.horsepower} hp</span>
          </div>
        </div>
        <p class="card-desc">${car.description}</p>
      </div>
      <div class="card-arrow">→</div>
    `;
    card.addEventListener('click', () => openModal(car));
    return card;
  }

  // ── Counters ─────────────────────────────────────────
  function updateCounters(cars) {
    animateCount('countPast',    cars.filter(c => c.era === 'past').length);
    animateCount('countPresent', cars.filter(c => c.era === 'present').length);
    animateCount('countFuture',  cars.filter(c => c.era === 'future').length);
  }

  function animateCount(id, target) {
    const el = document.getElementById(id);
    let count = 0;
    const step = Math.ceil(target / 20);
    const timer = setInterval(() => {
      count = Math.min(count + step, target);
      el.textContent = count;
      if (count >= target) clearInterval(timer);
    }, 40);
  }

  // ── Modal ────────────────────────────────────────────
  function openModal(car) {
    document.getElementById('modalMake').textContent    = car.make;
    document.getElementById('modalModel').textContent   = car.model;
    document.getElementById('modalYear').textContent    = car.year;
    document.getElementById('modalHP').textContent      = `${car.horsepower} hp`;
    document.getElementById('modalDesc').textContent    = car.description;
    document.getElementById('modalImage').src           = car.image_url || '';
    document.getElementById('modalImage').alt           = `${car.make} ${car.model}`;
    document.getElementById('modalForzaWrap').style.display = car.forza_available ? '' : 'none';

    const badge = document.getElementById('modalEra');
    badge.textContent  = car.era.toUpperCase();
    badge.className    = `modal-era-badge ${car.era}`;

    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ── Era buttons ──────────────────────────────────────
  eraBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      eraBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentEra = btn.dataset.era;
      applyFilters();
    });
  });

  // ── Forza toggle ─────────────────────────────────────
  forzaToggle.addEventListener('change', () => {
    forzaOnly = forzaToggle.checked;
    applyFilters();
  });

  // ── Close modal ──────────────────────────────────────
  modalClose.addEventListener('click', closeModal);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  // ── Init ─────────────────────────────────────────────
  fetchCars();
})();

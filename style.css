const key = 'varisai-canteen';
const phoneKey = 'varisai-canteen-mobile';

const saveMobileNumber = value => {
  const mobile = String(value || '').trim();
  localStorage.setItem(phoneKey, mobile);
  return mobile;
};

const getSavedMobileNumber = () => String(localStorage.getItem(phoneKey) || '').trim();

const categoryMenus = {
  Breakfast: ['Idli', 'Dosa', 'Masal Dosa', 'Chapathi'],
  Beverages: ['Tea', 'Coffee', 'Boost', 'Horlicks'],
  Lunch: ['Chicken Briyani', 'Mushroom Briyani'],
  Snacks: ['Vada', 'Samosa', 'Pani Puri', 'Vada Pav']
};

const base = {
  seq: 0,
  served: 0,
  queue: [],
  current: null,
  counters: [
    { name: 'Grill Station', open: true },
    { name: 'Combo Counter', open: true },
    { name: 'Beverage Hub', open: true }
  ]
};

let s = JSON.parse(localStorage.getItem(key) || 'null') || base;
if (Array.isArray(s.counters)) {
  s.counters = s.counters.map(counter => ({
    ...counter,
    name: counter.name === 'Drink Bar' ? 'Beverage Hub' : counter.name
  }));
}
let view = 'all';

const $ = id => document.getElementById(id);
const save = () => localStorage.setItem(key, JSON.stringify(s));

function formatPrice(value) {
  const amount = Number(value ?? 0);
  return Number.isFinite(amount) ? `₹${amount.toFixed(2)}` : '₹0.00';
}

function resetSession() {
  const freshSession = JSON.parse(JSON.stringify(base));
  s = freshSession;
  localStorage.removeItem(key);
  save();
  view = 'all';

  const form = $('form');
  if (form) form.reset();

  const ticket = $('ticket');
  if (ticket) ticket.style.display = 'none';

  const defaultRadio = document.querySelector('[name=service][value="Breakfast"]');
  if (defaultRadio) defaultRadio.checked = true;
  syncMenuOptions('Breakfast');

  const phoneAlert = $('phoneAlert');
  if (phoneAlert) phoneAlert.classList.remove('show');

  const ticketNo = $('ticketNo');
  const ticketInfo = $('ticketInfo');
  const billTime = $('billTime');
  const positionText = $('position');
  const estimateText = $('estimate');
  if (ticketNo) ticketNo.textContent = '—';
  if (ticketInfo) ticketInfo.textContent = '';
  if (billTime) billTime.textContent = '';
  if (positionText) positionText.textContent = '';
  if (estimateText) estimateText.textContent = '';

  document.querySelectorAll('.tabs button').forEach(item => {
    item.classList.toggle('active', item.dataset.filter === 'all');
  });

  render();
  toast('New billing started. Queue cleared.');
}

function syncMenuOptions(category = document.querySelector('[name=service]:checked')?.value || 'Breakfast') {
  const menuSelect = $('menuItem');
  if (!menuSelect) return;

  const options = categoryMenus[category] || categoryMenus.Breakfast;
  menuSelect.innerHTML = options.map(item => `<option value="${item}">${item}</option>`).join('');
}

const escape = value =>
  String(value).replace(/[&<>\"]/g, character => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;'
  }[character]));

function toast(message) {
  const toastBox = $('toast');
  if (!toastBox) return;

  toastBox.textContent = message;
  toastBox.classList.add('show');

  clearTimeout(window.t);
  window.t = setTimeout(() => toastBox.classList.remove('show'), 3000);
}

function playAlarm() {
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;

  const audio = new AudioContext();
  [0, 0.18, 0.36].forEach((delay, index) => {
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.value = index === 1 ? 880 : 720;
    gain.gain.setValueAtTime(0.0001, audio.currentTime + delay);
    gain.gain.exponentialRampToValueAtTime(0.18, audio.currentTime + delay + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + delay + 0.16);
    oscillator.connect(gain).connect(audio.destination);
    oscillator.start(audio.currentTime + delay);
    oscillator.stop(audio.currentTime + delay + 0.18);
  });

  setTimeout(() => audio.close(), 900);
}

function openWhatsAppDM(mobile, message) {
  const cleanMobile = String(mobile || '').replace(/\D/g, '');
  if (!cleanMobile) return false;

  const url = `https://wa.me/${cleanMobile}?text=${encodeURIComponent(message)}`;
  window.open(url, '_blank', 'noopener');
  return true;
}

function showPhoneAlert(person, counter) {
  const alert = $('phoneAlert');
  const title = $('alertTitle');
  const text = $('alertMessage');

  if (!alert || !title || !text) return;

  const mobile = person.mobile || getSavedMobileNumber();
  title.textContent = `${person.token} — order ready!`;
  text.textContent = mobile
    ? `Your order for ${person.menu} is ready. A DM will be sent to ${mobile}. Please collect it at ${counter}.`
    : `Your order for ${person.menu} is ready. Please collect it at ${counter}.`;
  alert.classList.add('show');

  clearTimeout(window.alertTimer);
  window.alertTimer = setTimeout(() => alert.classList.remove('show'), 6000);
  playAlarm();
}

function call(token, counter = 'Grill Station') {
  const person = s.queue.find(item => item.token === token);
  if (!person) return;

  if (s.current && s.current.token !== person.token) {
    s.current.status = 'Ready';
  }

  person.status = 'Preparing';
  person.counter = counter;
  s.current = person;

  save();
  render();

  toast(`${person.token} is now in ${counter}`);
  showPhoneAlert(person, counter);
}

async function sendReadyNotification(person) {
  const mobile = person.mobile || getSavedMobileNumber();
  const message = 'Your order is ready';

  if (!mobile) return false;

  try {
    const response = await fetch('http://localhost:5000/api/notify-ready', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mobile, message })
    });

    const result = await response.json();
    if (!response.ok || !result.ok) {
      console.error('Backend delivery failed:', result);
      return false;
    }

    return true;
  } catch (error) {
    console.error('Backend unavailable:', error);
    return false;
  }
}

async function ready(token) {
  const person = s.queue.find(item => item.token === token);
  if (!person) return;

  person.status = 'Ready';
  person.counter = person.counter || 'Pickup Counter';
  if (s.current?.token === token) s.current = null;

  save();
  render();
  toast(`${token} is ready for pickup.`);

  const message = 'Your order is ready';
  const mobile = person.mobile || getSavedMobileNumber();

  const delivered = await sendReadyNotification(person);
  if (!delivered && mobile) {
    console.warn('Direct message delivery failed for mobile:', mobile);
  }

  showPhoneAlert(person, person.counter || 'Pickup Counter');
}

function done(token) {
  const person = s.queue.find(item => item.token === token);
  if (!person) return;

  person.status = 'Completed';
  s.served += 1;

  if (s.current?.token === token) s.current = null;

  save();
  render();
  toast(`${token} collected successfully.`);
}

function skip(token) {
  const person = s.queue.find(item => item.token === token);
  if (!person) return;

  person.status = 'Waiting';
  person.rank = Date.now() + 999999;
  person.priority = 'normal';

  if (s.current?.token === token) s.current = null;

  save();
  render();
  toast(`${token} moved to the end of the queue.`);
}

function remove(token) {
  const person = s.queue.find(item => item.token === token);
  if (!person) return;

  person.status = 'Cancelled';
  if (s.current?.token === token) s.current = null;

  save();
  render();
  toast(`${token} removed from the queue.`);
}

function render() {
  const waiting = s.queue.filter(item => item.status === 'Waiting');
  const preparing = s.queue.filter(item => item.status === 'Preparing');
  const ready = s.queue.filter(item => item.status === 'Ready');
  const openCounters = s.counters.filter(counter => counter.open).length;
  const allCountersClosed = openCounters === 0;

  const waitingEl = $('waiting');
  const prepEl = $('prep');
  const readyEl = $('ready');
  const servedEl = $('served');
  const nowEl = $('now');
  const nowNameEl = $('nowName');
  const counterEl = $('counter');
  const countersEl = $('counters');
  const listEl = $('list');
  const totalEl = $('todayTotal');
  const waitEl = $('wait');

  if (waitingEl) waitingEl.textContent = waiting.length;
  if (prepEl) prepEl.textContent = preparing.length;
  if (readyEl) readyEl.textContent = ready.length;
  if (servedEl) servedEl.textContent = s.served;
  if (waitEl) waitEl.textContent = openCounters ? `${Math.max(4, waiting.length * 3)} min` : '—';
  if (totalEl) totalEl.textContent = s.seq;

  if (allCountersClosed) {
    if (nowEl) nowEl.textContent = 'No food available';
    if (nowNameEl) nowNameEl.textContent = 'All counters are closed right now. Please come back later.';
    if (counterEl) counterEl.textContent = 'Closed';
  } else {
    if (nowEl) nowEl.textContent = s.current ? s.current.token : 'No active order';
    if (nowNameEl) nowNameEl.textContent = s.current ? `${s.current.name} • ${s.current.service}` : 'Kitchen is ready for the next order';
    if (counterEl) counterEl.textContent = s.current ? s.current.counter : '—';
  }

  if (countersEl) {
    countersEl.innerHTML = s.counters.map(counter => `
      <div class="counter-row">
        <div>
          <b>
            <i class="status-dot" style="background:${counter.open ? '#3bb38a' : '#d6d8db'}"></i>
            ${counter.name}
          </b>
          <small>${counter.open ? 'Open' : 'Closed'}</small>
        </div>
        <button class="mini-btn" onclick="toggle('${counter.name}')">
          ${counter.open ? 'Close' : 'Open'}
        </button>
      </div>
    `).join('');
  }

  const rows = s.queue
    .filter(item => {
      if (view === 'all') return item.status !== 'Cancelled';
      if (view === 'waiting') return item.status === 'Waiting';
      return item.status === 'Waiting' && item.priority === 'staffs';
    })
    .sort((a, b) => a.rank - b.rank);

  if (listEl) {
    if (allCountersClosed) {
      listEl.innerHTML = '<p class="hint" style="padding:14px 3px">No food available right now.</p>';
      return;
    }

    listEl.innerHTML = rows.length
      ? `
        <table>
          <thead>
            <tr>
              <th>Token</th>
              <th>Price</th>
              <th>Item</th>
              <th>Time</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${rows.map(item => `
              <tr>
                <td class="token">
                  ${item.token}
                  ${item.priority === 'staffs' ? '<br><span class="badge priority">Staffs</span>' : ''}
                </td>
                <td>${escape(item.name)}</td>
                <td>${escape(item.menu || item.service)}</td>
                <td>${item.createdAt || '—'}</td>
                <td><span class="badge ${item.status}">${item.status}</span></td>
                <td>
                  ${item.status === 'Waiting' ? `
                    <button class="mini-btn" onclick="call('${item.token}')">Prep</button>
                    <button class="mini-btn" onclick="remove('${item.token}')">Cancel</button>
                  ` : item.status === 'Preparing' ? `
                    <button class="mini-btn" onclick="ready('${item.token}')">Ready</button>
                    <button class="mini-btn" onclick="skip('${item.token}')">Skip</button>
                  ` : item.status === 'Ready' ? `
                    <button class="mini-btn" onclick="done('${item.token}')">Collect</button>
                  ` : ''}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `
      : '<p class="hint" style="padding:14px 3px">No orders in this view.</p>';
  }
}

window.call = call;
window.ready = ready;
window.done = done;
window.skip = skip;
window.remove = remove;
window.toggle = name => {
  const counter = s.counters.find(item => item.name === name);
  if (!counter) return;

  counter.open = !counter.open;
  save();
  render();

  toast(`${name} is now ${counter.open ? 'open' : 'closed'}`);
};

$('form').onsubmit = event => {
  event.preventDefault();

  if (s.counters.every(counter => !counter.open)) {
    toast('No food available. All counters are closed.');
    return;
  }

  const priority = $('priority').value;
  const service = document.querySelector('[name=service]:checked').value;
  const menu = $('menuItem')?.value || categoryMenus[service][0];
  const priceValue = Number(($('price')?.value ?? '').trim() || 0);
  const mobile = saveMobileNumber($('mobileNumber')?.value ?? '');
  const token = String(++s.seq);
  const createdAt = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  let rank = Date.now();

  if (priority === 'staffs') rank -= 100000000;

  const order = {
    token,
    name: formatPrice(priceValue),
    price: Number(priceValue.toFixed(2)),
    service,
    menu,
    mobile,
    priority,
    createdAt,
    status: 'Waiting',
    rank,
    counter: 'Unassigned'
  };

  s.queue.push(order);
  save();

  const position = s.queue.filter(item => item.status === 'Waiting' && item.rank <= rank).length;
  render();

  const ticket = $('ticket');
  const ticketNo = $('ticketNo');
  const ticketInfo = $('ticketInfo');
  const billTime = $('billTime');
  const positionText = $('position');
  const estimateText = $('estimate');
  const nowDate = new Date();
  const billStamp = `${nowDate.toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' })} • ${nowDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

  if (ticket) ticket.style.display = 'block';
  if (ticketNo) ticketNo.textContent = token;
  if (ticketInfo) ticketInfo.textContent = `${order.name} • ${order.service} • ${order.menu}`;
  if (billTime) billTime.textContent = `Bill time: ${billStamp}`;
  if (positionText) positionText.textContent = `Your position: ${position} in line`;
  if (estimateText) estimateText.textContent = `Estimated wait: about ${Math.ceil(position / Math.max(s.counters.filter(counter => counter.open).length, 1)) * 4} minutes`;

  event.target.reset();
  const defaultRadio = document.querySelector('[name=service][value="Breakfast"]');
  if (defaultRadio) defaultRadio.checked = true;
  syncMenuOptions('Breakfast');

  toast(`Token ${token} created. We’ll notify you when your order is ready.`);

  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }
};

document.querySelectorAll('[name="service"]').forEach(radio => {
  radio.addEventListener('change', event => syncMenuOptions(event.target.value));
});

document.querySelectorAll('.tabs button').forEach(button => {
  button.onclick = () => {
    document.querySelectorAll('.tabs button').forEach(item => item.classList.remove('active'));
    button.classList.add('active');
    view = button.dataset.filter;
    render();
  };
});

const resetButton = $('resetSession');
if (resetButton) {
  resetButton.addEventListener('click', resetSession);
}

const dateNode = $('date');
if (dateNode) {
  dateNode.textContent = new Date().toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  });
}

const mobileInput = $('mobileNumber');
if (mobileInput) {
  mobileInput.value = getSavedMobileNumber();
  mobileInput.addEventListener('input', event => saveMobileNumber(event.target.value));
}

syncMenuOptions('Breakfast');
render();

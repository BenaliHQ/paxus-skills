// Client portal — dashboard for tax docs / appointments / messages
const { useState } = React;

const PortalSidebar = ({ active, setActive }) => {
  const items = [
    { id: 'dashboard', label: 'Dashboard', icon: 'layout-dashboard' },
    { id: 'documents', label: 'Documents', icon: 'folder' },
    { id: 'tax', label: 'Tax 2025', icon: 'receipt' },
    { id: 'books', label: 'Bookkeeping', icon: 'book-open' },
    { id: 'messages', label: 'Messages', icon: 'message-circle', badge: 2 },
    { id: 'calendar', label: 'Calendar', icon: 'calendar' },
    { id: 'billing', label: 'Billing', icon: 'credit-card' },
  ];
  return (
    <aside style={{
      width: 248, flex: 'none', height: '100vh', position: 'sticky', top: 0,
      background: '#FBF7F4', borderRight: '1px solid rgba(26,18,23,0.08)',
      display: 'flex', flexDirection: 'column', padding: '20px 16px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px 24px' }}>
        <img src="../../assets/paxus-mark.svg" style={{ width: 28, height: 28 }} />
        <span style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 500, fontSize: 18, letterSpacing: '0.16em', color: '#681E44' }}>PAXUS</span>
      </div>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {items.map(it => {
          const on = active === it.id;
          return (
            <a key={it.id} onClick={() => setActive(it.id)} style={{
              cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 12px', borderRadius: 12, fontSize: 14, fontWeight: 600,
              background: on ? '#F2E8EE' : 'transparent',
              color: on ? '#681E44' : '#1A1217',
              textDecoration: 'none',
              transition: 'background 200ms',
            }}>
              <i data-lucide={it.icon} style={{ width: 18, height: 18, strokeWidth: 1.75 }}></i>
              <span style={{ flex: 1 }}>{it.label}</span>
              {it.badge && (
                <span style={{ background: '#681E44', color: '#FBF7F4', fontSize: 11, fontWeight: 700, padding: '1px 7px', borderRadius: 9999 }}>{it.badge}</span>
              )}
            </a>
          );
        })}
      </nav>
      <div style={{ marginTop: 'auto', padding: 14, borderRadius: 16, background: '#fff', boxShadow: '0 0 0 1px rgba(26,18,23,0.08)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 36, height: 36, borderRadius: '50%', background: '#681E44', color: '#FBF7F4', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 13 }}>JT</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 13, fontWeight: 700, color: '#1A1217', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>June Tanaka</div>
            <div style={{ fontSize: 11, color: '#87797F' }}>Solo plan</div>
          </div>
          <i data-lucide="settings" style={{ width: 16, height: 16, color: '#87797F' }}></i>
        </div>
      </div>
    </aside>
  );
};

const PortalTopbar = ({ title }) => (
  <div style={{
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    padding: '20px 32px', borderBottom: '1px solid rgba(26,18,23,0.08)',
    background: 'rgba(251,247,244,0.85)', backdropFilter: 'blur(12px)',
    position: 'sticky', top: 0, zIndex: 10,
  }}>
    <div>
      <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: '#681E44', marginBottom: 4 }}>Welcome back</div>
      <h1 style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: 30, lineHeight: 1.1, letterSpacing: '-0.02em', margin: 0 }}>{title}</h1>
    </div>
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <button style={{ background: 'transparent', border: 0, padding: 10, borderRadius: 9999, cursor: 'pointer' }}><i data-lucide="search" style={{ width: 18, height: 18 }}></i></button>
      <button style={{ background: 'transparent', border: 0, padding: 10, borderRadius: 9999, cursor: 'pointer', position: 'relative' }}>
        <i data-lucide="bell" style={{ width: 18, height: 18 }}></i>
        <span style={{ position: 'absolute', top: 8, right: 8, width: 7, height: 7, borderRadius: '50%', background: '#B0202A' }}></span>
      </button>
      <button className="pxs-btn" style={{ background: '#681E44', color: '#FBF7F4', border: 0, fontFamily: 'Inter', fontWeight: 600, fontSize: 14, padding: '10px 18px', borderRadius: 9999, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6, transition: 'transform 200ms' }}>
        <i data-lucide="upload" style={{ width: 16, height: 16 }}></i> Upload doc
      </button>
    </div>
  </div>
);

const StatCard = ({ label, value, hint, tone = 'default' }) => {
  const bg = { default: '#fff', blush: '#F2E8EE', ink: '#1A1217' }[tone];
  const fg = tone === 'ink' ? '#FBF7F4' : '#1A1217';
  const sub = tone === 'ink' ? '#E0D0E0' : '#87797F';
  return (
    <div style={{
      background: bg, color: fg, borderRadius: 24, padding: 24,
      boxShadow: '0 0 0 1px rgba(26,18,23,0.10)',
    }}>
      <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: '0.10em', textTransform: 'uppercase', color: tone === 'ink' ? '#E0D0E0' : '#681E44' }}>{label}</div>
      <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: 44, letterSpacing: '-0.025em', lineHeight: 1, marginTop: 14 }}>{value}</div>
      <div style={{ fontSize: 13, color: sub, marginTop: 8 }}>{hint}</div>
    </div>
  );
};

const TaxTimeline = () => {
  const steps = [
    { label: 'Engagement signed', date: 'Jan 4', state: 'done' },
    { label: 'Documents uploaded', date: 'Feb 18', state: 'done' },
    { label: 'CPA review', date: 'In progress', state: 'active' },
    { label: 'Your sign-off', date: 'Apr 3', state: 'pending' },
    { label: 'Filed with IRS', date: 'Apr 10', state: 'pending' },
  ];
  return (
    <div style={{ background: '#fff', borderRadius: 24, padding: 28, boxShadow: '0 0 0 1px rgba(26,18,23,0.10)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 24 }}>
        <div>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#681E44' }}>Your 2025 return</div>
          <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 700, fontSize: 22, marginTop: 6 }}>On track for early April filing</div>
        </div>
        <span style={{ fontSize: 11, fontWeight: 700, padding: '5px 12px', borderRadius: 9999, background: '#FBEFD9', color: '#C77A1F' }}>3 of 5</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', position: 'relative' }}>
        <div style={{ position: 'absolute', left: 14, right: 14, top: 14, height: 2, background: '#E5DDE1', zIndex: 0 }}></div>
        <div style={{ position: 'absolute', left: 14, top: 14, height: 2, width: '50%', background: '#681E44', zIndex: 1 }}></div>
        {steps.map((s, i) => (
          <div key={i} style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', width: 110 }}>
            <div style={{
              width: 28, height: 28, borderRadius: '50%',
              background: s.state === 'pending' ? '#fff' : '#681E44',
              boxShadow: s.state === 'pending' ? 'inset 0 0 0 2px #C9BFC4' : 'none',
              color: '#FBF7F4', display: 'flex', alignItems: 'center', justifyContent: 'center',
              animation: s.state === 'active' ? 'pulse 1.6s ease-in-out infinite' : 'none',
            }}>
              {s.state === 'done' && <i data-lucide="check" style={{ width: 14, height: 14 }}></i>}
              {s.state === 'active' && <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#FBF7F4' }}></span>}
            </div>
            <div style={{ fontSize: 12, fontWeight: 700, marginTop: 10, color: s.state === 'pending' ? '#87797F' : '#1A1217' }}>{s.label}</div>
            <div style={{ fontSize: 11, color: '#87797F', marginTop: 2 }}>{s.date}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const DocList = () => {
  const docs = [
    { name: 'W-2 — Acme Corp.pdf', type: 'W-2', status: 'received', date: 'Feb 18' },
    { name: '1099-NEC — Mercury.pdf', type: '1099', status: 'received', date: 'Feb 14' },
    { name: 'Schedule K-1 — Sage LLC.pdf', type: 'K-1', status: 'review', date: 'Feb 22' },
    { name: 'Mortgage interest — Wells.pdf', type: '1098', status: 'received', date: 'Feb 10' },
    { name: 'Charitable — Red Cross.pdf', type: 'Receipt', status: 'missing', date: '—' },
  ];
  const tone = { received: ['#E2F2E8', '#1F6B3A'], review: ['#FBEFD9', '#C77A1F'], missing: ['#F8E0E2', '#B0202A'] };
  const label = { received: 'Received', review: 'In review', missing: 'Missing' };
  return (
    <div style={{ background: '#fff', borderRadius: 24, padding: '8px 8px', boxShadow: '0 0 0 1px rgba(26,18,23,0.10)' }}>
      <div style={{ padding: '20px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 18 }}>Your tax documents</div>
        <a style={{ fontSize: 13, color: '#681E44', fontWeight: 600 }}>View all →</a>
      </div>
      {docs.map((d, i) => (
        <div key={i} style={{
          display: 'grid', gridTemplateColumns: '36px 1fr 90px 110px 24px', gap: 14,
          alignItems: 'center', padding: '12px 16px', borderRadius: 16,
          background: i % 2 ? '#FBF7F4' : 'transparent',
        }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: '#F2E8EE', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#681E44' }}>
            <i data-lucide="file-text" style={{ width: 16, height: 16 }}></i>
          </div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 600, color: '#1A1217' }}>{d.name}</div>
            <div style={{ fontSize: 12, color: '#87797F' }}>{d.type} · {d.date}</div>
          </div>
          <span style={{
            fontSize: 11, fontWeight: 700, padding: '4px 10px', borderRadius: 9999,
            background: tone[d.status][0], color: tone[d.status][1], justifySelf: 'start',
          }}>{label[d.status]}</span>
          <span style={{ fontSize: 12, color: '#87797F' }}>Tax 2025</span>
          <i data-lucide="more-horizontal" style={{ width: 16, height: 16, color: '#87797F' }}></i>
        </div>
      ))}
    </div>
  );
};

const NextAppt = () => (
  <div style={{ background: '#681E44', color: '#FBF7F4', borderRadius: 24, padding: 28, position: 'relative', overflow: 'hidden' }}>
    <img src="../../assets/paxus-mark.svg" style={{ position: 'absolute', right: -50, top: -30, width: 200, opacity: 0.10 }} />
    <div style={{ position: 'relative' }}>
      <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#E0D0E0' }}>Next call</div>
      <div style={{ fontFamily: 'Manrope', fontWeight: 800, fontSize: 28, lineHeight: 1.1, letterSpacing: '-0.02em', marginTop: 12 }}>Quarterly check-in</div>
      <div style={{ fontSize: 14, color: '#E0D0E0', marginTop: 8 }}>Mar 28 · 10:00 AM PT · 30 min</div>
      <div style={{ marginTop: 18, display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{ width: 32, height: 32, borderRadius: '50%', background: '#E0D0E0', color: '#681E44', fontWeight: 700, fontSize: 12, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>RA</div>
        <span style={{ fontSize: 13 }}>with Rosa Aguilar, CPA</span>
      </div>
      <div style={{ marginTop: 24, display: 'flex', gap: 8 }}>
        <button className="pxs-btn" style={{ background: '#FBF7F4', color: '#1A1217', border: 0, padding: '9px 16px', borderRadius: 9999, fontWeight: 600, fontSize: 13, cursor: 'pointer', transition: 'transform 200ms' }}>Join call</button>
        <button className="pxs-btn" style={{ background: 'transparent', color: '#FBF7F4', border: 0, padding: '9px 16px', borderRadius: 9999, fontWeight: 600, fontSize: 13, cursor: 'pointer', boxShadow: 'inset 0 0 0 1px rgba(251,247,244,0.3)', transition: 'transform 200ms' }}>Reschedule</button>
      </div>
    </div>
  </div>
);

const MessageThread = () => (
  <div style={{ background: '#fff', borderRadius: 24, padding: 24, boxShadow: '0 0 0 1px rgba(26,18,23,0.10)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
      <div style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 18 }}>From your CPA</div>
      <a style={{ fontSize: 13, color: '#681E44', fontWeight: 600 }}>Open thread →</a>
    </div>
    <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
      <div style={{ width: 36, height: 36, borderRadius: '50%', background: '#681E44', color: '#FBF7F4', fontWeight: 700, fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none' }}>RA</div>
      <div>
        <div style={{ fontSize: 13, fontWeight: 700 }}>Rosa Aguilar <span style={{ color: '#87797F', fontWeight: 500, marginLeft: 6 }}>· 2h ago</span></div>
        <div style={{ fontSize: 14, lineHeight: 1.55, marginTop: 6, color: '#1A1217' }}>
          Hey June — I noticed your Q1 estimate is sitting a bit high based on Stripe payouts.
          Want to drop it by ~$1,200 before April 15? I'll prep the voucher either way.
        </div>
      </div>
    </div>
    <div style={{ marginTop: 16, display: 'flex', gap: 8, paddingTop: 16, borderTop: '1px solid rgba(26,18,23,0.08)' }}>
      <input placeholder="Reply…" style={{ flex: 1, border: 0, background: '#FBF7F4', padding: '10px 14px', borderRadius: 9999, fontSize: 14, fontFamily: 'Inter', outline: 'none' }} />
      <button className="pxs-btn" style={{ background: '#681E44', color: '#FBF7F4', border: 0, padding: '10px 18px', borderRadius: 9999, fontWeight: 600, fontSize: 13, cursor: 'pointer' }}>Send</button>
    </div>
  </div>
);

Object.assign(window, { PortalSidebar, PortalTopbar, StatCard, TaxTimeline, DocList, NextAppt, MessageThread });

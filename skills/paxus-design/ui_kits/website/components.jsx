// Marketing site components — Wise-style structural language with Paxus plum.
// Paxus services: Bookkeeping, Advisory / Fractional CFO, Outsourced Controller.
// (Tax positioning deferred — make no tax claim either way in copy.)
const { useState } = React;

const Button = ({ variant = 'primary', size = 'md', children, onClick, leadingIcon, trailingIcon }) => {
  const sizes = {
    sm: { padding: '6px 14px', fontSize: 13 },
    md: { padding: '12px 22px', fontSize: 15 },
    lg: { padding: '16px 30px', fontSize: 17 },
  };
  const variants = {
    primary: { background: '#682145', color: '#FBF7F4' },
    secondary: { background: 'rgba(104, 33, 69,0.08)', color: '#1A1217' },
    outline: { background: 'transparent', color: '#1A1217', boxShadow: 'inset 0 0 0 1px rgba(26,18,23,0.18)' },
    ghost: { background: 'transparent', color: '#1A1217' },
    onDark: { background: '#FBF7F4', color: '#1A1217' },
    onDarkOutline: { background: 'transparent', color: '#FBF7F4', boxShadow: 'inset 0 0 0 1.5px rgba(251,247,244,0.45)' },
  };
  return (
    <button onClick={onClick} className="pxs-btn"
      style={{
        ...sizes[size], ...variants[variant],
        border: 0, cursor: 'pointer', borderRadius: 9999,
        fontFamily: 'Inter, sans-serif', fontWeight: 600,
        display: 'inline-flex', alignItems: 'center', gap: 8,
        transition: 'transform 200ms cubic-bezier(0.34,1.56,0.64,1), background 200ms',
      }}>
      {leadingIcon && <i data-lucide={leadingIcon} style={{ width: 18, height: 18 }}></i>}
      {children}
      {trailingIcon && <i data-lucide={trailingIcon} style={{ width: 18, height: 18 }}></i>}
    </button>
  );
};

const Header = ({ active, onNav, onSignIn, onCta }) => {
  const links = ['Services', 'Clients', 'Resources', 'About'];
  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 50,
      backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
      background: 'rgba(251,247,244,0.85)',
      boxShadow: '0 1px 0 rgba(26,18,23,0.06)',
    }}>
      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '14px 32px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 36 }}>
          <a onClick={() => onNav('home')} style={{ cursor: 'pointer', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
            <img src="../../assets/paxus-mark-real.png" alt="" style={{ height: 32, width: 'auto' }} />
            <span style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 500, fontSize: 22, letterSpacing: '0.16em', color: '#682145' }}>PAXUS</span>
          </a>
          <nav style={{ display: 'flex', gap: 4 }}>
            {links.map(l => (
              <a key={l} onClick={() => onNav(l.toLowerCase())}
                className="pxs-nav"
                style={{
                  cursor: 'pointer', padding: '8px 14px', borderRadius: 9999,
                  fontSize: 14, fontWeight: 600, textDecoration: 'none',
                  color: active === l.toLowerCase() ? '#682145' : '#1A1217',
                  background: active === l.toLowerCase() ? '#F7EDF3' : 'transparent',
                  transition: 'background 200ms',
                }}>{l}</a>
            ))}
          </nav>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <Button variant="ghost" size="md" onClick={onSignIn}>Sign in</Button>
          <Button variant="primary" size="md" onClick={onCta}>Book a call</Button>
        </div>
      </div>
    </header>
  );
};

const Hero = ({ onCta }) => (
  <section style={{ maxWidth: 1280, margin: '0 auto', padding: '88px 32px 56px' }}>
    <div style={{ maxWidth: 980 }}>
      <div style={{
        fontSize: 11, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase',
        color: '#682145', marginBottom: 24, fontFamily: 'Inter',
      }}>Paxus CPA · Boutique accounting + advisory</div>
      <h1 style={{
        fontFamily: 'Manrope, sans-serif', fontWeight: 800,
        fontSize: 'clamp(56px, 9vw, 112px)', lineHeight: 0.92, letterSpacing: '-0.035em',
        margin: 0, color: '#1A1217',
      }}>
        Books that<br />
        <span style={{ color: '#682145' }}>balance</span> themselves.
      </h1>
      <p style={{
        marginTop: 28, fontSize: 20, lineHeight: 1.5, maxWidth: 620,
        color: '#4A4045', fontWeight: 400, fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif',
      }}>
        A boutique CPA practice for founders, family offices, and growing companies.
        Bookkeeping, controllership, and CFO-level guidance — all from
        one team that picks up the phone.
      </p>
      <div style={{ marginTop: 36, display: 'flex', gap: 12, alignItems: 'center' }}>
        <Button variant="primary" size="lg" onClick={onCta}>Book a 20-min call</Button>
        <Button variant="outline" size="lg">See our work</Button>
      </div>
      <div style={{ marginTop: 36, display: 'flex', gap: 28, color: '#4A4045', fontSize: 14, fontWeight: 500, fontFamily: 'Inter' }}>
        <span><strong style={{ color: '#1A1217' }}>140+</strong> active clients</span>
        <span><strong style={{ color: '#1A1217' }}>4 hr</strong> avg. response</span>
        <span><strong style={{ color: '#1A1217' }}>$420M</strong> assets under books</span>
      </div>
    </div>
  </section>
);

const ServiceCard = ({ eyebrow, title, body, icon, variant = 'default' }) => {
  const styles = {
    default: { background: '#fff', color: '#1A1217' },
    blush: { background: '#F7EDF3', color: '#1A1217' },
    dark: { background: '#682145', color: '#FBF7F4' },
  };
  const s = styles[variant];
  return (
    <div className="pxs-card" style={{
      ...s, borderRadius: 32, padding: '36px 32px',
      boxShadow: '0 0 0 1px rgba(26,18,23,0.10)',
      transition: 'transform 200ms, box-shadow 200ms',
      cursor: 'pointer',
    }}>
      <div style={{
        width: 48, height: 48, borderRadius: 14,
        background: variant === 'dark' ? 'rgba(251,247,244,0.12)' : '#F7EDF3',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        marginBottom: 28,
      }}>
        <i data-lucide={icon} stroke-width="1.25" style={{ width: 22, height: 22, color: variant === 'dark' ? '#FBF7F4' : '#682145' }}></i>
      </div>
      <div style={{
        fontSize: 11, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase',
        color: variant === 'dark' ? '#ECD2E1' : '#682145',
        marginBottom: 14, fontFamily: 'Inter',
      }}>{eyebrow}</div>
      <div style={{
        fontFamily: 'Manrope, sans-serif', fontWeight: 700, fontSize: 28, lineHeight: 1.1,
        letterSpacing: '-0.02em', marginBottom: 14,
      }}>{title}</div>
      <div style={{ fontSize: 16, lineHeight: 1.55, color: variant === 'dark' ? '#ECD2E1' : '#4A4045', fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif' }}>{body}</div>
    </div>
  );
};

const Services = () => (
  <section style={{ maxWidth: 1280, margin: '0 auto', padding: '64px 32px' }}>
    <div style={{ maxWidth: 720, marginBottom: 56 }}>
      <div className="t-eyebrow" style={{ marginBottom: 20 }}>What we do</div>
      <h2 style={{
        fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: 60, lineHeight: 0.95,
        letterSpacing: '-0.03em', margin: 0,
      }}>Three practices, one team.</h2>
      <p style={{ marginTop: 18, fontSize: 18, color: '#4A4045', maxWidth: 620, fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif' }}>
        Everything your books need — from monthly close to controller-level oversight —
        handled by one senior team that actually knows your numbers.
      </p>
    </div>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
      <ServiceCard eyebrow="Bookkeeping" title="Monthly close" icon="calculator"
        body="Reconciled, categorized, and closed by the 10th. You get a one-page summary you can actually read." />
      <ServiceCard eyebrow="Fractional CFO" title="Advisory on call" icon="trending-up" variant="blush"
        body="Senior CPA for board prep, fundraises, M&A diligence, and equity comp. Hourly with a monthly cap, so the bill never surprises you." />
      <ServiceCard eyebrow="Controllership" title="Outsourced controller" icon="briefcase" variant="dark"
        body="A senior controller embedded in your finance function — month-end close, internal controls, reporting, and the team training to back it up." />
    </div>
  </section>
);

const CaseStudies = () => {
  const cases = [
    {
      tag: 'Series B SaaS · 80 employees',
      quote: '"They rebuilt three years of books in six weeks and got us through our 409A without drama. We sleep better."',
      person: 'Lena Park, COO',
      org: 'Northvale Software',
    },
    {
      tag: 'Family office · $40M AUM',
      quote: '"We replaced two legacy bookkeepers with Paxus and cut close time from 21 days to 7. Reporting we actually use."',
      person: 'Daniel Reyes, Director',
      org: 'Bay Hollow Family Office',
    },
    {
      tag: 'Nonprofit · monthly close',
      quote: '"They rebuilt our books and now the board gets clean financials every month. First time we actually trust the numbers."',
      person: 'Imani Brooks, ED',
      org: 'River Arts Collective',
    },
  ];
  return (
    <section style={{ background: '#ECD2E1', padding: '96px 0', marginTop: 64, color: '#1A1217' }}>
      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '0 32px' }}>
        <div style={{ maxWidth: 720, marginBottom: 56 }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.16em', textTransform: 'uppercase', color: '#682145', marginBottom: 18, fontFamily: 'Inter' }}>The work</div>
          <h2 style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: 60, lineHeight: 0.95, letterSpacing: '-0.03em', margin: 0, color: '#1A1217' }}>What this looks like, in practice.</h2>
          <p style={{ marginTop: 18, fontSize: 18, color: '#4A4045', maxWidth: 620, fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif' }}>
            A few of the engagements we're proudest of. Names changed where requested; numbers verified.
          </p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18 }}>
          {cases.map((c, i) => (
            <div key={i} className="pxs-card" style={{
              background: '#FFFFFF',
              color: '#1A1217',
              borderRadius: 32, padding: '32px 28px',
              boxShadow: i === 1 ? '0 12px 32px -12px rgba(104, 33, 69,0.25), 0 0 0 1px rgba(104, 33, 69,0.18)' : '0 0 0 1px rgba(26,18,23,0.08)',
              transform: i === 1 ? 'translateY(-12px)' : 'none',
              transition: 'transform 200ms',
              display: 'flex', flexDirection: 'column', gap: 20,
              position: 'relative',
            }}>
              {i === 1 && <span style={{ position: 'absolute', top: -10, left: 24, background: '#682145', color: '#FBF7F4', fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', padding: '5px 12px', borderRadius: 9999, fontFamily: 'Inter' }}>Featured</span>}
              <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.10em', textTransform: 'uppercase', color: '#682145', fontFamily: 'Inter' }}>{c.tag}</span>
              <div style={{ fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif', fontSize: 20, lineHeight: 1.45, fontWeight: 400 }}>{c.quote}</div>
              <div style={{ marginTop: 'auto', paddingTop: 16, borderTop: '1px solid rgba(26,18,23,0.10)' }}>
                <div style={{ fontSize: 14, fontWeight: 700, fontFamily: 'Inter' }}>{c.person}</div>
                <div style={{ fontSize: 13, color: '#87797F', fontFamily: 'Inter' }}>{c.org}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 48, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
          <span style={{ fontFamily: 'Inter', fontSize: 13, color: '#4A4045', letterSpacing: '0.04em' }}>Trusted by teams at</span>
          <div style={{ display: 'flex', gap: 36 }}>
            {['Northvale', 'Bay Hollow', 'Civic Atlas', 'River Arts', 'Tessera Labs'].map(n =>
              <span key={n} style={{ fontFamily: 'Manrope', fontWeight: 700, fontSize: 16, letterSpacing: '0.08em', color: '#682145' }}>{n.toUpperCase()}</span>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

const CtaBlock = () => (
  <section style={{ maxWidth: 1280, margin: '64px auto', padding: '0 32px' }}>
    <div style={{
      position: 'relative', overflow: 'hidden',
      background: '#682145', color: '#FBF7F4',
      borderRadius: 48, padding: '88px 64px',
    }}>
      <img src="../../assets/paxus-mark-cream.png" alt=""
        style={{ position: 'absolute', right: 32, top: '50%', transform: 'translateY(-50%)', width: 280, opacity: 0.08, pointerEvents: 'none' }} />
      <div style={{ maxWidth: 720, position: 'relative' }}>
        <h2 style={{
          fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: 72, lineHeight: 0.92,
          letterSpacing: '-0.035em', margin: 0, color: '#FFFFFF',
        }}>Let's get coffee<br />and your books in order.</h2>
        <p style={{ marginTop: 24, fontSize: 19, color: '#F7EDF3', maxWidth: 540, fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif', lineHeight: 1.5 }}>
          A 20-minute intro call. No pitch, no pressure. We'll tell you whether we're a fit
          — and if not, who is.
        </p>
        <div style={{ marginTop: 36, display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <Button variant="onDark" size="lg">Book a call</Button>
          <Button variant="onDarkOutline" size="lg">Email the team</Button>
        </div>
      </div>
    </div>
  </section>
);

const Footer = () => (
  <footer style={{ background: '#682145', color: '#FBF7F4', padding: '64px 32px 32px' }}>
    <div style={{ maxWidth: 1280, margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: 40, paddingBottom: 48, borderBottom: '1px solid rgba(251,247,244,0.18)' }}>
        <div>
          <img src="../../assets/paxus-logo-cream.png" alt="Paxus" style={{ height: 60, width: 'auto' }} />
          <p style={{ marginTop: 16, fontSize: 14, maxWidth: 320, lineHeight: 1.6, fontFamily: 'Inter, "Helvetica Neue", Arial, sans-serif', color: '#F7EDF3' }}>
            Paxus CPA, PLLC. Licensed in California, Oregon, and Washington.
            Independent member of the AICPA.
          </p>
        </div>
        {[
          { h: 'Services', l: ['Bookkeeping', 'Fractional CFO', 'Outsourced controller'] },
          { h: 'Company', l: ['About', 'Team', 'Careers', 'Contact'] },
          { h: 'Clients', l: ['Case studies', 'Industries', 'Sign in', 'Refer a friend'] },
        ].map(c => (
          <div key={c.h}>
            <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#FFFFFF', marginBottom: 16, fontFamily: 'Inter' }}>{c.h}</div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 10 }}>
              {c.l.map(x => <li key={x}><a style={{ color: '#F7EDF3', textDecoration: 'none', fontSize: 14, fontFamily: 'Inter' }}>{x}</a></li>)}
            </ul>
          </div>
        ))}
      </div>
      <div style={{ paddingTop: 28, display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#ECD2E1', fontFamily: 'Inter' }}>
        <span>© 2026 Paxus CPA, PLLC</span>
        <span>Privacy · Terms · Engagement letter</span>
      </div>
    </div>
  </footer>
);

Object.assign(window, { Button, Header, Hero, Services, CaseStudies, CtaBlock, Footer });

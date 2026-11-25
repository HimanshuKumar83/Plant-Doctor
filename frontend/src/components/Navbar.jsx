import { Leaf, History, RotateCcw, Store } from 'lucide-react';

const Navbar = ({ apiStatus, historyCount, onScrollToHistory, onScrollToStores, onResetScan }) => {
  const isHealthy = apiStatus?.status === 'ok';

  return (
    <nav
      className="glass-card no-print"
      style={{
        borderRadius: '1rem',
        padding: '0.85rem 1.35rem',
        marginBottom: '1.25rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.75rem',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div
          style={{
            background: 'linear-gradient(135deg, var(--primary-dark), var(--primary))',
            padding: '0.5rem',
            borderRadius: '0.65rem',
            display: 'flex',
          }}
        >
          <Leaf size={22} color="white" />
        </div>
        <div>
          <span
            style={{
              fontSize: '1.35rem',
              fontWeight: 800,
              fontFamily: 'Outfit, sans-serif',
              background: 'linear-gradient(to right, #ffffff, #a7f3d0)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Plant Doctor
          </span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '50%',
                background: isHealthy ? '#34d399' : '#f59e0b',
                display: 'inline-block',
              }}
            />
            <span>
              {isHealthy
                ? `Engine Ready (${apiStatus?.model?.backend?.toUpperCase() || 'CNN'})`
                : 'Connecting to API...'}
            </span>
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
        <button type="button" onClick={onScrollToStores} className="btn-secondary">
          <Store size={16} />
          <span>Nearby Stores</span>
        </button>

        <button type="button" onClick={onScrollToHistory} className="btn-secondary">
          <History size={16} />
          <span>History ({historyCount})</span>
        </button>

        <button type="button" onClick={onResetScan} className="btn-primary">
          <RotateCcw size={16} />
          <span>New Scan</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;

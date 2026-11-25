import { Clock, Trash2 } from 'lucide-react';

const HistoryCard = ({ history, onClearHistory }) => {
  return (
    <div id="history-section" className="glass-card animate-fade-in no-print">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Clock size={20} style={{ color: 'var(--text-muted)' }} />
          <span>Recent Scans</span>
        </h3>
        {history.length > 0 && (
          <button
            type="button"
            onClick={onClearHistory}
            className="btn-secondary"
            style={{ padding: '0.35rem 0.65rem', fontSize: '0.76rem' }}
          >
            <Trash2 size={13} />
            <span>Clear</span>
          </button>
        )}
      </div>

      {!history || history.length === 0 ? (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
          Your last 10 leaf diagnoses will appear here for quick reference.
        </p>
      ) : (
        <div style={{ display: 'grid', gap: '0.7rem' }}>
          {history.map((item, index) => (
            <div
              key={index}
              style={{
                background: 'var(--surface)',
                padding: '0.8rem 0.95rem',
                borderRadius: '0.8rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '0.75rem',
              }}
            >
              <div>
                <p style={{ fontWeight: 600, fontSize: '0.9rem' }}>{item.disease}</p>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {item.crop} • {item.location || 'Local'} • {item.date}
                </p>
              </div>
              <span
                style={{
                  fontSize: '0.82rem',
                  color: item.confidence > 0.75 ? 'var(--primary-light)' : 'var(--accent)',
                  fontWeight: 700,
                }}
              >
                {(item.confidence * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryCard;

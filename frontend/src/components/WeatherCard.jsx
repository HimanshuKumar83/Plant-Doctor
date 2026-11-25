import { Cloud, Thermometer, Droplets, CloudRain, Zap, RefreshCw } from 'lucide-react';

const WeatherCard = ({ weather, loading, error, onRetry }) => {
  return (
    <div className="glass-card animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Cloud size={20} style={{ color: 'var(--secondary)' }} />
          <span>3-Day Local Weather Risk</span>
        </h3>
        {onRetry && (
          <button type="button" onClick={onRetry} className="btn-secondary no-print" style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}>
            <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            <span>Refresh</span>
          </button>
        )}
      </div>

      {error && (
        <div className="alert-banner alert-warn">
          <span>{error} Diagnosis will still work using offline agronomy rules.</span>
        </div>
      )}

      {!weather && !error && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading local weather forecast...</p>
      )}

      {weather && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem' }}>
            <div style={{ background: 'var(--surface)', padding: '0.85rem', borderRadius: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
                <Thermometer size={15} />
                <span style={{ fontSize: '0.76rem' }}>Avg Temp</span>
              </div>
              <p style={{ fontSize: '1.2rem', fontWeight: 700 }}>{weather.avg_temperature}°C</p>
            </div>

            <div style={{ background: 'var(--surface)', padding: '0.85rem', borderRadius: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
                <Droplets size={15} />
                <span style={{ fontSize: '0.76rem' }}>Avg Humidity</span>
              </div>
              <p style={{ fontSize: '1.2rem', fontWeight: 700 }}>{weather.avg_humidity}%</p>
            </div>

            <div style={{ background: 'var(--surface)', padding: '0.85rem', borderRadius: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
                <CloudRain size={15} />
                <span style={{ fontSize: '0.76rem' }}>3-Day Rain</span>
              </div>
              <p style={{ fontSize: '1.2rem', fontWeight: 700 }}>{weather.total_rain_mm} mm</p>
            </div>

            <div style={{ background: 'var(--surface)', padding: '0.85rem', borderRadius: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', marginBottom: '0.3rem' }}>
                <Zap size={15} />
                <span style={{ fontSize: '0.76rem' }}>Spread Risk</span>
              </div>
              <span className={`badge badge-${weather.risk_level}`}>{weather.risk_level}</span>
            </div>
          </div>

          <p style={{ marginTop: '0.9rem', fontSize: '0.86rem', color: '#cbd5e1' }}>
            {weather.risk_text}
          </p>
        </>
      )}
    </div>
  );
};

export default WeatherCard;

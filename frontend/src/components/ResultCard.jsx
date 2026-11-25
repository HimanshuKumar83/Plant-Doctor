import { Activity, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';

const ResultCard = ({ predictionResult, onSelectCandidate }) => {
  if (!predictionResult || !predictionResult.predictions?.length) return null;

  const { predictions, low_confidence, crop_mismatch, crop_filtered_suggestion } = predictionResult;
  const best = predictions[0];
  const confidencePct = (best.confidence * 100).toFixed(1);

  return (
    <div
      className="glass-card animate-fade-in"
      style={{
        borderLeft: `4px solid ${best.is_healthy ? 'var(--primary)' : 'var(--accent)'}`,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.9rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Activity size={20} style={{ color: 'var(--primary)' }} />
          <span>Diagnosis Results</span>
        </h3>
        <span className={`badge ${best.is_healthy ? 'badge-low' : 'badge-moderate'}`}>
          {best.is_healthy ? 'Healthy Leaf' : 'Disease Detected'}
        </span>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.55rem', marginBottom: '0.3rem' }}>{best.friendly_name}</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Model Confidence:{' '}
            <strong style={{ color: best.confidence >= 0.7 ? 'var(--primary-light)' : '#fcd34d' }}>
              {confidencePct}%
            </strong>
          </p>
        </div>

        <div>
          {best.confidence >= 0.75 ? (
            <CheckCircle size={42} style={{ color: 'var(--primary-light)', opacity: 0.85 }} />
          ) : (
            <ShieldAlert size={42} style={{ color: 'var(--accent)', opacity: 0.85 }} />
          )}
        </div>
      </div>

      {low_confidence && (
        <div className="alert-banner alert-warn" style={{ marginTop: '1rem' }}>
          <AlertTriangle size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
          <span>
            Confidence is below 60%. For higher accuracy, retake the photo closer to a single leaf in bright, even daylight with minimal background clutter.
          </span>
        </div>
      )}

      {crop_mismatch && crop_filtered_suggestion && (
        <div className="alert-banner alert-warn" style={{ marginTop: '0.85rem', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <strong>Crop hint mismatch:</strong> You selected a different crop, while the closest match for your selected crop is{' '}
            <strong>
              {crop_filtered_suggestion.friendly_name} ({(crop_filtered_suggestion.confidence * 100).toFixed(1)}%)
            </strong>.
          </div>
          {onSelectCandidate && (
            <button
              type="button"
              className="btn-secondary"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              onClick={() => onSelectCandidate(crop_filtered_suggestion)}
            >
              Use This Advice Instead
            </button>
          )}
        </div>
      )}

      <div style={{ marginTop: '1.25rem' }}>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.55rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Top 3 Predictions
        </p>
        <div style={{ display: 'grid', gap: '0.55rem' }}>
          {predictions.map((item) => {
            const pct = (item.confidence * 100).toFixed(1);
            return (
              <div key={item.class_name}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.86rem', marginBottom: '0.2rem' }}>
                  <span>{item.friendly_name}</span>
                  <span style={{ fontWeight: 600 }}>{pct}%</span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${Math.min(100, item.confidence * 100)}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, var(--primary-dark), var(--primary-light))',
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ResultCard;

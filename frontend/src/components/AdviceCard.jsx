import { useState } from 'react';
import {
  Sparkles,
  FileDown,
  FlaskConical,
  Leaf,
  ShieldCheck,
  AlertCircle,
  ShoppingBag,
  Store,
} from 'lucide-react';

const AdviceCard = ({ structuredAdvice, onFindStoresForDiagnosis }) => {
  const [lang, setLang] = useState('english'); // english | hindi

  if (!structuredAdvice) return null;

  const current = structuredAdvice[lang] || structuredAdvice.english;
  const isHindi = lang === 'hindi';
  const shoppingItems = structuredAdvice.shopping_items || [];
  const storeCategories = structuredAdvice.store_categories || [];

  return (
    <div className="glass-card animate-fade-in">
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '0.75rem',
          marginBottom: '1rem',
        }}
      >
        <div>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={20} style={{ color: 'var(--accent)' }} />
            <span>{isHindi ? 'स्मार्ट उपचार योजना' : 'Smart Treatment Plan'}</span>
          </h3>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Source:{' '}
            {structuredAdvice.source === 'gemini'
              ? 'Gemini Weather-Aware AI'
              : 'Offline Agronomy Knowledge Base'}
          </span>
        </div>

        <div className="no-print" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
          <div className="lang-toggle" role="group" aria-label="Language switcher">
            <button
              type="button"
              className={`lang-btn ${lang === 'english' ? 'active' : ''}`}
              onClick={() => setLang('english')}
            >
              English
            </button>
            <button
              type="button"
              className={`lang-btn ${lang === 'hindi' ? 'active' : ''}`}
              onClick={() => setLang('hindi')}
            >
              हिंदी
            </button>
          </div>

          <button
            type="button"
            onClick={() => window.print()}
            className="btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}
          >
            <FileDown size={15} />
            <span>Save / Print PDF</span>
          </button>
        </div>
      </div>

      {/* Summary */}
      <div
        style={{
          background: 'rgba(16, 185, 129, 0.09)',
          border: '1px solid rgba(16, 185, 129, 0.25)',
          borderRadius: '0.9rem',
          padding: '0.95rem 1rem',
          marginBottom: '1rem',
          fontSize: '0.95rem',
          color: '#ecfdf5',
        }}
      >
        {current.summary}
      </div>

      {/* Shopping list CTA for nearby stores */}
      {shoppingItems.length > 0 && (
        <div
          style={{
            background: 'rgba(56, 189, 248, 0.08)',
            border: '1px solid rgba(56, 189, 248, 0.25)',
            borderRadius: '0.9rem',
            padding: '0.9rem 1rem',
            marginBottom: '1rem',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.65rem', marginBottom: '0.55rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 700, color: '#bae6fd' }}>
              <ShoppingBag size={16} />
              {isHindi ? 'दुकान से क्या खरीदें:' : 'What to Ask For at the Agro Store:'}
            </span>
            {onFindStoresForDiagnosis && (
              <button
                type="button"
                className="btn-primary no-print"
                style={{ padding: '0.4rem 0.85rem', fontSize: '0.8rem' }}
                onClick={() => onFindStoresForDiagnosis(storeCategories[0] || 'all')}
              >
                <Store size={14} />
                <span>{isHindi ? 'नजदीकी दुकान देखें' : 'Find Nearest Store'}</span>
              </button>
            )}
          </div>
          <div className="chip-row">
            {shoppingItems.map((item, idx) => (
              <span key={idx} className="chip active" style={{ cursor: 'default' }}>
                {item}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Structured 4-card breakdown */}
      <div className="advice-grid">
        <div className="advice-section">
          <h4>
            <FlaskConical size={16} />
            <span>{isHindi ? 'रासायनिक नियंत्रण (समूह व समय)' : 'Chemical Control (Active Group & Timing)'}</span>
          </h4>
          <ul>
            {current.chemical.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="advice-section">
          <h4>
            <Leaf size={16} />
            <span>{isHindi ? 'जैविक, गोबर खाद व प्राकृतिक उपचार' : 'Organic, Manure & Biological Options'}</span>
          </h4>
          <ul>
            {current.organic.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="advice-section">
          <h4>
            <ShieldCheck size={16} />
            <span>{isHindi ? 'मिट्टी सुधार और रोकथाम' : 'Soil Correction & Preventive Care'}</span>
          </h4>
          <ul>
            {current.prevention.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="advice-section">
          <h4>
            <AlertCircle size={16} style={{ color: 'var(--accent)' }} />
            <span style={{ color: '#fcd34d' }}>{isHindi ? 'किसान सुरक्षा व सावधानियाँ' : 'Safety & PPE Precautions'}</span>
          </h4>
          <ul>
            {current.safety.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AdviceCard;

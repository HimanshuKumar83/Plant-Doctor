import { ShieldCheck, CloudSun, MapPin, Languages } from 'lucide-react';

const Hero = () => {
  return (
    <section className="hero-section animate-fade-in no-print">
      <h1 className="hero-title">
        Smart Crop Disease Diagnosis <br />
        &amp; Nearest Agro-Store Finder
      </h1>
      <p className="hero-subtitle">
        Upload or capture a leaf photo to detect 38 crop conditions, get weather- and soil-aware
        treatment in English &amp; Hindi, and locate nearby pesticide, fertilizer, and manure shops.
      </p>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1.5rem',
          marginTop: '1.75rem',
          flexWrap: 'wrap',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--primary-light)', fontSize: '0.92rem' }}>
          <ShieldCheck size={18} />
          <span>91.2% Validated Accuracy • 14 Crops</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--secondary)', fontSize: '0.92rem' }}>
          <CloudSun size={18} />
          <span>Live Weather &amp; Soil pH Rules</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--accent)', fontSize: '0.92rem' }}>
          <Languages size={18} />
          <span>English + हिंदी Advice</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: '#c4b5fd', fontSize: '0.92rem' }}>
          <MapPin size={18} />
          <span>Free Nearby Krishi Store Map</span>
        </div>
      </div>
    </section>
  );
};

export default Hero;

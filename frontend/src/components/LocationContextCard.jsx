import { useState } from 'react';
import axios from 'axios';
import { MapPin, Crosshair, Search, Sprout, Loader2 } from 'lucide-react';

const DEFAULT_CROPS = [
  'Auto-detect from leaf',
  'Apple',
  'Bell Pepper',
  'Blueberry',
  'Cherry',
  'Corn',
  'Grape',
  'Orange',
  'Peach',
  'Potato',
  'Raspberry',
  'Soybean',
  'Squash',
  'Strawberry',
  'Tomato',
];

const QUICK_CITIES = [
  { name: 'Delhi', lat: 28.7041, lon: 77.1025 },
  { name: 'Lucknow', lat: 26.8467, lon: 80.9462 },
  { name: 'Pune', lat: 18.5204, lon: 73.8567 },
  { name: 'Bengaluru', lat: 12.9716, lon: 77.5946 },
  { name: 'Bhopal', lat: 23.2599, lon: 77.4126 },
];

const LocationContextCard = ({
  apiBase,
  location,
  onLocationChange,
  cropData,
  onCropDataChange,
  crops,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [gpsLoading, setGpsLoading] = useState(false);
  const [locMsg, setLocMsg] = useState('');

  const cropList = crops && crops.length > 0 ? ['Auto-detect from leaf', ...crops] : DEFAULT_CROPS;

  const useBrowserGps = () => {
    if (!navigator.geolocation) {
      setLocMsg('GPS is not supported by this browser. Search your village/city below.');
      return;
    }
    setGpsLoading(true);
    setLocMsg('');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        onLocationChange({
          lat: Number(pos.coords.latitude.toFixed(5)),
          lon: Number(pos.coords.longitude.toFixed(5)),
          label: 'Current GPS Location',
        });
        setSearchResults([]);
        setGpsLoading(false);
      },
      () => {
        setLocMsg('Location permission denied or unavailable. Search your town/PIN code below.');
        setGpsLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const handleGeocodeSearch = async (e) => {
    e.preventDefault();
    if (searchQuery.trim().length < 2) return;
    setSearching(true);
    setLocMsg('');
    try {
      const res = await axios.get(`${apiBase}/geocode`, { params: { q: searchQuery.trim() } });
      const results = res.data.results || [];
      setSearchResults(results);
      if (results.length === 0) {
        setLocMsg('No matching place found. Try adding district or state name.');
      }
    } catch {
      setLocMsg('Location search unavailable right now. Use quick cities or GPS.');
    } finally {
      setSearching(false);
    }
  };

  const soilBadge =
    cropData.soil_pH <= 0
      ? { text: 'Unknown', cls: 'badge-moderate' }
      : cropData.soil_pH < 5.5
      ? { text: 'Acidic (Needs Lime)', cls: 'badge-high' }
      : cropData.soil_pH > 7.5
      ? { text: 'Alkaline (Needs Sulfur)', cls: 'badge-high' }
      : { text: 'Optimal Range', cls: 'badge-low' };

  return (
    <div className="glass-card animate-fade-in no-print">
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
        <Sprout size={20} style={{ color: 'var(--primary)' }} />
        <span>2. Farm Location &amp; Crop Context</span>
      </h3>

      {/* Location selector */}
      <div
        style={{
          background: 'rgba(255,255,255,0.03)',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: '0.9rem',
          padding: '0.9rem',
          marginBottom: '1rem',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.65rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem' }}>
            <MapPin size={15} style={{ color: 'var(--primary-light)' }} />
            <strong>{location.label}</strong>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
              ({location.lat.toFixed(3)}, {location.lon.toFixed(3)})
            </span>
          </div>

          <button type="button" onClick={useBrowserGps} className="btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }} disabled={gpsLoading}>
            {gpsLoading ? <Loader2 size={14} className="animate-spin" /> : <Crosshair size={14} />}
            <span>{gpsLoading ? 'Locating...' : 'Use Exact GPS'}</span>
          </button>
        </div>

        <form onSubmit={handleGeocodeSearch} style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            type="text"
            className="form-input"
            placeholder="Search village, city, or PIN code (e.g., Nashik 422001)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="btn-primary" style={{ padding: '0.55rem 0.9rem' }} disabled={searching}>
            {searching ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
          </button>
        </form>

        {locMsg && <p style={{ fontSize: '0.78rem', color: '#fcd34d', marginTop: '0.5rem' }}>{locMsg}</p>}

        {searchResults.length > 0 && (
          <div style={{ marginTop: '0.6rem', display: 'grid', gap: '0.35rem' }}>
            {searchResults.map((item, idx) => (
              <button
                key={idx}
                type="button"
                className="btn-secondary"
                style={{ justifyContent: 'flex-start', textAlign: 'left', fontSize: '0.78rem', padding: '0.45rem 0.65rem' }}
                onClick={() => {
                  onLocationChange({
                    lat: item.lat,
                    lon: item.lon,
                    label: item.display_name.split(',').slice(0, 2).join(', '),
                  });
                  setSearchResults([]);
                  setSearchQuery('');
                }}
              >
                <MapPin size={13} style={{ flexShrink: 0, color: 'var(--primary-light)' }} />
                <span>{item.display_name}</span>
              </button>
            ))}
          </div>
        )}

        <div className="chip-row" style={{ marginTop: '0.65rem' }}>
          {QUICK_CITIES.map((c) => (
            <button
              key={c.name}
              type="button"
              className={`chip ${location.label === c.name ? 'active' : ''}`}
              onClick={() => onLocationChange({ lat: c.lat, lon: c.lon, label: c.name })}
            >
              {c.name}
            </button>
          ))}
        </div>
      </div>

      {/* Crop details */}
      <div style={{ display: 'grid', gap: '0.85rem' }}>
        <div>
          <label className="form-label" htmlFor="crop-select">Crop Type</label>
          <select
            id="crop-select"
            className="form-select"
            value={cropData.crop_name}
            onChange={(e) => onCropDataChange({ ...cropData, crop_name: e.target.value })}
          >
            {cropList.map((crop) => (
              <option key={crop} value={crop}>
                {crop}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem' }}>
          <div>
            <label className="form-label" htmlFor="age-input">Plant Age (Weeks)</label>
            <input
              id="age-input"
              type="number"
              min="0"
              max="200"
              className="form-input"
              value={cropData.plant_age_weeks}
              onChange={(e) =>
                onCropDataChange({
                  ...cropData,
                  plant_age_weeks: Math.max(0, Number.parseInt(e.target.value, 10) || 0),
                })
              }
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label className="form-label" htmlFor="ph-input">Soil pH</label>
              <span className={`badge ${soilBadge.cls}`} style={{ fontSize: '0.65rem', padding: '0.1rem 0.45rem', marginBottom: '0.25rem' }}>
                {soilBadge.text}
              </span>
            </div>
            <input
              id="ph-input"
              type="number"
              min="0"
              max="14"
              step="0.1"
              className="form-input"
              value={cropData.soil_pH}
              onChange={(e) =>
                onCropDataChange({
                  ...cropData,
                  soil_pH: Math.min(14, Math.max(0, Number.parseFloat(e.target.value) || 0)),
                })
              }
            />
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
            <label className="form-label" htmlFor="spray-range" style={{ marginBottom: 0 }}>
              Chemical Sprays This Season
            </label>
            <span style={{ fontSize: '0.82rem', fontWeight: 700, color: cropData.spray_count >= 3 ? '#fcd34d' : 'var(--primary-light)' }}>
              {cropData.spray_count} {cropData.spray_count >= 3 ? '(Rotate group!)' : ''}
            </span>
          </div>
          <input
            id="spray-range"
            type="range"
            min="0"
            max="10"
            value={cropData.spray_count}
            onChange={(e) =>
              onCropDataChange({
                ...cropData,
                spray_count: Number.parseInt(e.target.value, 10) || 0,
              })
            }
            style={{ width: '100%', accentColor: 'var(--primary)' }}
          />
        </div>
      </div>
    </div>
  );
};

export default LocationContextCard;

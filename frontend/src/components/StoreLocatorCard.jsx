import { useEffect, useMemo, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Store, Navigation, Phone, Clock, ExternalLink, RefreshCw } from 'lucide-react';

const CATEGORY_TABS = [
  { id: 'all', label: 'All Agro Stores' },
  { id: 'pesticides', label: 'Pesticides' },
  { id: 'fertilizers', label: 'Fertilizers' },
  { id: 'manure', label: 'Manure / Organic' },
  { id: 'seeds', label: 'Seeds' },
];

const StoreLocatorCard = ({
  location,
  storesData,
  loading,
  error,
  category,
  onCategoryChange,
  radiusKm,
  onRadiusChange,
  onRefresh,
  recommendedItems,
}) => {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);

  const stores = useMemo(() => storesData?.stores || [], [storesData]);
  const fallbackSearches = storesData?.fallback_searches || [];

  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: [28.7041, 77.1025],
      zoom: 12,
      scrollWheelZoom: false,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    const layer = L.layerGroup().addTo(map);
    mapInstanceRef.current = map;
    markersLayerRef.current = layer;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
      markersLayerRef.current = null;
    };
  }, []);

  useEffect(() => {
    const map = mapInstanceRef.current;
    const layer = markersLayerRef.current;
    if (!map || !layer) return;

    layer.clearLayers();

    const userIcon = L.divIcon({
      className: 'custom-user-pin',
      html: `<div style="width:16px;height:16px;border-radius:50%;background:#38bdf8;border:3px solid #ffffff;box-shadow:0 0 12px rgba(56,189,248,0.9);"></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
    });

    L.marker([location.lat, location.lon], { icon: userIcon })
      .bindPopup(`<strong>Your Location</strong><br/>${location.label}`)
      .addTo(layer);

    L.circle([location.lat, location.lon], {
      radius: radiusKm * 1000,
      color: '#10b981',
      fillColor: '#10b981',
      fillOpacity: 0.06,
      weight: 1,
    }).addTo(layer);

    const bounds = [[location.lat, location.lon]];

    stores.forEach((store) => {
      const storeIcon = L.divIcon({
        className: 'custom-store-pin',
        html: `<div style="width:14px;height:14px;border-radius:50%;background:#10b981;border:2px solid #ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.5);"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],
      });

      const popupHtml = `
        <div style="font-family:Inter,sans-serif;min-width:160px;color:#0f172a;">
          <strong>${store.name}</strong><br/>
          <span style="font-size:12px;color:#475569;">${store.distance_km} km away</span><br/>
          <a href="${store.directions_url}" target="_blank" rel="noopener noreferrer" style="color:#059669;font-weight:600;font-size:12px;">Open Directions →</a>
        </div>
      `;

      L.marker([store.lat, store.lon], { icon: storeIcon }).bindPopup(popupHtml).addTo(layer);
      bounds.push([store.lat, store.lon]);
    });

    if (bounds.length > 1) {
      map.fitBounds(bounds, { padding: [30, 30], maxZoom: 14 });
    } else {
      map.setView([location.lat, location.lon], 12);
    }
  }, [location, stores, radiusKm]);

  return (
    <div id="nearby-stores-section" className="glass-card animate-fade-in">
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '0.75rem',
          marginBottom: '0.9rem',
        }}
      >
        <div>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Store size={20} style={{ color: 'var(--primary-light)' }} />
            <span>Nearby Pesticide, Fertilizer &amp; Manure Stores</span>
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Showing stores within {radiusKm} km of {location.label} (Free OpenStreetMap directory)
          </p>
        </div>

        <div className="no-print" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <select
            aria-label="Search radius"
            className="form-select"
            style={{ width: 'auto', padding: '0.4rem 0.7rem', fontSize: '0.82rem' }}
            value={radiusKm}
            onChange={(e) => onRadiusChange(Number(e.target.value))}
          >
            <option value={5}>5 km</option>
            <option value={12}>12 km</option>
            <option value={25}>25 km</option>
          </select>
          <button
            type="button"
            onClick={onRefresh}
            className="btn-secondary"
            style={{ padding: '0.4rem 0.7rem', fontSize: '0.82rem' }}
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {recommendedItems && recommendedItems.length > 0 && (
        <div
          style={{
            marginBottom: '0.9rem',
            padding: '0.65rem 0.85rem',
            borderRadius: '0.75rem',
            background: 'rgba(16, 185, 129, 0.09)',
            border: '1px solid rgba(16, 185, 129, 0.22)',
            fontSize: '0.82rem',
            color: '#d1fae5',
          }}
        >
          <strong>Recommended for current crop:</strong> {recommendedItems.join(' • ')}
        </div>
      )}

      {/* Category filters */}
      <div className="chip-row no-print" style={{ marginBottom: '0.95rem' }}>
        {CATEGORY_TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={`chip ${category === tab.id ? 'active' : ''}`}
            onClick={() => onCategoryChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Map */}
      <div ref={mapContainerRef} className="store-map-box no-print" />

      {error && (
        <div className="alert-banner alert-warn" style={{ marginBottom: '0.9rem' }}>
          <span>{error}</span>
        </div>
      )}

      {storesData?.warning && (
        <div className="alert-banner alert-warn" style={{ marginBottom: '0.9rem' }}>
          <span>{storesData.warning}</span>
        </div>
      )}

      {/* Store list */}
      {loading ? (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Searching nearby agricultural stores...</p>
      ) : stores.length > 0 ? (
        <div className="store-list">
          {stores.map((store) => (
            <div key={store.id} className="store-item">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.75rem' }}>
                <div>
                  <h4 style={{ fontSize: '1rem', color: '#f8fafc', marginBottom: '0.2rem' }}>{store.name}</h4>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{store.address}</p>
                </div>
                <span className="badge badge-low" style={{ flexShrink: 0 }}>
                  {store.distance_km} km
                </span>
              </div>

              <div className="chip-row">
                {store.categories.map((cat) => (
                  <span
                    key={cat}
                    style={{
                      fontSize: '0.7rem',
                      padding: '0.18rem 0.55rem',
                      borderRadius: '9999px',
                      background: 'rgba(255,255,255,0.06)',
                      color: '#cbd5e1',
                      textTransform: 'capitalize',
                    }}
                  >
                    {cat}
                  </span>
                ))}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.15rem' }}>
                <div style={{ display: 'flex', gap: '0.85rem', flexWrap: 'wrap', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  {store.phone && (
                    <a href={`tel:${store.phone}`} style={{ color: 'var(--secondary)', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Phone size={13} />
                      {store.phone}
                    </a>
                  )}
                  {store.opening_hours && (
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Clock size={13} />
                      {store.opening_hours}
                    </span>
                  )}
                </div>

                <a
                  href={store.directions_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary no-print"
                  style={{ padding: '0.4rem 0.8rem', fontSize: '0.78rem' }}
                >
                  <Navigation size={13} />
                  <span>Directions</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div
          style={{
            padding: '1rem',
            borderRadius: '0.85rem',
            background: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(255,255,255,0.08)',
            fontSize: '0.86rem',
            color: 'var(--text-muted)',
          }}
        >
          No tagged stores found inside {radiusKm} km in OpenStreetMap for this filter. Try expanding the radius to 25 km or open direct local map searches below:
        </div>
      )}

      {/* Always-available Google Maps deep-links (no API key needed) */}
      {fallbackSearches.length > 0 && (
        <div className="no-print" style={{ marginTop: '1rem', paddingTop: '0.9rem', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
          <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', marginBottom: '0.55rem' }}>
            Direct Google Maps Quick Searches (works in every village &amp; town):
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {fallbackSearches.map((item, idx) => (
              <a
                key={idx}
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary"
                style={{ fontSize: '0.78rem', padding: '0.45rem 0.8rem' }}
              >
                <ExternalLink size={13} />
                <span>{item.label}</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default StoreLocatorCard;

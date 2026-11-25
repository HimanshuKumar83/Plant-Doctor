import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ImageCapture from './components/ImageCapture';
import LocationContextCard from './components/LocationContextCard';
import WeatherCard from './components/WeatherCard';
import ResultCard from './components/ResultCard';
import AdviceCard from './components/AdviceCard';
import StoreLocatorCard from './components/StoreLocatorCard';
import HistoryCard from './components/HistoryCard';

const API_BASE =
  import.meta.env.VITE_API_URL !== undefined
    ? import.meta.env.VITE_API_URL
    : import.meta.env.PROD
    ? ''
    : 'http://localhost:8000';

function loadInitialHistory() {
  try {
    const saved = localStorage.getItem('diagnosis_history');
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}

function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [crops, setCrops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [diagError, setDiagError] = useState('');
  const [resetSignal, setResetSignal] = useState(0);

  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherError, setWeatherError] = useState('');

  const [predictionResult, setPredictionResult] = useState(null);
  const [structuredAdvice, setStructuredAdvice] = useState(null);

  const [location, setLocation] = useState({
    lat: 28.7041,
    lon: 77.1025,
    label: 'Delhi',
  });

  const [cropData, setCropData] = useState({
    crop_name: 'Auto-detect from leaf',
    plant_age_weeks: 6,
    soil_pH: 7.0,
    spray_count: 0,
  });

  const [storesData, setStoresData] = useState(null);
  const [storesLoading, setStoresLoading] = useState(false);
  const [storesError, setStoresError] = useState('');
  const [storeCategory, setStoreCategory] = useState('all');
  const [radiusKm, setRadiusKm] = useState(12);

  const [history, setHistory] = useState(loadInitialHistory);

  useEffect(() => {
    axios
      .get(`${API_BASE}/health`)
      .then((res) => {
        setApiStatus(res.data);
        if (res.data?.supported_crops) {
          setCrops(res.data.supported_crops);
        }
      })
      .catch(() => setApiStatus({ status: 'offline' }));

    if (navigator.permissions && navigator.geolocation) {
      navigator.permissions
        .query({ name: 'geolocation' })
        .then((perm) => {
          if (perm.state === 'granted') {
            navigator.geolocation.getCurrentPosition((pos) => {
              setLocation({
                lat: Number(pos.coords.latitude.toFixed(5)),
                lon: Number(pos.coords.longitude.toFixed(5)),
                label: 'GPS Location',
              });
            });
          }
        })
        .catch(() => {});
    }
  }, []);

  const loadWeather = useCallback(async (lat, lon) => {
    setWeatherLoading(true);
    setWeatherError('');
    try {
      const res = await axios.get(`${API_BASE}/weather`, { params: { lat, lon } });
      setWeather(res.data);
    } catch {
      setWeatherError('Could not fetch live weather forecast.');
    } finally {
      setWeatherLoading(false);
    }
  }, []);

  const loadStores = useCallback(async (lat, lon, radius, category) => {
    setStoresLoading(true);
    setStoresError('');
    try {
      const res = await axios.get(`${API_BASE}/stores/nearby`, {
        params: { lat, lon, radius_km: radius, category },
      });
      setStoresData(res.data);
    } catch {
      setStoresError('Could not load nearby stores from OpenStreetMap right now.');
    } finally {
      setStoresLoading(false);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    axios
      .get(`${API_BASE}/weather`, { params: { lat: location.lat, lon: location.lon } })
      .then((res) => {
        if (!cancelled) {
          setWeather(res.data);
          setWeatherError('');
        }
      })
      .catch(() => {
        if (!cancelled) setWeatherError('Could not fetch live weather forecast.');
      });
    return () => {
      cancelled = true;
    };
  }, [location.lat, location.lon]);

  useEffect(() => {
    let cancelled = false;
    axios
      .get(`${API_BASE}/stores/nearby`, {
        params: { lat: location.lat, lon: location.lon, radius_km: radiusKm, category: storeCategory },
      })
      .then((res) => {
        if (!cancelled) {
          setStoresData(res.data);
          setStoresError('');
        }
      })
      .catch(() => {
        if (!cancelled) setStoresError('Could not load nearby stores from OpenStreetMap right now.');
      });
    return () => {
      cancelled = true;
    };
  }, [location.lat, location.lon, radiusKm, storeCategory]);

  const saveToHistory = (entry) => {
    setHistory((prev) => {
      const updated = [entry, ...prev].slice(0, 10);
      localStorage.setItem('diagnosis_history', JSON.stringify(updated));
      return updated;
    });
  };

  const fetchRecommendation = async (candidate, currentWeather) => {
    const effectiveCrop =
      cropData.crop_name === 'Auto-detect from leaf' ? candidate.crop : cropData.crop_name;

    const recData = new FormData();
    recData.append('class_name', candidate.class_name);
    recData.append('friendly_name', candidate.friendly_name);
    recData.append('crop_name', effectiveCrop);
    recData.append('plant_age_weeks', String(cropData.plant_age_weeks));
    recData.append('soil_pH', String(cropData.soil_pH));
    recData.append('spray_count', String(cropData.spray_count));

    if (currentWeather) {
      recData.append('avg_temp', String(currentWeather.avg_temperature));
      recData.append('avg_humidity', String(currentWeather.avg_humidity));
      recData.append('total_rain', String(currentWeather.total_rain_mm));
      recData.append('risk_text', currentWeather.risk_text);
    }

    const recRes = await axios.post(`${API_BASE}/recommend`, recData);
    setStructuredAdvice(recRes.data.structured);
    return recRes.data.structured;
  };

  const handleDiagnosis = async (imageFile) => {
    setLoading(true);
    setDiagError('');
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      if (cropData.crop_name !== 'Auto-detect from leaf') {
        formData.append('crop_name', cropData.crop_name);
      }

      const predRes = await axios.post(`${API_BASE}/predict`, formData);
      setPredictionResult(predRes.data);

      const best = predRes.data.predictions[0];
      const advice = await fetchRecommendation(best, weather);

      if (advice?.store_categories?.length > 0) {
        setStoreCategory('all');
      }

      saveToHistory({
        date: new Date().toLocaleDateString(),
        disease: best.friendly_name,
        confidence: best.confidence,
        crop: cropData.crop_name === 'Auto-detect from leaf' ? best.crop : cropData.crop_name,
        location: location.label,
      });
    } catch (err) {
      const msg = err.response?.data?.detail || 'Diagnosis failed. Check backend connection and try again.';
      setDiagError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCandidate = async (candidate) => {
    setLoading(true);
    setDiagError('');
    try {
      await fetchRecommendation(candidate, weather);
    } catch {
      setDiagError('Could not update treatment plan for selected crop.');
    } finally {
      setLoading(false);
    }
  };

  const scrollToElement = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const handleResetScan = () => {
    setPredictionResult(null);
    setStructuredAdvice(null);
    setDiagError('');
    setResetSignal((n) => n + 1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="app-container">
      <Navbar
        apiStatus={apiStatus}
        historyCount={history.length}
        onScrollToHistory={() => scrollToElement('history-section')}
        onScrollToStores={() => scrollToElement('nearby-stores-section')}
        onResetScan={handleResetScan}
      />

      {!predictionResult && <Hero />}

      {diagError && (
        <div className="alert-banner alert-error" style={{ marginBottom: '1.25rem' }}>
          <span>{diagError}</span>
        </div>
      )}

      <main className="main-grid">
        <div className="column-stack">
          <ImageCapture
            key={resetSignal}
            onImageCaptured={handleDiagnosis}
            isLoading={loading}
          />

          {predictionResult && (
            <ResultCard
              predictionResult={predictionResult}
              onSelectCandidate={handleSelectCandidate}
            />
          )}

          {structuredAdvice && (
            <AdviceCard
              structuredAdvice={structuredAdvice}
              onFindStoresForDiagnosis={(suggestedCat) => {
                setStoreCategory(suggestedCat || 'all');
                scrollToElement('nearby-stores-section');
              }}
            />
          )}

          <StoreLocatorCard
            location={location}
            storesData={storesData}
            loading={storesLoading}
            error={storesError}
            category={storeCategory}
            onCategoryChange={setStoreCategory}
            radiusKm={radiusKm}
            onRadiusChange={setRadiusKm}
            onRefresh={() => loadStores(location.lat, location.lon, radiusKm, storeCategory)}
            recommendedItems={structuredAdvice?.shopping_items}
          />
        </div>

        <div className="column-stack">
          <LocationContextCard
            apiBase={API_BASE}
            location={location}
            onLocationChange={setLocation}
            cropData={cropData}
            onCropDataChange={setCropData}
            crops={crops}
          />

          <WeatherCard
            weather={weather}
            loading={weatherLoading}
            error={weatherError}
            onRetry={() => loadWeather(location.lat, location.lon)}
          />

          <HistoryCard
            history={history}
            onClearHistory={() => {
              setHistory([]);
              localStorage.removeItem('diagnosis_history');
            }}
          />
        </div>
      </main>

      <footer
        className="no-print"
        style={{
          marginTop: '3rem',
          textAlign: 'center',
          padding: '1.5rem 0 0',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          color: 'var(--text-muted)',
          fontSize: '0.85rem',
        }}
      >
        <p>Plant Doctor • CNN Leaf Diagnostics, Weather Intelligence &amp; OpenStreetMap Agro Store Finder</p>
      </footer>
    </div>
  );
}

export default App;

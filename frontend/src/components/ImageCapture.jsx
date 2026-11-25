import { useState, useRef, useEffect } from 'react';
import { Camera, Upload, RefreshCw, X, Check, Image as ImageIcon } from 'lucide-react';

const ImageCapture = ({ onImageCaptured, isLoading }) => {
  const [mode, setMode] = useState('choice'); // choice, camera, preview
  const [previewUrl, setPreviewUrl] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [cameraError, setCameraError] = useState('');

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const startCamera = async () => {
    setCameraError('');
    setMode('camera');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch {
      setCameraError('Could not access camera. Please allow camera permission or upload an image file.');
      setMode('choice');
    }
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || !video.videoWidth) return;

    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      (blob) => {
        if (!blob) return;
        const file = new File([blob], 'leaf_capture.jpg', { type: 'image/jpeg' });
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        stopCamera();
        setMode('preview');
      },
      'image/jpeg',
      0.92
    );
  };

  const acceptFile = (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setCameraError('Please select a valid image file (JPG, PNG, or WebP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setCameraError('Image is larger than 10 MB. Please choose a smaller photo.');
      return;
    }
    setCameraError('');
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setMode('preview');
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    acceptFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer?.files?.[0];
    acceptFile(file);
  };

  const reset = () => {
    stopCamera();
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setSelectedFile(null);
    setPreviewUrl(null);
    setCameraError('');
    setMode('choice');
  };

  const handleConfirm = () => {
    if (selectedFile) {
      onImageCaptured(selectedFile);
    }
  };

  return (
    <div className="glass-card animate-fade-in no-print">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Camera size={20} style={{ color: 'var(--primary)' }} />
          <span>1. Leaf Scanner</span>
        </h3>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          Clear, single-leaf photo in daylight works best
        </span>
      </div>

      {cameraError && (
        <div className="alert-banner alert-error" style={{ marginBottom: '1rem' }}>
          <span>{cameraError}</span>
        </div>
      )}

      {mode === 'choice' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          <button type="button" onClick={startCamera} className="upload-zone">
            <Camera size={32} style={{ color: 'var(--primary)' }} />
            <span style={{ fontWeight: 600 }}>Take Live Photo</span>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Use phone or webcam</span>
          </button>

          <label
            className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
          >
            <Upload size={32} style={{ color: 'var(--secondary)' }} />
            <span style={{ fontWeight: 600 }}>Upload or Drop Image</span>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>JPG, PNG, WebP (max 10 MB)</span>
            <input
              type="file"
              accept="image/jpeg,image/png,image/webp,image/*"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </label>
        </div>
      )}

      {mode === 'camera' && (
        <div style={{ position: 'relative' }}>
          <video ref={videoRef} autoPlay playsInline className="camera-preview" />
          <div
            style={{
              position: 'absolute',
              bottom: '1rem',
              left: 0,
              right: 0,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: '1rem',
            }}
          >
            <button type="button" onClick={reset} className="btn-secondary" style={{ background: 'rgba(239,68,68,0.85)' }}>
              <X size={18} />
              <span>Cancel</span>
            </button>
            <button
              type="button"
              onClick={capturePhoto}
              className="btn-primary"
              aria-label="Capture photo"
              style={{
                width: '3.75rem',
                height: '3.75rem',
                borderRadius: '50%',
                padding: 0,
              }}
            >
              <div style={{ width: '1.8rem', height: '1.8rem', border: '3px solid white', borderRadius: '50%' }} />
            </button>
          </div>
          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>
      )}

      {mode === 'preview' && previewUrl && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ position: 'relative', display: 'inline-block', width: '100%' }}>
            <img
              src={previewUrl}
              alt="Leaf preview"
              style={{
                width: '100%',
                borderRadius: '0.9rem',
                maxHeight: '340px',
                objectFit: 'contain',
                background: 'rgba(0,0,0,0.35)',
              }}
            />
            {selectedFile && (
              <span
                style={{
                  position: 'absolute',
                  top: '0.65rem',
                  right: '0.65rem',
                  background: 'rgba(0,0,0,0.68)',
                  padding: '0.25rem 0.6rem',
                  borderRadius: '0.5rem',
                  fontSize: '0.75rem',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.3rem',
                }}
              >
                <ImageIcon size={13} />
                {selectedFile.name}
              </span>
            )}
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '0.85rem', marginTop: '1.1rem', flexWrap: 'wrap' }}>
            <button type="button" onClick={reset} className="btn-secondary" disabled={isLoading}>
              <RefreshCw size={16} />
              <span>Change Photo</span>
            </button>
            <button type="button" onClick={handleConfirm} className="btn-primary" disabled={isLoading}>
              {isLoading ? <RefreshCw size={16} className="animate-spin" /> : <Check size={16} />}
              <span>{isLoading ? 'Analyzing Leaf & Weather...' : 'Diagnose & Get Plan'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageCapture;

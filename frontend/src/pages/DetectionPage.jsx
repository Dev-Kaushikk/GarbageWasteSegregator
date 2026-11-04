/**
 * Waste Detection Page
 * AI-Based Smart Garbage Waste Segregator
 * Flagship operational workspace supporting Upload, Live Webcam Scanning,
 * Audio Voice Assistance, Eco-Impact Metrics, and Printable Audit Certificates.
 */
import React, { useState, useEffect, useRef } from 'react';
import {
  ScanLine,
  Upload,
  Image as ImageIcon,
  Camera,
  CameraOff,
  Volume2,
  VolumeX,
  Printer,
  FileText,
  RotateCcw,
  Sparkles,
  Info,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  Play,
  Square,
  ShieldAlert,
  ArrowRight,
  Eye,
  Layers,
  Leaf
} from 'lucide-react';
import {
  detectWaste,
  getSampleImages,
  getSampleImageUrl,
  getModelInfo,
  switchModel
} from '../services/api';
import { DISPOSAL_BADGES } from '../utils/constants';
import EcoImpactCard from '../components/EcoImpactCard';
import AuditCertificateModal from '../components/AuditCertificateModal';
import MaterialDossierModal from '../components/MaterialDossierModal';

const DetectionPage = () => {
  // Input Modes: 'upload' or 'webcam'
  const [inputMode, setInputMode] = useState('upload');

  // Upload and Image State
  const [file, setFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedSample, setSelectedSample] = useState(null);
  const [sampleList, setSampleList] = useState([]);

  // Webcam State & Refs
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const autoScanIntervalRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [autoScanActive, setAutoScanActive] = useState(false);
  const [cameraFacing, setCameraFacing] = useState('environment'); // 'user' | 'environment'

  // Inference Controls
  const [confidence, setConfidence] = useState(0.10);
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Results State
  const [result, setResult] = useState(null);
  const [viewMode, setViewMode] = useState('annotated'); // 'annotated', 'canvas', 'original'
  const [selectedDetectionId, setSelectedDetectionId] = useState(null);
  const [hoveredDetectionId, setHoveredDetectionId] = useState(null);

  // Audio Voice Guidance
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(false);

  // Modals
  const [isAuditModalOpen, setIsAuditModalOpen] = useState(false);
  const [dossierItem, setDossierItem] = useState(null);

  // Canvas Refs
  const canvasRef = useRef(null);
  const imageElementRef = useRef(null);

  // Load sample list and active model metadata
  useEffect(() => {
    getSampleImages()
      .then((res) => {
        const samples = res.samples || [];
        setSampleList(samples);
        const params = new URLSearchParams(window.location.search);
        const requestedSample = params.get('sample');
        if (requestedSample) {
          const match = samples.find(s => s.filename === requestedSample) || { id: 'sample_req', filename: requestedSample, title: requestedSample };
          handleSelectSample(match);
        }
      })
      .catch((err) => console.warn('Could not load samples', err));

    getModelInfo()
      .then((res) => setModelInfo(res))
      .catch((err) => console.warn('Could not load model info', err));

    return () => {
      // Cleanup camera and audio on unmount
      stopWebcam();
      stopSpeaking();
    };
  }, []);

  const handleModelChange = async (newModelId) => {
    try {
      await switchModel(newModelId);
      const updated = await getModelInfo();
      setModelInfo(updated);
    } catch (err) {
      console.error('Failed to switch model', err);
    }
  };

  // --- Webcam Handlers ---
  const startWebcam = async (facing = cameraFacing) => {
    try {
      setError('');
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facing,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setIsCameraActive(true);
    } catch (err) {
      console.error('Camera access error:', err);
      setError('Camera access error: Please grant browser camera permissions.');
      setIsCameraActive(false);
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
    setAutoScanActive(false);
    if (autoScanIntervalRef.current) {
      clearInterval(autoScanIntervalRef.current);
      autoScanIntervalRef.current = null;
    }
  };

  const toggleCameraFacing = () => {
    const nextFacing = cameraFacing === 'user' ? 'environment' : 'user';
    setCameraFacing(nextFacing);
    if (isCameraActive) {
      startWebcam(nextFacing);
    }
  };

  const captureWebcamFrame = () => {
    if (!videoRef.current || !isCameraActive) return null;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas;
  };

  const runWebcamDetection = () => {
    if (loading) return;
    const canvas = captureWebcamFrame();
    if (!canvas) {
      setError('Camera is not active. Click "Start Camera" first.');
      return;
    }

    const previewUrl = canvas.toDataURL('image/jpeg', 0.85);
    setImagePreview(previewUrl);

    canvas.toBlob(async (blob) => {
      if (!blob) return;
      setLoading(true);
      setError('');
      try {
        const res = await detectWaste(blob, {
          conf: confidence,
          modelId: modelInfo?.active_model_id,
        });
        setResult(res);
        if (res.detections?.length > 0) {
          setSelectedDetectionId(res.detections[0].detection_id);
        }
        if (autoSpeak) {
          speakResults(res);
        }
      } catch (err) {
        setError(err?.message || 'Detection failed on webcam frame.');
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg', 0.85);
  };

  // Auto-scan interval toggle
  const toggleAutoScan = () => {
    if (autoScanActive) {
      clearInterval(autoScanIntervalRef.current);
      autoScanIntervalRef.current = null;
      setAutoScanActive(false);
    } else {
      if (!isCameraActive) {
        startWebcam().then(() => {
          setAutoScanActive(true);
        });
      } else {
        setAutoScanActive(true);
      }
    }
  };

  useEffect(() => {
    if (autoScanActive && isCameraActive) {
      autoScanIntervalRef.current = setInterval(() => {
        runWebcamDetection();
      }, 2500);
    } else if (autoScanIntervalRef.current) {
      clearInterval(autoScanIntervalRef.current);
      autoScanIntervalRef.current = null;
    }
    return () => {
      if (autoScanIntervalRef.current) {
        clearInterval(autoScanIntervalRef.current);
      }
    };
  }, [autoScanActive, isCameraActive, confidence]);

  // --- Upload & Sample Handlers ---
  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (selected.size > 16 * 1024 * 1024) {
      setError('File size exceeds 16MB limit.');
      return;
    }

    setFile(selected);
    setSelectedSample(null);
    setError('');
    setResult(null);

    const previewUrl = URL.createObjectURL(selected);
    setImagePreview(previewUrl);
  };

  const handleSelectSample = (sample) => {
    setSelectedSample(sample);
    setFile(null);
    setError('');
    setResult(null);

    const url = getSampleImageUrl(sample.filename);
    setImagePreview(url);

    runDetectionWithSample(sample.filename);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      if (droppedFile.size > 16 * 1024 * 1024) {
        setError('File size exceeds 16MB limit.');
        return;
      }
      setFile(droppedFile);
      setSelectedSample(null);
      setError('');
      setResult(null);
      setImagePreview(URL.createObjectURL(droppedFile));
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const resetWorkspace = () => {
    setFile(null);
    setSelectedSample(null);
    setImagePreview(null);
    setResult(null);
    setError('');
    setSelectedDetectionId(null);
    stopSpeaking();
  };

  const runDetection = async () => {
    if (!file && !selectedSample) {
      setError('Please upload an image or choose a test sample first.');
      return;
    }

    if (selectedSample) {
      runDetectionWithSample(selectedSample.filename);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await detectWaste(file, {
        conf: confidence,
        modelId: modelInfo?.active_model_id,
      });
      setResult(res);
      if (res.detections?.length > 0) {
        setSelectedDetectionId(res.detections[0].detection_id);
      }
      if (new URLSearchParams(window.location.search).get('audit') === 'true') {
        setIsAuditModalOpen(true);
      }
      if (autoSpeak) {
        speakResults(res);
      }
    } catch (err) {
      setError(err?.message || 'Detection failed. Ensure backend Flask server is running.');
    } finally {
      setLoading(false);
    }
  };

  const runDetectionWithSample = async (sampleFilename) => {
    setLoading(true);
    setError('');

    try {
      const res = await detectWaste(null, {
        conf: confidence,
        modelId: modelInfo?.active_model_id,
        sampleName: sampleFilename,
      });
      setResult(res);
      if (res.detections?.length > 0) {
        setSelectedDetectionId(res.detections[0].detection_id);
      }
      if (new URLSearchParams(window.location.search).get('audit') === 'true') {
        setIsAuditModalOpen(true);
      }
      if (autoSpeak) {
        speakResults(res);
      }
    } catch (err) {
      setError(err?.message || 'Detection failed on sample image.');
    } finally {
      setLoading(false);
    }
  };

  // --- Voice Audio Guidance (Text-To-Speech) ---
  const speakResults = (resData = result) => {
    if (!resData || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const total = resData.total_detections || 0;
    if (total === 0) {
      const utter = new SpeechSynthesisUtterance('Waste scan complete. No items were detected at the current confidence threshold.');
      window.speechSynthesis.speak(utter);
      return;
    }

    const primaryBin = resData.summary?.primary_bin || 'Municipal Waste Bin';
    const rate = resData.summary?.recyclability_rate || 0;
    const advice = resData.summary?.summary_advice || 'Follow local municipal sorting guidelines.';

    const text = `Waste scan complete. Localized ${total} objects. Primary destination is ${primaryBin} with a ${rate} percent circular recovery rate. Key guidance: ${advice}`;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
  };

  // --- Redraw interactive canvas when viewMode is 'canvas' ---
  useEffect(() => {
    if (viewMode !== 'canvas' || !imagePreview || !canvasRef.current || !result) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = imageElementRef.current;

    if (!img || !img.complete) return;

    canvas.width = img.clientWidth;
    canvas.height = img.clientHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    (result.detections || []).forEach((det) => {
      const norm = det.normalized_box;
      const x = norm.nx1 * canvas.width;
      const y = norm.ny1 * canvas.height;
      const w = norm.nw * canvas.width;
      const h = norm.nh * canvas.height;

      const isSelected = selectedDetectionId === det.detection_id;
      const isHovered = hoveredDetectionId === det.detection_id;

      const color = det.recommendation?.bin_color || '#2563EB';

      ctx.lineWidth = isSelected ? 3 : isHovered ? 3 : 2;
      ctx.strokeStyle = color;
      ctx.strokeRect(x, y, w, h);

      ctx.fillStyle = isSelected ? `${color}35` : isHovered ? `${color}25` : `${color}10`;
      ctx.fillRect(x, y, w, h);

      const label = `${det.recommendation?.display_name || det.class_name} ${(det.confidence * 100).toFixed(0)}%`;
      ctx.font = 'bold 11px system-ui, sans-serif';
      const textW = ctx.measureText(label).width + 12;
      const badgeY = Math.max(0, y - 18);

      ctx.fillStyle = color;
      ctx.fillRect(x, badgeY, textW, 18);

      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(label, x + 6, badgeY + 13);
    });
  }, [viewMode, result, selectedDetectionId, hoveredDetectionId, imagePreview]);

  return (
    <div className="space-y-6">
      {/* Title & Model Baseline Notice */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">AI Waste Detection Workspace</h1>
            <span className="text-[11px] px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded font-semibold">
              {modelInfo?.active_model_name || 'YOLO11n Waste-15 (Flagship Master Model)'}
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Real-time object localization, municipal segregation actions, voice guidance, and sustainability metrics.
          </p>
        </div>

        {/* Interactive Model Switcher Dropdown */}
        <div className="flex items-center gap-2 self-start sm:self-auto bg-white border border-slate-200 rounded-lg p-1.5 shadow-xs">
          <div className="flex items-center gap-1.5 px-1.5 text-xs text-slate-500 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="hidden sm:inline font-bold text-slate-700">Model:</span>
          </div>
          <select
            value={modelInfo?.active_model_id || 'tri_model_ensemble'}
            onChange={(e) => handleModelChange(e.target.value)}
            className="text-xs font-semibold text-slate-800 bg-slate-50 border border-slate-200 rounded-md px-2.5 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer"
          >
            <option value="tri_model_ensemble">🎯 Tri-Model Ensemble (WBF Consensus — ~75%+ mAP)</option>
            <option value="yolo11n_15class_target">⚡ YOLO11n Flagship (100-Epoch — Fast 12ms)</option>
            <option value="yolo11n_15class_kaggle_master">🔬 YOLO11n Kaggle Master (100-Epoch @ 800px)</option>
            <option value="yolo11s_15class_high_precision">💎 YOLO11s High-Precision (100-Epoch @ 800px)</option>
            <option value="yolo11n_15class_balanced_boost">🌱 YOLO11n Balanced Boost (30-Epoch)</option>
          </select>
        </div>
      </div>

      {/* Main Grid: Input Workspace (Left) & Vision Results (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Upload, Samples, Controls (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {/* Mode Switcher Tabs */}
          <div className="bg-white border border-slate-200 rounded-xl p-1 shadow-xs flex items-center gap-1">
            <button
              onClick={() => {
                setInputMode('upload');
                stopWebcam();
              }}
              className={`flex-1 py-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors ${
                inputMode === 'upload'
                  ? 'bg-blue-50 text-blue-700 border border-blue-200/60 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Upload & Samples</span>
            </button>

            <button
              onClick={() => {
                setInputMode('webcam');
                startWebcam();
              }}
              className={`flex-1 py-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors ${
                inputMode === 'webcam'
                  ? 'bg-blue-50 text-blue-700 border border-blue-200/60 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Camera className="w-3.5 h-3.5" />
              <span>Live Webcam Scanner</span>
            </button>
          </div>

          {/* Conditional Input Mode Content */}
          {inputMode === 'upload' ? (
            <>
              {/* 1. Quick Test Samples Bar */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-2.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-slate-800 uppercase tracking-wide text-[11px]">
                    Quick Test Samples
                  </span>
                  <span className="text-slate-400 text-[10px]">1-Click Verification</span>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  {sampleList.map((sample) => (
                    <button
                      key={sample.id}
                      onClick={() => handleSelectSample(sample)}
                      className={`rounded-lg border text-left p-1.5 transition-all flex flex-col overflow-hidden ${
                        selectedSample?.id === sample.id
                          ? 'border-blue-600 bg-blue-50/50 shadow-xs ring-1 ring-blue-600'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <img
                        src={getSampleImageUrl(sample.filename)}
                        alt={sample.title}
                        className="w-full h-16 object-cover rounded mb-1 bg-slate-100"
                      />
                      <span className="text-[10px] font-bold text-slate-700 truncate">{sample.filename}</span>
                      <span className="text-[9px] text-blue-600 font-medium truncate">{sample.title}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* 2. Drag & Drop File Upload Area */}
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className={`bg-white border-2 border-dashed rounded-xl p-5 text-center shadow-xs transition-colors ${
                  file ? 'border-blue-500 bg-blue-50/20' : 'border-slate-300 hover:border-slate-400'
                }`}
              >
                <div className="w-10 h-10 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600 mx-auto mb-2">
                  <Upload className="w-5 h-5" />
                </div>

                <h3 className="font-bold text-xs text-slate-800 mb-0.5">
                  {file ? file.name : 'Upload Waste Image'}
                </h3>
                <p className="text-[11px] text-slate-500 mb-3">
                  Drag & drop or browse image (JPG, PNG, WEBP, BMP up to 16MB)
                </p>

                <div className="flex items-center justify-center gap-2">
                  <label className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold cursor-pointer shadow-xs transition-colors">
                    <span>Browse Files</span>
                    <input
                      type="file"
                      accept="image/jpeg,image/png,image/webp,image/bmp"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>

                  {(file || selectedSample) && (
                    <button
                      type="button"
                      onClick={resetWorkspace}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg text-xs font-medium transition-colors"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </div>
            </>
          ) : (
            /* Webcam Mode Viewport & Controls */
            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-800 uppercase tracking-wide text-[11px] flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full ${isCameraActive ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'}`} />
                  <span>Live Camera Viewport</span>
                </span>
                <span className="text-[10px] text-slate-400 font-mono">
                  {isCameraActive ? 'Active Stream' : 'Camera Off'}
                </span>
              </div>

              {/* Video Viewport */}
              <div className="relative aspect-video w-full bg-slate-900 rounded-lg overflow-hidden border border-slate-800 flex items-center justify-center">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`}
                />

                {!isCameraActive && (
                  <div className="text-center p-6 space-y-2 text-slate-500">
                    <CameraOff className="w-8 h-8 mx-auto text-slate-600" />
                    <p className="text-xs text-slate-400">Camera is currently stopped.</p>
                    <button
                      onClick={() => startWebcam()}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition-colors"
                    >
                      Turn On Camera
                    </button>
                  </div>
                )}

                {/* Reticle HUD overlay when active */}
                {isCameraActive && (
                  <div className="absolute inset-4 pointer-events-none border-2 border-white/20 rounded-lg flex items-center justify-center">
                    <div className="w-12 h-12 border-2 border-blue-400/60 rounded-full animate-ping opacity-25" />
                    <span className="absolute top-2 left-2 text-[9px] font-mono text-emerald-400 bg-slate-900/60 px-1.5 py-0.5 rounded">
                      ● LIVE SCANNER
                    </span>
                  </div>
                )}
              </div>

              {/* Webcam Control Buttons */}
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={runWebcamDetection}
                  disabled={!isCameraActive || loading}
                  className="py-2.5 px-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 text-white disabled:text-slate-400 rounded-lg text-xs font-bold shadow-xs flex items-center justify-center gap-1.5 transition-colors"
                >
                  <Camera className="w-4 h-4" />
                  <span>Snap & Segregate</span>
                </button>

                <button
                  onClick={toggleAutoScan}
                  disabled={!isCameraActive}
                  className={`py-2.5 px-3 rounded-lg text-xs font-bold border transition-colors flex items-center justify-center gap-1.5 ${
                    autoScanActive
                      ? 'bg-rose-50 border-rose-300 text-rose-700 animate-pulse'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {autoScanActive ? <Square className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                  <span>{autoScanActive ? 'Stop Auto-Scan' : 'Auto-Scan (2.5s)'}</span>
                </button>
              </div>

              <div className="flex items-center justify-between text-[11px] pt-1 text-slate-500">
                <button
                  onClick={toggleCameraFacing}
                  className="text-blue-600 hover:underline flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Flip Camera ({cameraFacing})</span>
                </button>

                {isCameraActive && (
                  <button
                    onClick={stopWebcam}
                    className="text-rose-600 hover:underline flex items-center gap-1"
                  >
                    <CameraOff className="w-3 h-3" />
                    <span>Stop Camera</span>
                  </button>
                )}
              </div>
            </div>
          )}

          {/* 3. Inference Parameters & Detect Button */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-3.5">
            <div>
              <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
                <span>Confidence Threshold:</span>
                <span className="font-mono text-blue-600 font-bold">{(confidence * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.85"
                step="0.01"
                value={confidence}
                onChange={(e) => setConfidence(parseFloat(e.target.value))}
                className="w-full accent-blue-600 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>Sensitive (5%)</span>
                <span>Optimal (10%)</span>
                <span>Strict (50%+)</span>
              </div>
            </div>

            {/* Auto-Speech Toggle */}
            <div className="flex items-center justify-between pt-1 border-t border-slate-100 text-xs text-slate-600">
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={autoSpeak}
                  onChange={(e) => setAutoSpeak(e.target.checked)}
                  className="rounded text-blue-600 accent-blue-600 w-3.5 h-3.5 cursor-pointer"
                />
                <span className="text-[11px] font-medium text-slate-700">Auto-speak segregation audio</span>
              </label>

              {result && (
                <button
                  onClick={isSpeaking ? stopSpeaking : () => speakResults(result)}
                  className="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1"
                >
                  {isSpeaking ? <VolumeX className="w-3.5 h-3.5 text-rose-600" /> : <Volume2 className="w-3.5 h-3.5" />}
                  <span>{isSpeaking ? 'Stop Audio' : 'Play Voice'}</span>
                </button>
              )}
            </div>

            {inputMode === 'upload' && (
              <button
                onClick={runDetection}
                disabled={(!file && !selectedSample) || loading}
                className={`w-full py-2.5 px-4 rounded-lg text-xs font-bold shadow-xs flex items-center justify-center gap-2 transition-colors ${
                  loading
                    ? 'bg-blue-400 text-white cursor-not-allowed'
                    : (!file && !selectedSample)
                    ? 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none'
                    : 'bg-blue-600 hover:bg-blue-700 text-white active:bg-blue-800'
                }`}
              >
                {loading ? (
                  <>
                    <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Running YOLO & Segregation Engine...</span>
                  </>
                ) : (
                  <>
                    <ScanLine className="w-4 h-4" />
                    <span>Detect Waste & Segregate</span>
                  </>
                )}
              </button>
            )}

            {error && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 font-medium flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Visualizer Viewport (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3">
            {/* View Mode Toolbar */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <ImageIcon className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                  Image Analysis Frame
                </span>
                {result && (
                  <span className="text-xs font-semibold px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-full">
                    {result.total_detections} Detected
                  </span>
                )}
              </div>

              {result && (
                <div className="flex items-center gap-2">
                  <div className="flex items-center bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
                    <button
                      onClick={() => setViewMode('annotated')}
                      className={`px-2.5 py-1 rounded-md transition-colors ${
                        viewMode === 'annotated' ? 'bg-white text-blue-600 shadow-xs' : 'text-slate-600'
                      }`}
                    >
                      Annotated
                    </button>
                    <button
                      onClick={() => setViewMode('canvas')}
                      className={`px-2.5 py-1 rounded-md transition-colors ${
                        viewMode === 'canvas' ? 'bg-white text-blue-600 shadow-xs' : 'text-slate-600'
                      }`}
                    >
                      Interactive
                    </button>
                    <button
                      onClick={() => setViewMode('original')}
                      className={`px-2.5 py-1 rounded-md transition-colors ${
                        viewMode === 'original' ? 'bg-white text-blue-600 shadow-xs' : 'text-slate-600'
                      }`}
                    >
                      Original
                    </button>
                  </div>

                  <button
                    onClick={() => setIsAuditModalOpen(true)}
                    className="px-2.5 py-1 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-md text-xs font-semibold text-slate-700 flex items-center gap-1 transition-colors"
                    title="Export certified waste audit report"
                  >
                    <FileText className="w-3.5 h-3.5 text-blue-600" />
                    <span className="hidden sm:inline">Audit Report</span>
                  </button>
                </div>
              )}
            </div>

            {/* Visual Viewport Box */}
            <div className="relative w-full min-h-[340px] max-h-[480px] bg-slate-900 rounded-lg overflow-hidden flex items-center justify-center border border-slate-800">
              {imagePreview ? (
                <div className="relative inline-block max-w-full max-h-[470px]">
                  <img
                    ref={imageElementRef}
                    src={
                      viewMode === 'annotated' && result?.annotated_image_b64
                        ? result.annotated_image_b64
                        : imagePreview
                    }
                    alt="Target waste"
                    className="max-h-[470px] w-auto object-contain block mx-auto select-none"
                    onLoad={() => {
                      if (canvasRef.current && imageElementRef.current) {
                        canvasRef.current.width = imageElementRef.current.clientWidth;
                        canvasRef.current.height = imageElementRef.current.clientHeight;
                      }
                    }}
                  />

                  {viewMode === 'canvas' && (
                    <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" />
                  )}

                  {loading && (
                    <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center">
                      <div className="bg-white/90 px-4 py-2 rounded-lg text-xs font-bold text-slate-800 shadow-md flex items-center gap-2">
                        <span className="w-3.5 h-3.5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                        <span>Analyzing Frame...</span>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center p-8 space-y-2 text-slate-500">
                  <ImageIcon className="w-10 h-10 mx-auto text-slate-700" />
                  <p className="text-xs text-slate-400">Select a sample or browse an image to inspect detections.</p>
                </div>
              )}
            </div>

            {result && (
              <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
                <span>Inference Latency: <strong>{result.processing_time_ms} ms</strong></span>
                <span>Session ID: <strong className="font-mono text-slate-700">{result.session_id}</strong></span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Sustainability Metrics & Detections Section */}
      {result && (
        <section className="space-y-6">
          {/* Eco-Impact & Sustainability Card */}
          <EcoImpactCard detections={result.detections} summary={result.summary} />

          {/* Overall Image Summary Callout */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Overall Recommendation:</span>
                <span className="text-sm font-extrabold text-slate-900">{result.summary?.primary_disposal}</span>
                <span
                  className="px-2 py-0.5 rounded text-[11px] font-bold text-white shadow-2xs"
                  style={{ backgroundColor: result.summary?.primary_bin_color }}
                >
                  {result.summary?.primary_bin}
                </span>
              </div>

              <div className="flex items-center gap-3 text-xs text-slate-600 font-medium">
                <button
                  onClick={isSpeaking ? stopSpeaking : () => speakResults(result)}
                  className={`px-3 py-1 rounded-lg border text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                    isSpeaking
                      ? 'bg-rose-50 text-rose-700 border-rose-200 animate-pulse'
                      : 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100'
                  }`}
                >
                  {isSpeaking ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
                  <span>{isSpeaking ? 'Stop Guidance' : '🔊 Read Instructions Aloud'}</span>
                </button>

                <button
                  onClick={() => setIsAuditModalOpen(true)}
                  className="px-3 py-1 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
                >
                  <FileText className="w-3.5 h-3.5 text-blue-600" />
                  <span>Audit Certificate</span>
                </button>
              </div>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              <strong>Action Summary:</strong> {result.summary?.summary_advice}
            </p>
          </div>

          {/* Itemized Detections Grid */}
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-slate-900 uppercase tracking-wide">
                Itemized Detections ({result.detections?.length || 0})
              </h3>
              <span className="text-xs text-slate-400">Click any card to open full handling dossier</span>
            </div>

            {result.detections?.length === 0 ? (
              <p className="text-xs text-slate-400 py-4 text-center">No waste objects detected at the specified confidence threshold.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.detections.map((det) => {
                  const rec = det.recommendation || {};
                  const isSelected = selectedDetectionId === det.detection_id;
                  const badge = DISPOSAL_BADGES[rec.primary_action] || DISPOSAL_BADGES['General waste'];

                  return (
                    <div
                      key={det.detection_id}
                      onClick={() => {
                        setSelectedDetectionId(det.detection_id);
                        setDossierItem(det);
                      }}
                      onMouseEnter={() => setHoveredDetectionId(det.detection_id)}
                      onMouseLeave={() => setHoveredDetectionId(null)}
                      className={`rounded-xl border p-4 transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
                        isSelected
                          ? 'border-blue-600 bg-blue-50/20 shadow-xs ring-1 ring-blue-600'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div>
                        {/* Header: Class, Order, Badge */}
                        <div className="flex items-start justify-between gap-2 mb-2">
                          <div>
                            <div className="flex items-center gap-1.5">
                              <span className="w-5 h-5 rounded-full bg-slate-100 text-slate-700 text-[10px] font-bold flex items-center justify-center">
                                #{det.detection_id}
                              </span>
                              <h4 className="font-bold text-sm text-slate-900">{rec.display_name || det.class_name}</h4>
                            </div>
                            <span className="text-[11px] text-slate-400 font-mono pl-6.5">
                              Confidence: {(det.confidence * 100).toFixed(1)}%
                            </span>
                          </div>

                          <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${badge.bg} ${badge.text} ${badge.border}`}>
                            {badge.icon} {badge.label}
                          </span>
                        </div>

                        {/* Material & Explanation */}
                        <div className="space-y-1.5 text-xs text-slate-600">
                          <div>
                            <strong className="text-slate-800">Material:</strong> {rec.material_description}
                          </div>
                          <p className="text-[11px] text-slate-500 leading-relaxed">
                            {rec.explanation}
                          </p>
                        </div>
                      </div>

                      {/* Preparation Instructions */}
                      {rec.preparation_instructions && rec.preparation_instructions.length > 0 && (
                        <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs space-y-1">
                          <strong className="text-slate-800 text-[11px] block uppercase font-bold">Preparation & Handling:</strong>
                          <ul className="space-y-0.5 text-slate-600 text-[11px]">
                            {rec.preparation_instructions.map((step, idx) => (
                              <li key={idx} className="flex items-start gap-1">
                                <span className="text-blue-600 font-bold">•</span>
                                <span>{step}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Safety Precautions if any */}
                      {rec.safety_precautions && rec.safety_precautions.length > 0 && (
                        <div className="bg-rose-50 border border-rose-200 rounded-lg p-2.5 text-xs text-rose-800 space-y-0.5">
                          <div className="font-bold text-[10px] uppercase flex items-center gap-1 text-rose-700">
                            <ShieldAlert className="w-3.5 h-3.5" />
                            <span>Safety Note:</span>
                          </div>
                          {rec.safety_precautions.map((s, idx) => (
                            <p key={idx} className="text-[11px]">{s}</p>
                          ))}
                        </div>
                      )}

                      {/* Handling Details & Dossier CTA */}
                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                        <span>Target Bin: <strong className="text-slate-700 font-semibold">{rec.bin_name || det.bin || 'Designated Waste Bin'}</strong></span>
                        <span className="text-blue-600 font-semibold flex items-center gap-0.5">
                          <span>Details</span>
                          <ArrowRight className="w-3 h-3" />
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Audit Certificate Modal */}
      <AuditCertificateModal
        isOpen={isAuditModalOpen}
        onClose={() => setIsAuditModalOpen(false)}
        result={result}
        modelInfo={modelInfo}
      />

      {/* Material Dossier Modal */}
      <MaterialDossierModal
        isOpen={Boolean(dossierItem)}
        onClose={() => setDossierItem(null)}
        detection={dossierItem}
      />
    </div>
  );
};

export default DetectionPage;

'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { Camera, Upload, AlertCircle, CheckCircle2, Smartphone, Focus, Leaf, Droplets, Beef, ShieldAlert, Wheat, ShieldQuestion, QrCode, XCircle, Menu } from 'lucide-react';

export default function Home() {
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Camera State
  const [isCameraActive, setIsCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // File & Barcode State
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [barcode, setBarcode] = useState('');

  // User Profile State
  const [userOrigin, setUserOrigin] = useState('ashkenazi');
  const [userCountry, setUserCountry] = useState('México');
  const [chaguimAlerts, setChaguimAlerts] = useState('false');
  const [kosherRecipes, setKosherRecipes] = useState('false');

  useEffect(() => {
    const storedOrigin = localStorage.getItem('userOrigin');
    const storedCountry = localStorage.getItem('userCountry');
    const storedChaguim = localStorage.getItem('chaguimAlerts');
    const storedRecipes = localStorage.getItem('kosherRecipes');
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedOrigin) setUserOrigin(storedOrigin);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedCountry) setUserCountry(storedCountry);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedChaguim) setChaguimAlerts(storedChaguim);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedRecipes) setKosherRecipes(storedRecipes);
  }, []);

  useEffect(() => {
    localStorage.setItem('userOrigin', userOrigin);
  }, [userOrigin]);

  useEffect(() => {
    localStorage.setItem('userCountry', userCountry);
  }, [userCountry]);

  // Start Camera Stream
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' } // Prefer back camera on mobile
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsCameraActive(true);
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      alert("No se pudo acceder a la cámara. Por favor permite el acceso o usa la opción de subir foto.");
    }
  };

  // Stop Camera Stream
  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraActive(false);
    }
  };

  // Cleanup camera on unmount
  useEffect(() => {
    return () => stopCamera();
  }, []);

  const dataURLtoBlob = (dataurl: string) => {
    let arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)![1],
      bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
  }

  // File Compression Helper (WebP 1024px)
  const compressImageFile = (file: File): Promise<Blob> => {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = URL.createObjectURL(file);
      img.onload = () => {
        let width = img.width;
        let height = img.height;
        const maxSize = 1024;
        if (width > height && width > maxSize) {
          height = Math.round((height * maxSize) / width);
          width = maxSize;
        } else if (height > maxSize) {
          width = Math.round((width * maxSize) / height);
          height = maxSize;
        }
        
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          resolve(file); // fallback
          return;
        }
        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => {
          if (blob) resolve(blob);
          else resolve(file); // fallback
        }, 'image/webp', 0.7); // 70% quality WebP
      };
      img.onerror = () => resolve(file); // fallback on error
    });
  };

  // Handle Photo Capture
  const takePhotoAndScan = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    // Draw video frame to canvas, resizing if needed
    const video = videoRef.current;
    let width = video.videoWidth;
    let height = video.videoHeight;
    const maxSize = 1024;
    
    if (width > height && width > maxSize) {
      height = Math.round((height * maxSize) / width);
      width = maxSize;
    } else if (height > maxSize) {
      width = Math.round((width * maxSize) / height);
      height = maxSize;
    }

    const canvas = canvasRef.current;
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Get image blob, highly compressed WebP
    const dataUrl = canvas.toDataURL('image/webp', 0.7);
    const blob = dataURLtoBlob(dataUrl);

    // Proceed to scan
    await executeScan(blob);
  };

  // Handle File Upload
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;
    setIsScanning(true); // show feedback early during compression
    const file = e.target.files[0];
    try {
      const compressedBlob = await compressImageFile(file);
      await executeScan(compressedBlob);
    } catch (err) {
      console.error(err);
      await executeScan(file); // fallback to original
    }
  };

  // Handle Barcode only submission
  const handleBarcodeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!barcode.trim()) return;
    await executeScan(null, barcode);
  };

  // Main API Call
  const executeScan = async (imageFile: Blob | File | null, barcodeStr: string = '') => {
    setIsScanning(true);
    setResult(null); // Clear previous

    const formData = new FormData();
    if (imageFile) {
      formData.append('images', imageFile, 'capture.jpg');
    }
    const finalBarcode = barcodeStr || barcode;
    if (finalBarcode) {
      formData.append('barcode', finalBarcode);
    }

    if (!imageFile && !finalBarcode) {
      setIsScanning(false);
      alert("Proporciona una imagen o un código de barras");
      return;
    }

    const preferences = {
      origen: userOrigin,
      pais: userCountry,
      kosherRecipes: kosherRecipes
    };
    formData.append('preferences', JSON.stringify(preferences));

    try {
      // PHASE 1: Fast Scan 
      const fastController = new AbortController();
      const fastTimeout = setTimeout(() => fastController.abort(), 15000); // 15s max for fast phase

      let fastResult = null;
      try {
        const fastRes = await fetch('/api/scan?phase=fast', {
          method: 'POST',
          body: formData,
          signal: fastController.signal
        });
        clearTimeout(fastTimeout);

        if (fastRes.ok) {
          fastResult = await fastRes.json();
          // Render Phase 1 immediately
          setResult({ ...fastResult, phase: 'fast' });
        }
      } catch (e) {
        console.error("Phase 1 Fast Scan failed or timed out:", e);
        // Continue to Phase 2 regardless
      }

      // PHASE 2: Detailed Scan
      const detailedController = new AbortController();
      const detailedTimeout = setTimeout(() => detailedController.abort(), 50000);

      const res = await fetch('/api/scan?phase=detailed', {
        method: 'POST',
        body: formData,
        signal: detailedController.signal
      });
      clearTimeout(detailedTimeout);

      if (!res.ok) {
        let errMessage = `Error ${res.status}: ${res.statusText}`;
        try {
          const err = await res.json();
          errMessage = err.detail || errMessage;
        } catch (e) {
          console.error("Error parsing detailed failure");
        }
        throw new Error(errMessage);
      }

      const data = await res.json();
      // Render Phase 2 
      setResult({ ...data, phase: 'detailed' });

      if (isCameraActive) stopCamera(); 
    } catch (error: any) {
      console.error('Scan failed:', error);
      let finalMsg = error.message;
      if (error.name === 'AbortError') {
        finalMsg = 'La solicitud tardó demasiado tiempo (Timeout).';
      }
      alert('Error: ' + finalMsg);
      
      // If we already rendered Phase 1 but Phase 2 crashed (e.g. Rate Limit), 
      // replace the loading skeleton with the error message.
      setResult((prev: any) => {
        if (prev && prev.phase === 'fast') {
          return { ...prev, phase: 'error', explicacion_halajica: `**Análisis Detallado:**\nNo se pudo cargar el desglose final debido a un error: ${finalMsg}` };
        }
        return prev; // Or null if it crashed before Phase 1
      });

    } finally {
      setIsScanning(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col lg:flex-row p-4 lg:p-10 gap-8 max-w-[1400px] mx-auto relative">

      {/* LEFT COLUMN: Scanner / Input */}
      <div className="flex-1 w-full max-w-lg mx-auto lg:max-w-none flex flex-col h-full lg:sticky lg:top-10">

        <header className="w-full flex justify-between items-center mb-8">
          <Link href="/chaguim" className="text-2xl text-slate-300 hover:text-emerald-400 transition" aria-label="Abrir Guía Chaguim">☰</Link>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            KosherScan
          </h1>
          <Link href="/settings" className="text-2xl text-slate-300 hover:text-white transition">⚙️</Link>
        </header>

        <div className="w-full bg-slate-800/80 border border-slate-700/50 rounded-[2.5rem] p-8 lg:p-12 backdrop-blur-xl shadow-2xl flex flex-col items-center flex-grow">

          <h2 className="text-3xl font-bold mt-2 mb-2 tracking-tight text-white text-center">Analizar Producto</h2>

          <div className="flex flex-col gap-2 mt-4 mb-8 text-slate-400 text-sm">
            <div className="flex items-center justify-center gap-2">
              <Smartphone className="w-4 h-4 text-emerald-400" />
              <span>Fotografía el producto o ingresa su código</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <Focus className="w-4 h-4 text-emerald-400" />
              <span>Asegúrate de que etiquetas sean legibles</span>
            </div>
          </div>

          {/* Scanner Viewport */}
          <div className="relative w-full aspect-square max-w-[320px] rounded-3xl overflow-hidden bg-slate-900 border-2 border-slate-700/50 my-4 flex justify-center items-center group shadow-inner">

            {/* Camera feed */}
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className={`absolute inset-0 w-full h-full object-cover z-10 ${isCameraActive ? 'opacity-100' : 'opacity-0'}`}
            />
            <canvas ref={canvasRef} className="hidden" />

            {/* Offline Animation (when camera is off) */}
            {!isCameraActive && (
              <>
                <div className="absolute inset-0 bg-emerald-500/5 rounded-full blur-3xl animate-pulse"></div>
                {/* Corners */}
                <div className="absolute top-4 left-4 w-10 h-10 border-t-4 border-l-4 border-slate-500 rounded-tl-2xl transition-all group-hover:border-emerald-500"></div>
                <div className="absolute top-4 right-4 w-10 h-10 border-t-4 border-r-4 border-slate-500 rounded-tr-2xl transition-all group-hover:border-emerald-500"></div>
                <div className="absolute bottom-4 left-4 w-10 h-10 border-b-4 border-l-4 border-slate-500 rounded-bl-2xl transition-all group-hover:border-emerald-500"></div>
                <div className="absolute bottom-4 right-4 w-10 h-10 border-b-4 border-r-4 border-slate-500 rounded-br-2xl transition-all group-hover:border-emerald-500"></div>
                {/* Inner dash */}
                <div className="w-16 h-16 border-2 border-dashed border-slate-600 rounded-full animate-[spin_10s_linear_infinite]"></div>
              </>
            )}

            {/* Scanning Overlay overlays on top of everything */}
            {isScanning && (
              <div className="absolute inset-0 bg-emerald-900/40 backdrop-blur-md flex flex-col items-center justify-center z-20">
                <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                <span className="font-bold animate-pulse text-emerald-100 drop-shadow-lg text-lg">Analizando IA...</span>
              </div>
            )}

            {/* Active Camera Overlay */}
            {isCameraActive && !isScanning && (
              <>
                <div className="absolute top-4 left-4 w-10 h-10 border-t-4 border-l-4 border-emerald-400 rounded-tl-2xl z-10 shadow-[0_0_15px_rgba(16,185,129,0.5)]"></div>
                <div className="absolute top-4 right-4 w-10 h-10 border-t-4 border-r-4 border-emerald-400 rounded-tr-2xl z-10 shadow-[0_0_15px_rgba(16,185,129,0.5)]"></div>
                <div className="absolute bottom-4 left-4 w-10 h-10 border-b-4 border-l-4 border-emerald-400 rounded-bl-2xl z-10 shadow-[0_0_15px_rgba(16,185,129,0.5)]"></div>
                <div className="absolute bottom-4 right-4 w-10 h-10 border-b-4 border-r-4 border-emerald-400 rounded-br-2xl z-10 shadow-[0_0_15px_rgba(16,185,129,0.5)]"></div>
              </>
            )}
          </div>

          <div className="w-full flex gap-3 mt-6">
            {!isCameraActive ? (
              <button
                onClick={startCamera}
                disabled={isScanning}
                className="flex-1 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-white font-semibold py-4 rounded-2xl shadow-[0_8px_25px_rgba(16,185,129,0.3)] transition-all active:scale-95 flex items-center justify-center gap-2"
              >
                <Camera className="w-5 h-5" /> Activar Cámara
              </button>
            ) : (
              <>
                <button
                  onClick={stopCamera}
                  disabled={isScanning}
                  className="bg-slate-700 hover:bg-slate-600 text-white font-semibold px-5 py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center"
                  title="Detener Cámara"
                >
                  <XCircle className="w-6 h-6" />
                </button>
                <button
                  onClick={takePhotoAndScan}
                  disabled={isScanning}
                  className="flex-1 bg-gradient-to-r from-emerald-500 to-emerald-600 shadow-[0_8px_25px_rgba(16,185,129,0.3)] hover:brightness-110 text-white font-bold py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2 text-lg"
                >
                  <Camera className="w-6 h-6" /> Capturar
                </button>
              </>
            )}
          </div>

          <div className="w-full flex items-center gap-4 my-6 opacity-50">
            <div className="h-px bg-slate-500 flex-1"></div>
            <span className="text-sm font-medium uppercase tracking-wider text-slate-300">O Alternativas</span>
            <div className="h-px bg-slate-500 flex-1"></div>
          </div>

          <div className="w-full flex flex-col gap-4">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept="image/*"
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isScanning}
              className="w-full bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white font-semibold py-3.5 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2"
            >
              <Upload className="w-5 h-5 opacity-70" /> Subir desde Galería
            </button>

            <form onSubmit={handleBarcodeSubmit} className="flex gap-2">
              <div className="relative flex-1">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <QrCode className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="text"
                  value={barcode}
                  onChange={(e) => setBarcode(e.target.value)}
                  placeholder="Insertar Código Barras (EAN/UPC)"
                  className="w-full bg-slate-900 border border-slate-700 text-white rounded-2xl py-3.5 pl-10 pr-4 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
                />
              </div>
              <button
                type="submit"
                disabled={isScanning || !barcode.trim()}
                className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:hover:bg-emerald-600 text-white font-semibold px-6 py-3.5 rounded-2xl transition-all active:scale-95 flex items-center justify-center"
              >
                Buscar
              </button>
            </form>
          </div>

          {/* Configuración de Perfil (Ashkenazi/Sefaradí, País) */}
          <div className="w-full flex items-center justify-between gap-4 mt-2 p-4 bg-slate-900/50 rounded-2xl border border-slate-700/50">
            <div className="flex flex-col flex-1">
              <label className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">Costumbre</label>
              <select
                value={userOrigin}
                onChange={(e) => setUserOrigin(e.target.value)}
                className="bg-transparent text-white font-medium focus:outline-none appearance-none cursor-pointer"
              >
                <option value="ashkenazi" className="bg-slate-800">Ashkenazí</option>
                <option value="sefaradi" className="bg-slate-800">Sefaradí</option>
              </select>
            </div>

            <div className="w-px h-8 bg-slate-700"></div>

            <div className="flex flex-col flex-1 pl-2">
              <label className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">País</label>
              <select
                value={userCountry}
                onChange={(e) => setUserCountry(e.target.value)}
                className="bg-transparent text-white font-medium focus:outline-none appearance-none cursor-pointer"
              >
                <option value="México" className="bg-slate-800">México</option>
                <option value="Estados Unidos" className="bg-slate-800">Estados Unidos</option>
                <option value="Argentina" className="bg-slate-800">Argentina</option>
                <option value="Israel" className="bg-slate-800">Israel</option>
                <option value="España" className="bg-slate-800">España</option>
                <option value="Otro" className="bg-slate-800">Otro País</option>
              </select>
            </div>
          </div>

          {/* Disclaimer Node */}
          <div className="mt-8 pt-5 border-t border-slate-700 flex items-start gap-3 w-full opacity-70">
            <ShieldQuestion className="w-5 h-5 text-emerald-500/80 flex-shrink-0 mt-0.5" />
            <p className="text-[11px] text-slate-300 leading-relaxed">
              <strong>Nota importante:</strong> Este análisis de inteligencia artificial es una herramienta de asistencia tecnológica de referencia. <strong>No sustituye de ninguna manera el dictamen ni la revisión de una autoridad rabínica competente.</strong> En caso de duda sobre la Kashrut de un ingrediente o producto, consulte siempre a su Mashgiach o Rabino experto de confianza.
            </p>
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN: Results */}
      <div className="flex-1 w-full max-w-lg mx-auto lg:max-w-none h-full min-h-[500px]">
        {result ? (
          <ResultView result={result} onBack={() => setResult(null)} />
        ) : chaguimAlerts === 'true' ? (
          <ChaguimWidget userOrigin={userOrigin} />
        ) : (
          <div className="h-full min-h-[600px] flex flex-col items-center justify-center border-2 border-dashed border-slate-700/50 bg-slate-800/20 rounded-[2.5rem] p-12 text-slate-500">
            <div className="w-24 h-24 mb-6 rounded-full bg-slate-800/50 flex items-center justify-center">
              <Leaf className="w-10 h-10 opacity-30" />
            </div>
            <h3 className="text-xl font-medium text-slate-400 mb-2 text-center">Esperando Análisis</h3>
            <p className="text-sm text-center max-w-xs text-slate-500">
              Escanea un producto con la cámara de la izquierda o introduce su código de barras para desglosar el resultado aquí.
            </p>
          </div>
        )}
      </div>
    </main>
  );
}

function ResultView({ result, onBack }: { result: any, onBack: () => void }) {
  const status = result.resultado?.toUpperCase() || 'DUDOSO';
  const isKosher = status.includes('KOSHER') && !status.includes('NO');

  return (
    <div className="w-full flex-col flex gap-4 animate-in fade-in slide-in-from-bottom-8 duration-500">

      {/* Dynamic Status Header */}
      <div className={`w-full p-8 rounded-[2.5rem] shadow-xl flex flex-col justify-center text-white relative overflow-hidden
        ${isKosher ? 'bg-gradient-to-br from-emerald-500 to-emerald-700 shadow-emerald-500/20' : 'bg-gradient-to-br from-rose-500 to-rose-700 shadow-rose-500/20'}`}>

        {/* Background decorative icon */}
        <div className="absolute -right-6 -bottom-6 opacity-10 pointer-events-none">
          {isKosher ? <CheckCircle2 className="w-48 h-48" /> : <ShieldAlert className="w-48 h-48" />}
        </div>

        <div className="flex flex-col relative z-10">
          <span className="text-sm font-semibold uppercase tracking-widest opacity-80 mb-1">Estatus Final</span>
          <div className="flex items-center gap-3 text-4xl font-black tracking-tight drop-shadow-md">
            {isKosher ? <CheckCircle2 className="w-10 h-10" /> : <ShieldAlert className="w-10 h-10" />}
            {status}
          </div>
          <div className="mt-4 flex flex-col backdrop-blur-md bg-white/20 px-4 py-3 rounded-xl text-white/90 border border-white/20 max-w-sm">
            <span className="font-bold text-xs uppercase tracking-wider mb-1 opacity-80">Certeza IA</span>
            <span className="font-medium text-sm leading-relaxed">{result.confianza_analisis || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="w-full flex flex-col gap-5 mt-2">

        {/* Quick Summary Section */}
        {result.explicacion_halajica && result.explicacion_halajica.includes('**Resumen Rápido:**') && (
          <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-emerald-500/30 backdrop-blur-xl">
            <h3 className="text-white font-bold text-lg mb-2 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" /> Resumen Rápido
            </h3>
            <p className="text-emerald-100/90 text-[15px] leading-relaxed font-medium">
              {result.explicacion_halajica.split('**Resumen Rápido:**')[1]?.split('**Análisis Detallado:**')[0]?.trim()}
            </p>
          </div>
        )}

        {/* Basic Grid Info */}
        <div className="grid grid-cols-2 gap-4">
          {/* Seal Card */}
          <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl">
            <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-2 block">Sello</span>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-emerald-500/10 text-emerald-400 rounded-2xl flex items-center justify-center font-black text-xl border border-emerald-500/20 shadow-inner">
                {result.sello_detectado?.nombre ? result.sello_detectado.nombre.substring(0, 2).toUpperCase() : '??'}
              </div>
              <div className="flex flex-col">
                <div className="font-bold text-lg text-white leading-tight">
                  {result.sello_detectado?.nombre || 'Ninguno'}
                </div>
                {result.sello_detectado?.nombre && result.sello_detectado.nombre !== 'Ninguno' && (
                  <span className="text-xs text-slate-400 font-medium">
                    {result.sello_detectado.pais || ''} • {result.sello_detectado.confianza || ''}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Category Card */}
          <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl">
            <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-2 block">Categoría</span>
            <div className="flex items-center gap-3 text-lg font-bold text-white leading-tight">
              <span className="text-emerald-400 bg-emerald-500/10 p-2.5 rounded-2xl border border-emerald-500/20">
                {result.categoria?.includes('Parve') ? <Leaf className="w-6 h-6" /> :
                  result.categoria?.includes('Lácteo') ? <Droplets className="w-6 h-6 text-blue-400" /> :
                    <Beef className="w-6 h-6 text-rose-400" />}
              </span>
              {result.categoria || 'Parve'}
            </div>
          </div>
        </div>

        {/* Product Meta (if from API) */}
        {result.off_data && (
          <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl">
            <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2 border-b border-slate-700 pb-3">
              <QrCode className="w-5 h-5 text-indigo-400" /> Registro OpenFoodFacts
            </h3>
            <div className="flex flex-col gap-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Producto</span>
                <span className="text-white font-medium text-right">{result.off_data.product_name || 'Desconocido'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Marca</span>
                <span className="text-white font-medium text-right">{result.off_data.brands || 'N/A'}</span>
              </div>
            </div>
          </div>
        )}

        {/* Alerts */}
        {result.alertas && result.alertas.length > 0 && result.alertas[0] !== "Ninguno" && (
          <div className="bg-amber-900/20 p-6 rounded-3xl shadow-lg border border-amber-700/30 backdrop-blur-xl">
            <h3 className="text-amber-400 font-bold text-lg mb-4 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5" /> Alertas Relevantes
            </h3>
            <div className="flex flex-col gap-3">
              {result.alertas.map((alerta: string, i: number) => (
                <div key={i} className="flex gap-3 text-amber-200 bg-amber-950/40 p-4 rounded-2xl border border-amber-800/30">
                  <ShieldAlert className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-500" />
                  <span className="text-sm font-medium leading-relaxed">{alerta}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Characteristics */}
        <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl">
          <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-4 block">Filtros Adicionales</span>
          <div className="flex flex-wrap gap-2">
            {result.caracteristicas_basicas?.vegano && (
              <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-4 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 shadow-inner">
                <Leaf className="w-4 h-4" /> Vegano
              </span>
            )}
            {result.caracteristicas_basicas?.sin_gluten && (
              <span className="bg-amber-500/10 text-amber-400 border border-amber-500/20 px-4 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 shadow-inner">
                <Wheat className="w-4 h-4" /> Sin Gluten
              </span>
            )}
            {result.caracteristicas_basicas?.sin_lacteos && (
              <span className="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-4 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 shadow-inner">
                <Droplets className="w-4 h-4" /> Sin Lácteos
              </span>
            )}
            {!result.caracteristicas_basicas?.vegano && !result.caracteristicas_basicas?.sin_gluten && !result.caracteristicas_basicas?.sin_lacteos && (
              <span className="text-slate-500 italic text-sm">Información de dietas no disponible</span>
            )}
          </div>
        </div>

        {/* Halachic Explanation */}
        <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl relative overflow-hidden">
          <h3 className="text-white font-bold text-lg mb-3">Detalle del Análisis Halájico</h3>
          
          {result.phase === 'fast' ? (
            <div className="flex flex-col gap-3 animate-pulse">
              <div className="h-4 bg-slate-700/50 rounded w-full"></div>
              <div className="h-4 bg-slate-700/50 rounded w-5/6"></div>
              <div className="h-4 bg-slate-700/50 rounded w-4/6"></div>
              <div className="mt-2 flex items-center gap-2 text-emerald-400/80 text-sm font-medium">
                <div className="w-4 h-4 border-2 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin"></div>
                Redactando desglose halájico detallado...
              </div>
            </div>
          ) : (
            <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-line animate-in fade-in duration-700">
              {result.explicacion_halajica?.includes('**Análisis Detallado:**') 
                ? result.explicacion_halajica.split('**Análisis Detallado:**')[1]?.trim() 
                : result.explicacion_halajica || 'No se brindaron detalles adicionales de la lógica.'}
            </p>
          )}
        </div>

        {/* Recipe Suggestion */}
        {result.receta_sugerida && (
          <div className="bg-gradient-to-br from-emerald-900/40 to-slate-800/80 p-6 rounded-3xl shadow-lg border border-emerald-500/40 backdrop-blur-xl mt-2 relative overflow-hidden">
            <h3 className="text-emerald-400 font-bold text-lg mb-2 flex items-center gap-2">
              <span className="text-2xl">👨‍🍳</span> {result.receta_sugerida.nombre}
            </h3>
            <p className="text-emerald-100/90 text-sm leading-relaxed">
              {result.receta_sugerida.descripcion}
            </p>
          </div>
        )}

        <button
          onClick={onBack}
          className="mt-2 w-full text-slate-400 font-bold py-5 hover:bg-slate-800 border border-transparent hover:border-slate-700 rounded-[2rem] transition-all"
        >
          ❮ Escanear Otro Producto
        </button>
      </div>
    </div>
  );
}

function ChaguimWidget({ userOrigin }: { userOrigin: string }) {
  // Hardcoded current upcoming holiday estimation
  const daysLeft = 17;
  
  return (
    <div className="h-full min-h-[600px] flex flex-col items-center justify-center p-6 lg:p-10 animate-in fade-in slide-in-from-right-8 duration-700">
      <div className="w-full max-w-md bg-gradient-to-b from-slate-800 to-slate-900 border border-emerald-500/30 rounded-[2.5rem] p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
        
        <div className="flex flex-col items-center text-center relative z-10">
          <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mb-6 border border-emerald-500/40">
            <span className="text-4xl">🍷</span>
          </div>
          
          <h2 className="text-emerald-400 font-bold tracking-widest uppercase text-xs mb-2">Próxima Festividad</h2>
          <h3 className="text-4xl font-black text-white mb-2 drop-shadow-md">Pesaj</h3>
          
          <div className="bg-slate-950/50 py-2 px-6 rounded-full border border-slate-700/50 mb-8 inline-block">
            <span className="text-slate-300 font-medium">Faltan <span className="text-emerald-400 font-bold text-lg">{daysLeft}</span> días</span>
          </div>
          
          <div className="w-full bg-slate-800/50 rounded-2xl p-5 border border-slate-700/50 text-left">
            <h4 className="text-white font-bold mb-3 text-sm flex items-center gap-2">
              <span className="bg-slate-700 w-6 h-6 rounded-full flex items-center justify-center text-xs">📋</span>
              Preparación ({userOrigin === 'ashkenazi' ? 'Ashkenazí' : 'Sefaradí'})
            </h4>
            <ul className="text-sm text-slate-400 space-y-2">
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>Limpieza a fondo y venta de Jametz antes del 12 de Abril.</span>
              </li>
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>{userOrigin === 'ashkenazi' ? 'Kitniyot (arroz, legumbres) no están permitidos.' : 'Kitniyot (arroz, frijoles) estricto según la costumbre sefaradí que se siga.'}</span>
              </li>
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>Usa la cámara de KosherScan para certificar sellos de &quot;Kosher L&apos;Pesach&quot;.</span>
              </li>
            </ul>
          </div>
          
          <button className="mt-6 w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-2xl transition-all shadow-[0_8px_20px_rgba(16,185,129,0.2)]">
            Ver Guía Completa Pesaj
          </button>
        </div>
      </div>
    </div>
  );
}

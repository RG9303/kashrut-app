'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useLanguage } from '@/hooks/useLanguage';
import { Camera, Upload, ShieldAlert, CheckCircle2, ChevronLeft, Search, ZoomIn } from 'lucide-react';

interface Deteccion {
  bbox: number[];
  descripcion: string;
  especie_aproximada: string;
  confianza: string;
  severidad: string;
  accion_recomendada: string;
}

interface InsectResult {
  confianza_global: string;
  detecciones: Deteccion[];
  resumen?: string;
}

const TEXTS = {
  esp: {
    title: "Escáner de Insectos",
    description: "Coloca la hoja, vegetal o producto sobre una superficie clara y presiona escanear. El motor IA buscará insectos camuflados.",
    noSource: "Sin origen de captura",
    inspecting: "Inspeccionando...",
    activateCamera: "Activar Cámara",
    scan: "Escanear",
    scanAnother: "Escanear Otra",
    uploadGallery: "Subir desde Galería",
    status: "Status",
    globalConfidence: "Confianza Global",
    clean: "Limpio",
    suspects: "Sospechosos",
    severity: "Severidad",
    recommendation: "Recomendación",
    noInsect: "Ningún Insecto Detectado",
    noInsectDesc: "La IA no encontró signos de infestación. Aún así, sigue los procedimientos Halájicos de lavado regulares.",
    waitingImage: "Esperando Imagen",
    waitingImageDesc: "Toma una foto de alta calidad a las hojas con buena iluminación natural para obtener los mejores resultados de la IA.",
    cameraError: "No se pudo acceder a la cámara.",
    serverError: "Error de servidor",
    noStatus: "No se pudo detectar el estatus de insectos.",
    errorPrefix: "Error: "
  },
  eng: {
    title: "Insect Scanner",
    description: "Place the leaf, vegetable or product on a clear surface and press scan. The AI engine will look for camouflaged insects.",
    noSource: "No capture source",
    inspecting: "Inspecting...",
    activateCamera: "Activate Camera",
    scan: "Scan",
    scanAnother: "Scan Another",
    uploadGallery: "Upload from Gallery",
    status: "Status",
    globalConfidence: "Global Confidence",
    clean: "Clean",
    suspects: "Suspects",
    severity: "Severity",
    recommendation: "Recommendation",
    noInsect: "No Insect Detected",
    noInsectDesc: "The AI found no signs of infestation. Even so, follow the regular Halachic washing procedures.",
    waitingImage: "Waiting for Image",
    waitingImageDesc: "Take a high-quality photo of the leaves with good natural lighting to get the best AI results.",
    cameraError: "Could not access the camera.",
    serverError: "Server error",
    noStatus: "Could not detect the insect status.",
    errorPrefix: "Error: "
  }
};

export default function Insectos() {
  const { lang } = useLanguage();
  const t = TEXTS[lang];

  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<InsectResult | null>(null);
  
  const [isCameraActive, setIsCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const startCamera = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' }
        });
        if (videoRef.current) {
            videoRef.current.srcObject = stream;
            setIsCameraActive(true);
            setImagePreview(null);
            setResult(null);
        }
    } catch (err) {
        console.error("Error accessing camera:", err);
        alert(t.cameraError);
    }
  };

  const stopCamera = () => {
      if (videoRef.current?.srcObject) {
          const stream = videoRef.current.srcObject as MediaStream;
          stream.getTracks().forEach(track => track.stop());
          videoRef.current.srcObject = null;
          setIsCameraActive(false);
      }
  };

  useEffect(() => {
      return () => stopCamera();
  }, []);

  const captureAndScan = async () => {
      if (!videoRef.current || !canvasRef.current) return;
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
      setImagePreview(dataUrl);
      
      const blob = await (await fetch(dataUrl)).blob();
      await executeScan(blob);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
      if (!e.target.files?.length) return;
      const file = e.target.files[0];
      const url = URL.createObjectURL(file);
      setImagePreview(url);
      setResult(null);
      stopCamera();
      await executeScan(file);
  };

  const executeScan = async (imageBlob: Blob | File) => {
      setIsScanning(true);
      setResult(null);
      
      const formData = new FormData();
      formData.append('images', imageBlob, 'capture.jpg');

      try {
          const res = await fetch('/api/analyze_insects', {
              method: 'POST',
              body: formData
          });

          if (!res.ok) {
              const err = await res.json();
              throw new Error(err.detail || t.serverError);
          }

          const data = await res.json();
          // The API returns the whole object, including insect_scanner
          if (data.insect_scanner) {
             setResult(data.insect_scanner);
          } else {
             throw new Error(t.noStatus);
          }

          if (isCameraActive) stopCamera();
      } catch (error: any) {
          console.error(error);
          alert(t.errorPrefix + error.message);
      } finally {
          setIsScanning(false);
      }
  };

  return (
    <main className="flex min-h-screen flex-col p-4 lg:p-10 gap-8 max-w-[1400px] mx-auto bg-[#0a1128] text-white">
      <header className="w-full flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-slate-400 hover:text-white transition bg-slate-800 p-2 rounded-full">
              <ChevronLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-2xl lg:text-3xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 flex items-center gap-2">
             {t.title}
          </h1>
        </div>
      </header>

      <div className="flex flex-col lg:flex-row gap-8 w-full">
        {/* Left Column: Scanner and Preview */}
        <div className="flex-1 w-full max-w-lg mx-auto lg:max-w-none flex flex-col items-center bg-slate-900 border border-slate-700/50 rounded-[2.5rem] p-6 lg:p-10 shadow-2xl relative">
            <p className="text-slate-400 text-center mb-6 text-sm">
                {t.description}
            </p>

            <div className="relative w-full aspect-square max-w-[400px] rounded-3xl overflow-hidden bg-slate-950 border-2 border-slate-700/50 my-2 flex justify-center items-center shadow-inner group">
                
                {imagePreview ? (
                    <>
                        <img src={imagePreview} className="absolute inset-0 w-full h-full object-contain z-10" alt="Preview" />
                        {/* Overlay Bounding Boxes */}
                        {result && result.detecciones && result.detecciones.map((d, idx) => {
                            // Gemini standard is usually [ymin, xmin, ymax, xmax] scaled 1000
                            const [ymin, xmin, ymax, xmax] = d.bbox; 
                            
                            // Let's protect against different coordinate scales
                            let maxVal = Math.max(ymin, xmin, ymax, xmax);
                            let scale = 1000;
                            if (maxVal <= 100 && maxVal > 1) scale = 100;
                            if (maxVal <= 1) scale = 1;

                            const top = (ymin / scale) * 100;
                            const left = (xmin / scale) * 100;
                            const h = ((ymax - ymin) / scale) * 100;
                            const w = ((xmax - xmin) / scale) * 100;

                            const isHigh = d.severidad.toLowerCase() === 'alta' || d.severidad.toLowerCase() === 'high';
                            const borderColor = isHigh ? 'border-rose-500' : 'border-amber-400';
                            const bgColor = isHigh ? 'bg-rose-500/20' : 'bg-amber-400/20';

                            return (
                                <div 
                                    key={idx}
                                    className={`absolute ${borderColor} ${bgColor} border-2 z-20 flex items-start justify-start shadow-[0_0_10px_rgba(0,0,0,0.5)]`}
                                    style={{
                                        top: `${top}%`, left: `${left}%`, width: `${w}%`, height: `${h}%`
                                    }}
                                >
                                    <span className="bg-black/80 text-white text-[9px] px-1 font-bold absolute -top-4 whitespace-nowrap rounded-t-sm">
                                        {d.especie_aproximada.substring(0, 15)} {d.confianza}
                                    </span>
                                </div>
                            )
                        })}
                    </>
                ) : (
                    <>
                        <video ref={videoRef} autoPlay playsInline muted className={`absolute inset-0 w-full h-full object-cover z-10 ${isCameraActive ? 'opacity-100' : 'opacity-0'}`} />
                        <canvas ref={canvasRef} className="hidden" />
                        {!isCameraActive && (
                            <div className="flex flex-col items-center opacity-40">
                                <Search className="w-16 h-16 mb-2" />
                                <span className="font-bold tracking-widest uppercase text-xs">{t.noSource}</span>
                            </div>
                        )}
                    </>
                )}

                {isScanning && (
                    <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-md flex flex-col items-center justify-center z-30">
                        <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                        <span className="font-bold animate-pulse text-emerald-100 drop-shadow-lg text-lg">{t.inspecting}</span>
                    </div>
                )}
            </div>

            <div className="w-full flex gap-3 mt-6">
                {!isCameraActive && !imagePreview ? (
                    <button onClick={startCamera} className="flex-1 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white font-bold py-4 rounded-2xl shadow-[0_8px_25px_rgba(16,185,129,0.3)] transition-all active:scale-95 flex items-center justify-center gap-2">
                        <Camera className="w-5 h-5" /> {t.activateCamera}
                    </button>
                ) : isCameraActive ? (
                    <button onClick={captureAndScan} disabled={isScanning} className="flex-1 bg-gradient-to-r from-emerald-500 to-cyan-500 shadow-[0_8px_25px_rgba(16,185,129,0.3)] text-white font-bold py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2 text-lg">
                        <ZoomIn className="w-6 h-6" /> {t.scan}
                    </button>
                ) : (
                    <button onClick={() => setImagePreview(null)} className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-3.5 rounded-2xl transition-all border border-slate-700">
                        {t.scanAnother}
                    </button>
                )}
            </div>

            <div className="w-full mt-4 flex flex-col gap-3">
                <input type="file" ref={fileInputRef} onChange={handleFileUpload} accept="image/*" className="hidden" />
                <button onClick={() => fileInputRef.current?.click()} disabled={isScanning} className="w-full bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-300 font-semibold py-3.5 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2">
                <Upload className="w-5 h-5 opacity-70" /> {t.uploadGallery}
                </button>
            </div>
        </div>

        {/* Right Column: AI Results */}
        <div className="flex-1 w-full flex flex-col gap-6">
           {result ? (
               <div className="w-full animate-in slide-in-from-right-8 duration-500 flex flex-col gap-6">
                   
                   {/* Confidence Metric */}
                   <div className={`p-6 rounded-[2rem] border shadow-2xl flex items-center justify-between
                      ${result.detecciones.length === 0 ? 'bg-emerald-900/30 border-emerald-500/50' : 'bg-rose-900/30 border-rose-500/50'}`}>
                       <div className="flex flex-col gap-1">
                           <span className="uppercase text-[11px] tracking-widest font-bold opacity-60">{t.status}</span>
                           <h3 className="text-3xl font-black">
                               {result.detecciones.length === 0 ? t.clean : `${result.detecciones.length} ${t.suspects}`}
                           </h3>
                       </div>
                       <div className="flex flex-col items-end gap-1">
                          <span className="uppercase text-[11px] tracking-widest font-bold opacity-60">{t.globalConfidence}</span>
                          <span className="text-2xl font-bold bg-slate-900 px-4 py-1 rounded-xl border border-slate-700 text-cyan-400">
                              {result.confianza_global}
                          </span>
                       </div>
                   </div>

                   {/* Detections List */}
                   {result.detecciones.length > 0 ? (
                       <div className="flex flex-col gap-4">
                           {result.detecciones.map((det, i) => (
                               <div key={i} className="bg-slate-900 border border-slate-700/60 p-5 rounded-3xl flex gap-4 overflow-hidden relative">
                                   {/* Status Indicator */}
                                   <div className={`w-1.5 absolute left-0 top-0 bottom-0 ${det.severidad.toLowerCase() === 'alta' || det.severidad.toLowerCase() === 'high' ? 'bg-rose-500' : 'bg-amber-400'}`}></div>
                                   
                                   <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center flex-shrink-0 border border-slate-700">
                                       <ShieldAlert className={`w-6 h-6 ${det.severidad.toLowerCase() === 'alta' || det.severidad.toLowerCase() === 'high' ? 'text-rose-400' : 'text-amber-400'}`} />
                                   </div>
                                   <div className="flex flex-col w-full">
                                       <div className="flex justify-between items-start mb-1">
                                           <h4 className="font-bold text-lg capitalize">{det.especie_aproximada || det.descripcion}</h4>
                                           <span className="text-xs bg-slate-800 px-2 py-0.5 rounded text-slate-300 font-bold tracking-wider">
                                               {det.confianza} AI
                                           </span>
                                       </div>
                                       <div className="grid grid-cols-2 gap-2 mt-2">
                                           <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                                              <span className="text-[10px] text-slate-500 uppercase block mb-0.5">{t.severity}</span>
                                              <span className={`text-sm font-semibold ${det.severidad.toLowerCase() === 'alta' || det.severidad.toLowerCase() === 'high' ? 'text-rose-400' : 'text-amber-400'}`}>{det.severidad}</span>
                                           </div>
                                           <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                                              <span className="text-[10px] text-slate-500 uppercase block mb-0.5">{t.recommendation}</span>
                                              <span className="text-sm font-semibold text-slate-200 line-clamp-1">{det.accion_recomendada}</span>
                                           </div>
                                       </div>
                                   </div>
                               </div>
                           ))}
                       </div>
                   ) : (
                       <div className="bg-emerald-900/20 border border-emerald-500/30 p-10 rounded-3xl flex flex-col items-center text-center">
                           <CheckCircle2 className="w-16 h-16 text-emerald-400 mb-4" />
                           <h4 className="text-emerald-100 font-bold text-xl mb-2">{t.noInsect}</h4>
                           <p className="text-emerald-200/60 text-sm max-w-sm">
                               {t.noInsectDesc}
                           </p>
                       </div>
                   )}
               </div>
           ) : (
               <div className="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-slate-700/50 bg-slate-800/10 rounded-[2.5rem] p-12 text-slate-500">
                    <ShieldAlert className="w-16 h-16 mb-4 opacity-20" />
                    <h3 className="text-lg font-medium text-slate-400 mb-2 text-center">{t.waitingImage}</h3>
                    <p className="text-sm text-center max-w-xs text-slate-500">
                      {t.waitingImageDesc}
                    </p>
               </div>
           )}
        </div>
      </div>
    </main>
  );
}


'use client';

import { useState, useRef, useEffect } from 'react';
import { useLanguage } from '@/hooks/useLanguage';
import Link from 'next/link';
import { Camera, Upload, AlertCircle, CheckCircle2, Smartphone, Focus, Leaf, Droplets, Beef, ShieldAlert, Wheat, ShieldQuestion, QrCode, XCircle, Menu, History } from 'lucide-react';

interface ScanItem {
  id: number;
  resultado: string;
  hechsher: string;
  barcode: string;
  fullData?: any;
}


const TEXTS = {
  esp: {
    sidebarTitle: "Inicio (Escáner)",
    megaGuide: "Mega-Guía Chaguim",
    kosherRecipe: "Recetario Kosher",
    soon: "Pronto",
    hebrewCalendar: "Calendario Hebreo",
    logosCatalog: "Catálogo de Logos",
    insectScanner: "Escáner de Insectos",
    kashrutAlerts: "Alertas de Kashrut",
    kashrutAlertsDesc: "Avisos urgentes sobre productos que perdieron certificación.",
    analyzeProduct: "Analizar Producto",
    photoOrCode: "Fotografía el producto o ingresa su código",
    makeSureLabels: "Asegúrate de que etiquetas sean legibles",
    analyzingAI: "Analizando IA...",
    activateCamera: "Activar Cámara",
    stopCamera: "Detener Cámara",
    capture: "Capturar",
    orAlternatives: "O Alternativas",
    uploadGallery: "Subir desde Galería",
    insertBarcode: "Insertar Código Barras (EAN/UPC)",
    search: "Buscar",
    custom: "Costumbre",
    ashkenazi: "Ashkenazí",
    sephardi: "Sefaradí",
    country: "País",
    mexico: "México",
    usa: "Estados Unidos",
    argentina: "Argentina",
    israel: "Israel",
    spain: "España",
    otherCountry: "Otro País",
    importantNote: "Nota importante:",
    importantNoteDesc1: "{t.importantNoteDesc1}",
    importantNoteDesc2: "{t.importantNoteDesc2}",
    importantNoteDesc3: "{t.importantNoteDesc3}",
    waitingAnalysis: "Esperando Análisis",
    scanProductCamera: "{t.scanProductCamera}",
    finalStatus: "Estatus Final",
    aiConfidence: "Certeza IA",
    quickSummary: "Resumen Rápido",
    seal: "Sello",
    none: "Ninguno",
    category: "Categoría",
    openFoodFacts: "Registro OpenFoodFacts",
    product: "Producto",
    unknown: "Desconocido",
    brand: "Marca",
    relevantAlerts: "Alertas Relevantes",
    additionalFilters: "Filtros Adicionales",
    vegan: "Vegano",
    glutenFree: "Sin Gluten",
    dairyFree: "Sin Lácteos",
    dietInfoNA: "Información de dietas no disponible",
    halachicDetail: "Detalle del Análisis Halájico",
    draftingHalachic: "{t.draftingHalachic}",
    noLogicDetails: "No se brindaron detalles adicionales de la lógica.",
    scanAnother: "{t.scanAnother}",
    recentHistory: "{t.recentHistory}",
    hide: "Ocultar",
    viewRecipe: "Ver Receta",
    requiredIngredients: "Ingredientes Requeridos",
    noDetailed: "No detallados.",
    prepSteps: "Pasos de Preparación",
    generalInstructions: "Sigue las instrucciones generales de cocina.",
    nextHoliday: "{t.nextHoliday}",
    daysLeft: "Faltan",
    days: "días",
    preparation: "Preparación",
    pesachPrep1: "{t.pesachPrep1}",
    pesachPrep2Ashk: "Kitniyot (arroz, legumbres) no están permitidos.",
    pesachPrep2Sef: "Kitniyot (arroz, frijoles) estricto según la costumbre sefaradí que se siga.",
    pesachPrep3: "Usa la cámara de KosherScan para certificar sellos de \"Kosher L'Pesach\".",
    viewFullGuide: "{t.viewFullGuide}"
  },
  eng: {
    sidebarTitle: "Home (Scanner)",
    megaGuide: "Mega-Guide Chaguim",
    kosherRecipe: "Kosher Recipes",
    soon: "Soon",
    hebrewCalendar: "Hebrew Calendar",
    logosCatalog: "Logos Catalog",
    insectScanner: "Insect Scanner",
    kashrutAlerts: "Kashrut Alerts",
    kashrutAlertsDesc: "Urgent notices about products that lost certification.",
    analyzeProduct: "Analyze Product",
    photoOrCode: "Photograph the product or enter its code",
    makeSureLabels: "Make sure labels are readable",
    analyzingAI: "Analyzing AI...",
    activateCamera: "Activate Camera",
    stopCamera: "Stop Camera",
    capture: "Capture",
    orAlternatives: "Or Alternatives",
    uploadGallery: "Upload from Gallery",
    insertBarcode: "Insert Barcode (EAN/UPC)",
    search: "Search",
    custom: "Custom",
    ashkenazi: "Ashkenazi",
    sephardi: "Sephardic",
    country: "Country",
    mexico: "Mexico",
    usa: "United States",
    argentina: "Argentina",
    israel: "Israel",
    spain: "Spain",
    otherCountry: "Other Country",
    importantNote: "Important Note:",
    importantNoteDesc1: "This artificial intelligence analysis is a technological assistance tool for reference.",
    importantNoteDesc2: "It does not substitute the opinion or review of a competent Rabbinic authority in any way.",
    importantNoteDesc3: "When in doubt about the Kashrut of an ingredient or product, always consult your trusted Mashgiach or expert Rabbi.",
    waitingAnalysis: "Waiting for Analysis",
    scanProductCamera: "Scan a product with the camera on the left or enter its barcode to break down the result here.",
    finalStatus: "Final Status",
    aiConfidence: "AI Confidence",
    quickSummary: "Quick Summary",
    seal: "Seal",
    none: "None",
    category: "Category",
    openFoodFacts: "OpenFoodFacts Record",
    product: "Product",
    unknown: "Unknown",
    brand: "Brand",
    relevantAlerts: "Relevant Alerts",
    additionalFilters: "Additional Filters",
    vegan: "Vegan",
    glutenFree: "Gluten Free",
    dairyFree: "Dairy Free",
    dietInfoNA: "Diet information not available",
    halachicDetail: "Halachic Analysis Detail",
    draftingHalachic: "Drafting detailed halachic breakdown...",
    noLogicDetails: "No additional logic details were provided.",
    scanAnother: "Scan Another Product",
    recentHistory: "Recent History",
    hide: "Hide",
    viewRecipe: "View Recipe",
    requiredIngredients: "Required Ingredients",
    noDetailed: "Not detailed.",
    prepSteps: "Preparation Steps",
    generalInstructions: "Follow general cooking instructions.",
    nextHoliday: "Next Holiday",
    daysLeft: "Remaining",
    days: "days",
    preparation: "Preparation",
    pesachPrep1: "Thorough cleaning and sale of Chametz before April 12.",
    pesachPrep2Ashk: "Kitniyot (rice, legumes) are not allowed.",
    pesachPrep2Sef: "Kitniyot (rice, beans) strict according to the Sephardic custom followed.",
    pesachPrep3: "Use the KosherScan camera to certify \"Kosher L'Pesach\" seals.",
    viewFullGuide: "View Full Pesach Guide"
  }
};

export default function Home() {
  const { lang } = useLanguage();
  const t = TEXTS[lang];
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState<any>(null); // Keeping any as it was there

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
  const [scanHistory, setScanHistory] = useState<ScanItem[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const storedOrigin = localStorage.getItem('userOrigin');
    const storedCountry = localStorage.getItem('userCountry');
    const storedChaguim = localStorage.getItem('chaguimAlerts');
    const storedRecipes = localStorage.getItem('kosherRecipes');
    const storedHistory = localStorage.getItem('scanHistory');
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedOrigin) setUserOrigin(storedOrigin);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedCountry) setUserCountry(storedCountry);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedChaguim) setChaguimAlerts(storedChaguim);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedRecipes) setKosherRecipes(storedRecipes);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedHistory) {
      try {
        setScanHistory(JSON.parse(storedHistory));
      } catch (e) {}
    }
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

      setScanHistory(prev => {
        const item = {
          id: Date.now(),
          resultado: data.resultado || t.unknown,
          hechsher: data.sello_detectado?.nombre || t.none,
          barcode: finalBarcode || 'Análisis Visual',
          fullData: data
        };
        const updated = [item, ...prev].slice(0, 5);
        localStorage.setItem('scanHistory', JSON.stringify(updated));
        return updated;
      });

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
    <main className="flex min-h-screen flex-col p-4 lg:p-10 gap-8 max-w-[1400px] mx-auto relative">
      
      {/* Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="fixed inset-0 z-50 flex">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)}></div>
          <div className="relative w-80 max-w-[85vw] bg-slate-900 border-r border-slate-700/50 flex flex-col h-full shadow-2xl animate-in slide-in-from-left duration-300">
            <div className="p-6 border-b border-slate-800 flex justify-between items-center">
              <h2 className="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-emerald-600 tracking-tight">KosherScan</h2>
              <button onClick={() => setIsSidebarOpen(false)} className="text-slate-400 hover:text-white transition-colors">
                <XCircle className="w-6 h-6"/>
              </button>
            </div>
            <div className="p-4 flex flex-col gap-2 overflow-y-auto">
              <button onClick={() => setIsSidebarOpen(false)} className="flex items-center gap-3 p-3.5 rounded-xl hover:bg-slate-800/80 text-slate-300 hover:text-white transition-colors w-full text-left font-medium border border-transparent hover:border-slate-700/50">
                <Camera className="w-5 h-5 text-emerald-500" /> {t.sidebarTitle}
              </button>
              <Link href="/chaguim" className="flex items-center gap-3 p-3.5 rounded-xl hover:bg-slate-800/80 text-slate-300 hover:text-white transition-colors w-full text-left font-medium border border-transparent hover:border-slate-700/50">
                <span className="text-xl w-5 flex justify-center">🍷</span> {t.megaGuide}
              </Link>
              <div className="flex items-center gap-3 p-3.5 rounded-xl opacity-60 cursor-not-allowed text-slate-400 w-full text-left font-medium">
                <span className="text-xl w-5 flex justify-center">👨‍🍳</span> {t.kosherRecipe} <span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded-full ml-auto font-bold uppercase tracking-widest border border-slate-700">{t.soon}</span>
              </div>
              <Link href="/calendario" className="flex items-center gap-3 p-3.5 rounded-xl hover:bg-slate-800/80 text-slate-300 hover:text-white transition-colors w-full text-left font-medium border border-transparent hover:border-slate-700/50">
                <span className="text-xl w-5 flex justify-center">📅</span> {t.hebrewCalendar}
              </Link>
              <Link href="/logos" className="flex items-center gap-3 p-3.5 rounded-xl hover:bg-slate-800/80 text-slate-300 hover:text-white transition-colors w-full text-left font-medium border border-transparent hover:border-slate-700/50">
                <span className="text-xl w-5 flex justify-center">🔖</span> {t.logosCatalog}
              </Link>
              <Link href="/insectos" className="flex items-center gap-3 p-3.5 rounded-xl hover:bg-slate-800/80 text-slate-300 hover:text-white transition-colors w-full text-left font-medium border border-transparent hover:border-slate-700/50">
                <span className="text-xl w-5 flex justify-center">🐛</span> {t.insectScanner}
              </Link>
              
              <div className="mt-8 pt-6 border-t border-slate-800">
               <div className="flex flex-col gap-1 p-4 rounded-xl bg-gradient-to-br from-rose-500/10 to-transparent border border-rose-500/20 text-rose-300 w-full text-left opacity-90 backdrop-blur-sm shadow-inner cursor-not-allowed">
                 <div className="flex items-center gap-2 font-bold mb-1">
                   <ShieldAlert className="w-5 h-5 text-rose-500" /> {t.kashrutAlerts}
                 </div>
                 <p className="text-xs text-rose-400/80 leading-relaxed pr-2">{t.kashrutAlertsDesc}</p>
                 <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2.5 py-1 rounded-full w-fit mt-2 font-bold uppercase tracking-wider border border-rose-500/30">{t.soon}</span>
               </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-col lg:flex-row gap-8 w-full">
        {/* LEFT COLUMN: Scanner / Input */}
        <div className="flex-1 w-full max-w-lg mx-auto lg:max-w-none flex flex-col h-full lg:sticky lg:top-10">

        <header className="w-full flex justify-between items-center mb-8">
          <button onClick={() => setIsSidebarOpen(true)} className="text-2xl text-slate-300 hover:text-emerald-400 transition transform hover:scale-110 active:scale-95" aria-label="Abrir Menú">☰</button>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            KosherScan
          </h1>
          <Link href="/settings" className="text-2xl text-slate-300 hover:text-white transition">⚙️</Link>
        </header>

        <div className="w-full bg-slate-800/80 border border-slate-700/50 rounded-[2.5rem] p-8 lg:p-12 backdrop-blur-xl shadow-2xl flex flex-col items-center flex-grow">

          <h2 className="text-3xl font-bold mt-2 mb-2 tracking-tight text-white text-center">{t.analyzeProduct}</h2>

          <div className="flex flex-col gap-2 mt-4 mb-8 text-slate-400 text-sm">
            <div className="flex items-center justify-center gap-2">
              <Smartphone className="w-4 h-4 text-emerald-400" />
              <span>{t.photoOrCode}</span>
            </div>
            <div className="flex items-center justify-center gap-2">
              <Focus className="w-4 h-4 text-emerald-400" />
              <span>{t.makeSureLabels}</span>
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
                <span className="font-bold animate-pulse text-emerald-100 drop-shadow-lg text-lg">{t.analyzingAI}</span>
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
                <Camera className="w-5 h-5" /> {t.activateCamera}
              </button>
            ) : (
              <>
                <button
                  onClick={stopCamera}
                  disabled={isScanning}
                  className="bg-slate-700 hover:bg-slate-600 text-white font-semibold px-5 py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center"
                  title={t.stopCamera}
                >
                  <XCircle className="w-6 h-6" />
                </button>
                <button
                  onClick={takePhotoAndScan}
                  disabled={isScanning}
                  className="flex-1 bg-gradient-to-r from-emerald-500 to-emerald-600 shadow-[0_8px_25px_rgba(16,185,129,0.3)] hover:brightness-110 text-white font-bold py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2 text-lg"
                >
                  <Camera className="w-6 h-6" /> {t.capture}
                </button>
              </>
            )}
          </div>

          <div className="w-full flex items-center gap-4 my-6 opacity-50">
            <div className="h-px bg-slate-500 flex-1"></div>
            <span className="text-sm font-medium uppercase tracking-wider text-slate-300">{t.orAlternatives}</span>
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
              <Upload className="w-5 h-5 opacity-70" /> {t.uploadGallery}
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
                  placeholder={t.insertBarcode}
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
              <label className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">{t.custom}</label>
              <select
                value={userOrigin}
                onChange={(e) => setUserOrigin(e.target.value)}
                className="bg-transparent text-white font-medium focus:outline-none appearance-none cursor-pointer"
              >
                <option value="ashkenazi" className="bg-slate-800">{t.ashkenazi}</option>
                <option value="sefaradi" className="bg-slate-800">{t.sephardi}</option>
              </select>
            </div>

            <div className="w-px h-8 bg-slate-700"></div>

            <div className="flex flex-col flex-1 pl-2">
              <label className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">{t.country}</label>
              <select
                value={userCountry}
                onChange={(e) => setUserCountry(e.target.value)}
                className="bg-transparent text-white font-medium focus:outline-none appearance-none cursor-pointer"
              >
                <option value="México" className="bg-slate-800">{t.mexico}</option>
                <option value="Estados Unidos" className="bg-slate-800">{t.usa}</option>
                <option value="Argentina" className="bg-slate-800">{t.argentina}</option>
                <option value="Israel" className="bg-slate-800">{t.israel}</option>
                <option value="España" className="bg-slate-800">{t.spain}</option>
                <option value="Otro" className="bg-slate-800">{t.otherCountry}</option>
              </select>
            </div>
          </div>

          {/* Disclaimer Node */}
          <div className="mt-8 pt-5 border-t border-slate-700 flex items-start gap-3 w-full opacity-70">
            <ShieldQuestion className="w-5 h-5 text-emerald-500/80 flex-shrink-0 mt-0.5" />
            <p className="text-[11px] text-slate-300 leading-relaxed">
              <strong>{t.importantNote}</strong> {t.importantNoteDesc1} <strong>{t.importantNoteDesc2}</strong> {t.importantNoteDesc3}
            </p>
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN: Results */}
      <div className="flex-1 w-full max-w-lg mx-auto lg:max-w-none h-full min-h-[500px]">
        {result ? (
          <ResultView result={result} onBack={() => setResult(null)} t={t} />
        ) : (
          <div className="h-full min-h-[600px] flex flex-col items-center justify-center border-2 border-dashed border-slate-700/50 bg-slate-800/20 rounded-[2.5rem] p-12 text-slate-500">
            <div className="w-24 h-24 mb-6 rounded-full bg-slate-800/50 flex items-center justify-center">
              <Leaf className="w-10 h-10 opacity-30" />
            </div>
            <h3 className="text-xl font-medium text-slate-400 mb-2 text-center">{t.waitingAnalysis}</h3>
            <p className="text-sm text-center max-w-xs text-slate-500">
              {t.scanProductCamera}
            </p>
          </div>
        )}
      </div>
      </div> {/* End Top Columns Wrapper */}

      {/* BOTTOM WIDGETS */}
      <div className="w-full grid grid-cols-1 lg:grid-cols-2 gap-8 mt-4">
        {/* Scan History Widget */}
        {scanHistory.length > 0 && (
          <ScanHistoryWidget history={scanHistory} onRestore={(d) => setResult({ ...d, phase: 'detailed' })} t={t} />
        )}
        
        {/* Chaguim Widget */}
        {chaguimAlerts === 'true' && (
          <ChaguimWidget userOrigin={userOrigin} t={t} />
        )}
      </div>

    </main>
  );
}

function ResultView({ result, onBack, t }: { result: any, onBack: () => void, t: any }) {
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
          <span className="text-sm font-semibold uppercase tracking-widest opacity-80 mb-1">{t.finalStatus}</span>
          <div className="flex items-center gap-3 text-4xl font-black tracking-tight drop-shadow-md">
            {isKosher ? <CheckCircle2 className="w-10 h-10" /> : <ShieldAlert className="w-10 h-10" />}
            {status}
          </div>
          <div className="mt-4 flex flex-col backdrop-blur-md bg-white/20 px-4 py-3 rounded-xl text-white/90 border border-white/20 max-w-sm">
            <span className="font-bold text-xs uppercase tracking-wider mb-1 opacity-80">{t.aiConfidence}</span>
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
            <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-2 block">{t.seal}</span>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-emerald-500/10 text-emerald-400 rounded-2xl flex items-center justify-center font-black text-xl border border-emerald-500/20 shadow-inner">
                {result.sello_detectado?.nombre ? result.sello_detectado.nombre.substring(0, 2).toUpperCase() : '??'}
              </div>
              <div className="flex flex-col">
                <div className="font-bold text-lg text-white leading-tight">
                  {result.sello_detectado?.nombre || t.none}
                </div>
                {result.sello_detectado?.nombre && result.sello_detectado.nombre !== t.none && (
                  <span className="text-xs text-slate-400 font-medium">
                    {result.sello_detectado.pais || ''} • {result.sello_detectado.confianza || ''}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Category Card */}
          <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl">
            <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-2 block">{t.category}</span>
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
                <span className="text-slate-400">{t.product}</span>
                <span className="text-white font-medium text-right">{result.off_data.product_name || t.unknown}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">{t.brand}</span>
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
          <span className="text-slate-400 font-semibold text-xs uppercase tracking-wider mb-4 block">{t.additionalFilters}</span>
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
              <span className="text-slate-500 italic text-sm">{t.dietInfoNA}</span>
            )}
          </div>
        </div>

        {/* Halachic Explanation */}
        <div className="bg-slate-800/80 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl relative overflow-hidden">
          <h3 className="text-white font-bold text-lg mb-3">{t.halachicDetail}</h3>
          
          {result.phase === 'fast' ? (
            <div className="flex flex-col gap-3 animate-pulse">
              <div className="h-4 bg-slate-700/50 rounded w-full"></div>
              <div className="h-4 bg-slate-700/50 rounded w-5/6"></div>
              <div className="h-4 bg-slate-700/50 rounded w-4/6"></div>
              <div className="mt-2 flex items-center gap-2 text-emerald-400/80 text-sm font-medium">
                <div className="w-4 h-4 border-2 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin"></div>
                {t.draftingHalachic}
              </div>
            </div>
          ) : (
            <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-line animate-in fade-in duration-700">
              {result.explicacion_halajica?.includes('**Análisis Detallado:**') 
                ? result.explicacion_halajica.split('**Análisis Detallado:**')[1]?.trim() 
                : result.explicacion_halajica || t.noLogicDetails}
            </p>
          )}
        </div>

        {/* Recipe Suggestion */}
        {result.receta_sugerida && result.receta_sugerida.nombre && !result.receta_sugerida.nombre.includes('N/A') && (
          <RecipeCard recipe={result.receta_sugerida} t={t} />
        )}

        <button
          onClick={onBack}
          className="mt-2 w-full text-slate-400 font-bold py-5 hover:bg-slate-800 border border-transparent hover:border-slate-700 rounded-[2rem] transition-all"
        >
          ❮ {t.scanAnother}
        </button>
      </div>
    </div>
  );
}

function ChaguimWidget({ userOrigin, t }: { userOrigin: string, t: any }) {
  const [daysLeft, setDaysLeft] = useState(0);

  useEffect(() => {
    // Pesach starts evening of April 1, 2026.
    const pesajDate = new Date('2026-04-01T18:00:00');
    const today = new Date();
    const diff = Math.ceil((pesajDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setDaysLeft(diff > 0 ? diff : 0);
  }, []);
  
  return (
    <div className="w-full flex-grow flex flex-col items-center justify-center p-6 lg:p-10 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="w-full max-w-md bg-gradient-to-b from-slate-800 to-slate-900 border border-emerald-500/30 rounded-[2.5rem] p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
        
        <div className="flex flex-col items-center text-center relative z-10">
          <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mb-6 border border-emerald-500/40">
            <span className="text-4xl">🍷</span>
          </div>
          
          <h2 className="text-emerald-400 font-bold tracking-widest uppercase text-xs mb-2">{t.nextHoliday}</h2>
          <h3 className="text-4xl font-black text-white mb-2 drop-shadow-md">Pesaj</h3>
          
          <div className="bg-slate-950/50 py-2 px-6 rounded-full border border-slate-700/50 mb-8 inline-block">
            <span className="text-slate-300 font-medium">{t.daysLeft} <span className="text-emerald-400 font-bold text-lg">{daysLeft}</span> {t.days}</span>
          </div>
          
          <div className="w-full bg-slate-800/50 rounded-2xl p-5 border border-slate-700/50 text-left">
            <h4 className="text-white font-bold mb-3 text-sm flex items-center gap-2">
              <span className="bg-slate-700 w-6 h-6 rounded-full flex items-center justify-center text-xs">📋</span>
              {t.preparation} ({userOrigin === 'ashkenazi' ? 'Ashkenazí' : 'Sefaradí'})
            </h4>
            <ul className="text-sm text-slate-400 space-y-2">
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>{t.pesachPrep1}</span>
              </li>
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>{userOrigin === 'ashkenazi' ? t.pesachPrep2Ashk : t.pesachPrep2Sef}</span>
              </li>
              <li className="flex gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span>{t.pesachPrep3}</span>
              </li>
            </ul>
          </div>
          
          <Link href="/chaguim" className="mt-6 w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-2xl transition-all shadow-[0_8px_20px_rgba(16,185,129,0.2)] text-center block">
            {t.viewFullGuide}
          </Link>
        </div>
      </div>
    </div>
  );
}

function ScanHistoryWidget({ history, onRestore, t }: { history: ScanItem[], onRestore: (data: any) => void, t: any }) {
  return (
    <div className="w-full bg-slate-800/80 border border-slate-700/50 rounded-[2.5rem] p-8 shadow-xl relative overflow-hidden flex flex-col h-full animate-in fade-in slide-in-from-bottom-8 duration-500">
      <h3 className="text-white font-bold text-xl mb-6 flex items-center gap-2">
        <History className="w-6 h-6 text-emerald-400" />
        {t.recentHistory}
      </h3>
      <div className="flex flex-col gap-4 overflow-y-auto pr-2 max-h-[400px]">
        {history.map((item) => {
          const isKosher = item.resultado?.toUpperCase().includes('KOSHER') && !item.resultado?.toUpperCase().includes('NO');
          const isDudoso = item.resultado?.toUpperCase().includes('DUDOSO');
          const statusColor = isKosher ? 'text-emerald-400' : isDudoso ? 'text-yellow-400' : 'text-red-400';
          const badgeClass = isKosher ? 'bg-emerald-500/10 border-emerald-500/20' : isDudoso ? 'bg-yellow-500/10 border-yellow-500/20' : 'bg-red-500/10 border-red-500/20';

          return (
            <div 
              key={item.id} 
              onClick={() => item.fullData && onRestore(item.fullData)}
              className="bg-slate-900/50 border border-slate-700/30 p-4 rounded-2xl flex justify-between items-center hover:border-emerald-500/50 transition-colors cursor-pointer group shadow-sm hover:shadow-emerald-500/10"
            >
              <div className="flex flex-col">
                <span className={`font-bold transition-colors group-hover:text-emerald-300 ${statusColor}`}>{item.resultado}</span>
                <span className="text-slate-400 text-xs mt-1 font-mono transition-colors group-hover:text-slate-300">{item.barcode}</span>
              </div>
              <div className={`px-3 py-1 rounded-full border transition-all ${badgeClass} group-hover:bg-opacity-20`}>
                <span className={`font-bold text-xs ${statusColor}`}>{item.hechsher}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function RecipeCard({ recipe, t }: { recipe: any, t: any }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div 
      onClick={() => setIsExpanded(!isExpanded)}
      className="bg-gradient-to-br from-emerald-900/40 to-slate-800/80 p-6 rounded-3xl shadow-lg border border-emerald-500/40 backdrop-blur-xl mt-2 relative overflow-hidden cursor-pointer transition-all hover:border-emerald-500/70 group"
    >
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-emerald-400 font-bold text-lg flex items-center gap-2 group-hover:text-emerald-300 transition-colors">
          {recipe.nombre}
        </h3>
        <span className="text-emerald-500/50 text-xs font-bold uppercase tracking-widest bg-emerald-500/10 px-3 py-1.5 rounded-full group-hover:bg-emerald-500/20 transition-colors">
          {isExpanded ? t.hide : t.viewRecipe}
        </span>
      </div>
      <p className="text-emerald-100/90 text-sm leading-relaxed mb-4">
        {recipe.descripcion}
      </p>

      {isExpanded && (
        <div className="animate-in fade-in slide-in-from-top-4 duration-500 border-t border-emerald-500/20 pt-4 mt-2">
           <div className="w-full h-40 bg-slate-900/80 rounded-2xl mb-5 overflow-hidden relative border border-emerald-500/20 shadow-inner">
              <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80" alt="Receta" className="w-full h-full object-cover opacity-60 mix-blend-luminosity hover:mix-blend-normal hover:opacity-100 transition-all duration-700" />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent pointer-events-none"></div>
           </div>
           
           <h4 className="text-white font-bold tracking-tight mb-3 flex items-center gap-2">
             <span className="bg-emerald-500/20 w-6 h-6 rounded-full flex items-center justify-center text-emerald-400 text-xs shadow-inner border border-emerald-500/30">1</span>
             {t.requiredIngredients}
           </h4>
           <ul className="pl-5 text-emerald-50 text-sm mb-6 space-y-2 font-medium">
             {Array.isArray(recipe.ingredientes_receta) 
                ? recipe.ingredientes_receta.map((ing: string, i: number) => (
                   <li key={i} className="flex items-start gap-2">
                     <span className="text-emerald-500 text-lg leading-none mt-0.5">•</span> {ing}
                   </li>
                 ))
                : <li>{recipe.ingredientes_receta || t.noDetailed}</li>
             }
           </ul>

           <h4 className="text-white font-bold tracking-tight mb-3 flex items-center gap-2">
             <span className="bg-emerald-500/20 w-6 h-6 rounded-full flex items-center justify-center text-emerald-400 text-xs shadow-inner border border-emerald-500/30">2</span>
             {t.prepSteps}
           </h4>
           <ol className="pl-2 text-emerald-50 text-sm space-y-3">
             {Array.isArray(recipe.pasos_receta) 
                ? recipe.pasos_receta.map((paso: string, i: number) => (
                   <li key={i} className="flex gap-3 bg-slate-900/40 p-3 rounded-xl border border-slate-700/30">
                     <span className="text-emerald-500 font-black opacity-60">0{i+1}</span>
                     <span className="leading-relaxed">{paso}</span>
                   </li>
                 ))
                : <li className="bg-slate-900/40 p-3 rounded-xl border border-slate-700/30">{recipe.pasos_receta || t.generalInstructions}</li>
             }
           </ol>
        </div>
      )}
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Globe, MapPin, Search, XCircle, Info, BookOpen, ShieldCheck } from 'lucide-react';

interface LogoInfo {
  id: number;
  category: string;
  name: string;
  description: string;
  color: string;
  symbol: React.ReactNode;
  fullDetails: {
    history: string;
    rabbi: string;
    strictness: string;
    regions: string;
  };
}

export default function LogosPage() {

  const logos: LogoInfo[] = [
    {
      id: 1,
      category: 'Globales',
      name: 'Orthodox Union (OU)',
      description: 'La agencia certificadora más grande y reconocida a nivel mundial. Certifica más del 65% del mercado kosher global.',
      color: 'from-blue-600 to-indigo-900',
      symbol: (
        <div className="relative w-16 h-16 border-[4px] border-white rounded-full flex items-center justify-center font-black text-white text-3xl shadow-lg">
          U
        </div>
      ),
      fullDetails: {
         history: 'Fundada en 1898, la Unión Ortodoxa introdujo la supervisión moderna corporativa, creando el concepto del Mashguíaj industrial.',
         rabbi: 'Rabino Menachem Genack (CEO Kashrut Division)',
         strictness: 'Altamente Confiable (Estándar de Oro Global).',
         regions: 'Estados Unidos, Europa, Israel y más de 100 países.'
      }
    },
    {
      id: 2,
      category: 'Globales',
      name: 'OK Kosher',
      description: 'Con sede central en Brooklyn, es la segunda agencia internacional con mayor cantidad de productos certificados.',
      color: 'from-emerald-500 to-teal-800',
      symbol: (
        <div className="relative border-[4px] border-white w-14 h-16 rounded-[40%] flex items-center justify-center font-black text-white text-3xl shadow-lg">
          K
        </div>
      ),
      fullDetails: {
         history: 'Iniciada en 1935 por el Rabino Berel Levy, fue pionera en informatizar los datos de ingredientes industriales a nivel mundial.',
         rabbi: 'Rabino Don Yoel Levy (Z"L) / Rabino Chaim Fogelman',
         strictness: 'Mehadrin. Suelen exigir lineamientos "Cholov Yisroel" y "Pas Yisroel" en lácteos y panadería.',
         regions: 'Norteamérica, Asia y Países del Este.'
      }
    },
    {
      id: 3,
      category: 'Globales',
      name: 'Star-K',
      description: 'Líder en tecnología y halajá (Baltimore). Son la autoridad principal en la certificación de software y electrodomésticos.',
      color: 'from-amber-500 to-orange-800',
      symbol: (
        <div className="relative w-20 h-20 flex items-center justify-center scale-90">
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-b-[50px] border-b-white opacity-80 mt-[-15px]"></div>
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-t-[50px] border-t-white opacity-80 mt-[15px]"></div>
          <span className="font-black text-amber-800 z-10 text-2xl">K</span>
        </div>
      ),
      fullDetails: {
         history: 'Empezó como un consejo local de Baltimore y creció dictando regulaciones mundiales sobre el uso sabático ("Sabbath Mode") de refrigeradores y hornos.',
         rabbi: 'Rabino Moshe Heinemann',
         strictness: 'Nivel superior. Estrictos estándares Glatt Kosher.',
         regions: 'Norteamérica, Europa del Este, China e India.'
      }
    },
    {
      id: 8,
      category: 'Globales',
      name: 'Kof-K (Kosher Supervision)',
      description: 'Agencia pionera ubicada en New Jersey. Destaca por el uso de tecnologías de rastreo y es sumamente popular en alimentos estadounidenses.',
      color: 'from-red-500 to-pink-800',
      symbol: (
        <div className="relative w-16 h-16 flex items-center justify-center font-black text-white text-[40px] shadow-lg">
          <span className="absolute text-5xl opacity-40">כ</span>
          <span className="z-10">K</span>
        </div>
      ),
      fullDetails: {
         history: 'KOF-K fue la primera agencia Kashrut en utilizar un sistema informático global para monitorear millones de ingredientes.',
         rabbi: 'Rabino Aharon Yehuda Dr. Zecharia Senter (Z"L)',
         strictness: 'Confiabilidad Ortodoxa Excelente.',
         regions: 'América del Norte, Israel, Asia Continental.'
      }
    },
    {
      id: 9,
      category: 'Globales',
      name: 'cRc (Chicago Rabbinical Council)',
      description: 'Una de las agencias regionales más gigantes y respetadas, famosa por sus listas de bebidas y recomendaciones de pescados.',
      color: 'from-slate-700 to-slate-900',
      symbol: (
        <div className="relative w-20 h-16 flex flex-col items-center justify-center">
            <div className="w-0 h-0 border-l-[35px] border-l-transparent border-r-[35px] border-r-transparent border-b-[55px] border-b-white absolute"></div>
            <span className="z-10 font-bold text-slate-800 text-sm mt-3 tracking-widest">cRc</span>
        </div>
      ),
      fullDetails: {
         history: 'El cRc opera como una entidad sin fines de lucro en el Medio Oeste. Sus documentos, apps y listas de licores y whiskies son consultados mundialmente.',
         rabbi: 'Rabino Sholem Fishbane',
         strictness: 'Ortodoxa Rigurosa, recomendada extensamente.',
         regions: 'Norteamérica central e internacional.'
      }
    },
    {
      id: 4,
      category: 'Israelies',
      name: 'Badatz Edah HaChareidis',
      description: 'Considerado uno de los estándares más rigurosos (Mehadrin) de Jerusalén. Altamente confiable mundialmente.',
      color: 'from-red-600 to-rose-900',
      symbol: (
        <div className="font-bold text-white text-2xl tracking-widest bg-red-950/40 px-3 py-2 rounded-xl border border-white/20">
          בָדָ״ץ
        </div>
      ),
      fullDetails: {
         history: 'Formado antes de la creación del Estado de Israel, rige sobre las comunidades más ultraortodoxas de Jerusalén con procesos inflexibles sin indulgencias modernas.',
         rabbi: 'Tribunal Rabínico de la Edah HaChareidis (Jerusalén)',
         strictness: 'Máximo rigor (Chumra). Aceptada universalmente sin cuestionamientos (Glatt / Mehadrin).',
         regions: 'Jerusalén, Bet Shemesh, e importaciones premium israelíes.'
      }
    },
    {
      id: 5,
      category: 'Israelies',
      name: 'Rabinato Principal de Israel',
      description: 'Rabbanut. Sello estatal base requerido para cualquier producción, importación o venta legal de un producto Kosher dentro del Estado de Israel.',
      color: 'from-sky-500 to-blue-800',
      symbol: (
        <div className="w-16 h-14 bg-white rounded-md flex flex-col items-center justify-center text-sky-800 font-bold shadow-lg border-2 border-white/80">
          <span className="text-[10px] uppercase">Kosher</span>
          <span className="text-xl leading-none">כשר</span>
        </div>
      ),
      fullDetails: {
         history: 'Creado por el Estado de Israel, funciona como la ley base nacional de Kashrut. Hay dos niveles: "Rabbanut Regular" y "Rabbanut Mehadrin".',
         rabbi: 'Gran Rabinato (Rishon LeZion y Gran Rabino Ashkenazí)',
         strictness: 'Básico (Regular) a veces depende de permisos (Heter Mejira). El Mehadrin es más riguroso.',
         regions: 'Nacional (Todo el territorio del Estado de Israel).'
      }
    },
    {
      id: 6,
      category: 'Locales',
      name: 'KMD (Maguen David México)',
      description: 'La principal autoridad certificadora de la comunidad Judeo-Mexicana en Ciudad de México. Manejan directrices estrictas.',
      color: 'from-slate-600 to-slate-900',
      symbol: (
        <div className="flex border-4 border-white h-12 items-center px-2 bg-blue-600 font-black text-white text-xl tracking-tighter">
          KMD
        </div>
      ),
      fullDetails: {
         history: 'Pilar del resurgimiento Kosher en México, el KMD es el sello local más prolífico, garantizando que millones de productos mexicanos cumplan las leyes de Kashrut para exportación y consumo doméstico.',
         rabbi: 'Comité Rabínico de la Comunidad Maguen David',
         strictness: 'Ortodoxo Estricto y rigurosa política de Jalav Israel y Bishul Yisroel local.',
         regions: 'Ciudad de México, Cancún, Centroamérica.'
      }
    },
    {
      id: 7,
      category: 'Locales',
      name: 'One Kosher',
      description: 'Certificadora internacional basada en México que expande su alcance y popularidad certificando alimentos industrializados para toda Latinoamérica.',
      color: 'from-purple-600 to-fuchsia-900',
      symbol: (
        <div className="flex items-center gap-1 font-black text-white text-2xl">
          <span className="bg-white text-purple-800 px-2 py-1 rounded">1</span>
          <span>K</span>
        </div>
      ),
      fullDetails: {
         history: 'Fundada como una solución dinámica y corporativa en México, ha logrado digitalizar sus listas de Kashrut permitiendo a los turistas en Latam acceder a enormes bibliotecas de productos locales seguros.',
         rabbi: 'Rabino Nissim L. Michan / KMD Network',
         strictness: 'Riguroso Estándar Internacional.',
         regions: 'México, Sudamérica, el Caribe, USA (importaciones hispanas).'
      }
    }
  ];

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLogo, setSelectedLogo] = useState<LogoInfo | null>(null);

  const filteredLogos = searchTerm 
    ? logos.filter(l => l.name.toLowerCase().includes(searchTerm.toLowerCase()) || l.description.toLowerCase().includes(searchTerm.toLowerCase()))
    : [];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans pb-20 selection:bg-emerald-500/30">
      
      {/* 
        ========================================================================
        ENCYCLOPEDIA MODAL (DIALOG) 
        ======================================================================== 
      */}
      {selectedLogo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 animate-in fade-in duration-300">
           {/* Backdrop */}
           <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={() => setSelectedLogo(null)}></div>
           
           {/* Modal Body */}
           <div className="relative bg-slate-900 w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-[2.5rem] shadow-2xl border border-slate-700">
              {/* Header Gradient */}
              <div className={`h-40 w-full flex items-center justify-center relative overflow-hidden bg-gradient-to-br ${selectedLogo.color}`}>
                 <button onClick={() => setSelectedLogo(null)} className="absolute top-4 right-4 text-white/50 hover:text-white transition-colors bg-black/20 p-1.5 rounded-full z-20">
                   <XCircle className="w-8 h-8" />
                 </button>
                 <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                 <div className="relative z-10 scale-125 drop-shadow-2xl">{selectedLogo.symbol}</div>
              </div>

              {/* Content Body */}
              <div className="p-8">
                 <div className="flex items-center gap-3 mb-2">
                   <span className="text-[10px] bg-emerald-500/20 text-emerald-400 font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-emerald-500/20">{selectedLogo.category}</span>
                 </div>
                 <h2 className="text-3xl font-black text-white mb-6 tracking-tight">{selectedLogo.name}</h2>
                 
                 <div className="space-y-6">
                   <div className="bg-slate-800/50 p-5 rounded-2xl border border-slate-700/50">
                     <h4 className="flex items-center gap-2 text-emerald-400 font-bold text-sm mb-2 uppercase tracking-wide">
                        <BookOpen className="w-4 h-4" /> Historia de la Agencia
                     </h4>
                     <p className="text-slate-300 text-sm leading-relaxed">{selectedLogo.fullDetails.history}</p>
                   </div>

                   <div className="bg-slate-800/50 p-5 rounded-2xl border border-slate-700/50">
                     <h4 className="flex items-center gap-2 text-blue-400 font-bold text-sm mb-2 uppercase tracking-wide">
                        <ShieldCheck className="w-4 h-4" /> Nivel Halájico (Strictness)
                     </h4>
                     <p className="text-slate-300 text-sm leading-relaxed">{selectedLogo.fullDetails.strictness}</p>
                   </div>

                   <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                     <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-700/30">
                       <span className="block text-slate-500 text-xs font-bold uppercase mb-1">Autoridad Rabínica</span>
                       <span className="text-slate-200 text-sm">{selectedLogo.fullDetails.rabbi}</span>
                     </div>
                     <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-700/30">
                       <span className="block text-slate-500 text-xs font-bold uppercase mb-1">Región Principal</span>
                       <span className="text-slate-200 text-sm">{selectedLogo.fullDetails.regions}</span>
                     </div>
                   </div>
                 </div>
                 
                 <button onClick={() => setSelectedLogo(null)} className="w-full mt-8 py-4 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white font-bold rounded-2xl transition-all">
                   Cerrar Enciclopedia
                 </button>
              </div>
           </div>
        </div>
      )}
      {/* ======================================================================== */}


      <div className="max-w-5xl mx-auto p-4 lg:p-8">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-10 px-2 mt-4 lg:mt-0">
          <div className="flex items-center gap-4">
            <Link href="/" className="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center border border-slate-700 hover:bg-slate-700 transition-colors shadow-lg">
              <ArrowLeft className="text-slate-400 w-6 h-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">Catálogo Enciclopédico</h1>
              <p className="text-slate-400 font-medium text-sm flex items-center gap-1">
                Diccionario Kashrut Global
              </p>
            </div>
          </div>
        </div>

        {/* Search Header Design */}
        <div className="bg-slate-800/50 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl mb-10 relative focus-within:border-emerald-500/50 transition-colors">
           <div className="flex items-center gap-4">
             <div className="w-14 h-14 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-black flex-shrink-0">
               <Search className="w-7 h-7" />
             </div>
             <div className="flex-grow">
               <input 
                 type="text"
                 placeholder="Busca cualquier certificado..."
                 value={searchTerm}
                 onChange={(e) => setSearchTerm(e.target.value)}
                 className="w-full bg-transparent border-none text-white text-xl md:text-2xl font-bold placeholder-slate-500 focus:outline-none focus:ring-0 p-0"
               />
               <p className="text-slate-400 text-xs md:text-sm mt-1">Escribe cualquier letra (ej. OU, cRc) para abrir instantáneamente la enciclopedia oculta del sello.</p>
             </div>
           </div>
        </div>

        {searchTerm ? (
          <div className="mb-10 animate-in fade-in duration-300">
            <h2 className="text-2xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
               Resultados Enciclopédicos ({filteredLogos.length})
            </h2>
            {filteredLogos.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredLogos.map(logo => (
                  <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-emerald-500/40 rounded-3xl overflow-hidden hover:border-emerald-400 transition-all shadow-[0_4px_20px_rgba(16,185,129,0.15)] group">
                    <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                       <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                       <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                       <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                         <span className="opacity-0 group-hover:opacity-100 bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-full text-xs transition-opacity transform translate-y-4 group-hover:translate-y-0">Estudiar Detalle</span>
                       </div>
                    </div>
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-lg text-white">{logo.name}</h3>
                        <span className="text-[10px] bg-slate-900 border border-slate-700 px-2 py-1 rounded-md text-emerald-400 font-bold uppercase tracking-wider">{logo.category}</span>
                      </div>
                      <p className="text-sm text-slate-400 leading-relaxed line-clamp-2">{logo.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16 bg-slate-800/20 rounded-3xl border border-slate-700/50">
                <Info className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <h3 className="text-xl text-slate-300 font-bold">No encontrado en Enciclopedia</h3>
                <p className="text-slate-500 mt-2 max-w-md mx-auto">No tenemos este sello pre-programado. Utiliza la cámara principal en la pantalla de "Inicio" para que la Inteligencia Artificial analice visualmente el sello desconocido que tienes en tus manos.</p>
                <Link href="/" className="mt-6 inline-block bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white px-6 py-2.5 rounded-xl font-bold transition-colors">Volver al Escáner IA</Link>
              </div>
            )}
          </div>
        ) : (
          <>
            {/* Globales */}
        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <Globe className="text-blue-400 w-6 h-6" /> Sellos Globales
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {logos.filter(l => l.category === 'Globales').map(logo => (
              <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl group relative">
                <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 z-20 transition-opacity bg-black/50 p-1.5 rounded-full backdrop-blur-md">
                   <Info className="w-4 h-4 text-white" />
                </div>
                <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                   <div className="absolute bottom-2 left-3 text-white/40 text-[10px] font-bold uppercase tracking-widest group-hover:opacity-0 transition-opacity">
                     Clic para Enciclopedia
                   </div>
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-lg text-white mb-2">{logo.name}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed line-clamp-2">{logo.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Israelies */}
        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <MapPin className="text-amber-400 w-6 h-6" /> Agencias en Israel
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {logos.filter(l => l.category === 'Israelies').map(logo => (
              <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl flex flex-col sm:flex-row group relative">
                <div className={`h-full sm:w-40 bg-gradient-to-br ${logo.color} flex items-center justify-center p-8 sm:p-0 relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out flex-shrink-0`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                   <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                     <Info className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                   </div>
                </div>
                <div className="p-6 flex-grow">
                  <h3 className="font-bold text-lg text-white mb-2">{logo.name}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{logo.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Locales (Mexico) */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <MapPin className="text-emerald-400 w-6 h-6" /> Locales (Latinoamérica)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {logos.filter(l => l.category === 'Locales').map(logo => (
              <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl flex flex-col sm:flex-row group relative">
                <div className={`h-full sm:w-40 bg-gradient-to-br ${logo.color} flex items-center justify-center p-8 sm:p-0 relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out flex-shrink-0`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                   <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                     <Info className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                   </div>
                </div>
                <div className="p-6 flex-grow">
                  <h3 className="font-bold text-lg text-white mb-2">{logo.name}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{logo.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        </>
        )}

      </div>
    </div>
  );
}

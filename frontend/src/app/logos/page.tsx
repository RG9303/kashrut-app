'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Globe, MapPin, Search } from 'lucide-react';

export default function LogosPage() {

  const logos = [
    {
      id: 1,
      category: 'Globales',
      name: 'Orthodox Union (OU)',
      description: 'La agencia certificadora más grande y reconocida a nivel mundial. Su sede está en Nueva York y certifica más del 65% del mercado kosher global.',
      color: 'from-blue-600 to-indigo-900',
      symbol: (
        <div className="relative w-16 h-16 border-[4px] border-white rounded-full flex items-center justify-center font-black text-white text-3xl shadow-lg">
          U
        </div>
      )
    },
    {
      id: 2,
      category: 'Globales',
      name: 'OK Kosher',
      description: 'Con sede central en Brooklyn, es la segunda agencia internacional con mayor cantidad de productos certificados mediante procesos industriales rígidos.',
      color: 'from-emerald-500 to-teal-800',
      symbol: (
        <div className="relative border-[4px] border-white w-14 h-16 rounded-[40%] flex items-center justify-center font-black text-white text-3xl shadow-lg">
          K
        </div>
      )
    },
    {
      id: 3,
      category: 'Globales',
      name: 'Star-K',
      description: 'Líder en tecnología y halajá (Baltimore). Son la autoridad principal en la certificación de software, electrodomésticos y modo sabático.',
      color: 'from-amber-500 to-orange-800',
      symbol: (
        <div className="relative w-20 h-20 flex items-center justify-center">
          {/* Custom CSS Star of David approximation */}
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-b-[50px] border-b-white opacity-80 mt-[-15px]"></div>
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-t-[50px] border-t-white opacity-80 mt-[15px]"></div>
          <span className="font-black text-amber-800 z-10 text-2xl">K</span>
        </div>
      )
    },
    {
      id: 4,
      category: 'Israelies',
      name: 'Badatz Edah HaChareidis',
      description: 'Considerado uno de los estándares más rigurosos (Mehadrin) de Jerusalén. Altamente confiable para cruzar cualquier diferencia de costumbres entre ashkenazím y sefaradím.',
      color: 'from-red-600 to-rose-900',
      symbol: (
        <div className="font-bold text-white text-2xl tracking-widest bg-red-950/40 px-3 py-2 rounded-xl border border-white/20">
          בָדָ״ץ
        </div>
      )
    },
    {
      id: 5,
      category: 'Israelies',
      name: 'Rabinato Principal',
      description: 'Rabbinate of Israel (Rabbanut). Sello estatal base requerido para cualquier producción, importación o venta legal de un producto Kosher dentro del Estado de Israel.',
      color: 'from-sky-500 to-blue-800',
      symbol: (
        <div className="w-16 h-14 bg-white rounded-md flex flex-col items-center justify-center text-sky-800 font-bold shadow-lg border-2 border-white/80">
          <span className="text-[10px] uppercase">Kosher</span>
          <span className="text-xl leading-none">כשר</span>
        </div>
      )
    },
    {
      id: 6,
      category: 'Locales',
      name: 'KMD (Maguen David)',
      description: 'La principal autoridad certificadora de la comunidad Judeo-Mexicana en Ciudad de México. Manejan directrices estrictas y certificación "Jalav Israel".',
      color: 'from-slate-600 to-slate-900',
      symbol: (
        <div className="flex border-4 border-white h-12 items-center px-2 bg-blue-600 font-black text-white text-xl tracking-tighter">
          KMD
        </div>
      )
    },
    {
      id: 7,
      category: 'Locales',
      name: 'One Kosher',
      description: 'Certificadora internacional basada en México (K-MD) que expande su alcance y popularidad certificando alimentos industrializados e importados para Latam.',
      color: 'from-purple-600 to-fuchsia-900',
      symbol: (
        <div className="flex items-center gap-1 font-black text-white text-2xl">
          <span className="bg-white text-purple-800 px-2 py-1 rounded">1</span>
          <span>K</span>
        </div>
      )
    }
  ];

  const [searchTerm, setSearchTerm] = useState('');

  const filteredLogos = searchTerm 
    ? logos.filter(l => l.name.toLowerCase().includes(searchTerm.toLowerCase()) || l.description.toLowerCase().includes(searchTerm.toLowerCase()))
    : [];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans pb-20 selection:bg-emerald-500/30">
      <div className="max-w-5xl mx-auto p-4 lg:p-8">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-10 px-2 mt-4 lg:mt-0">
          <div className="flex items-center gap-4">
            <Link href="/" className="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center border border-slate-700 hover:bg-slate-700 transition-colors shadow-lg">
              <ArrowLeft className="text-slate-400 w-6 h-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">Catálogo de Logos</h1>
              <p className="text-slate-400 font-medium text-sm flex items-center gap-1">
                Kashrut Verification
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
                 placeholder="Busca un sello (ej. OU, Star-K, etc.)"
                 value={searchTerm}
                 onChange={(e) => setSearchTerm(e.target.value)}
                 className="w-full bg-transparent border-none text-white text-xl md:text-2xl font-bold placeholder-slate-500 focus:outline-none focus:ring-0 p-0"
               />
               <p className="text-slate-400 text-xs md:text-sm mt-1">Escribe cualquier letra para autocompletar e identificar rápidamente la agencia certificadora.</p>
             </div>
           </div>
        </div>

        {searchTerm ? (
          <div className="mb-10 animate-in fade-in duration-300">
            <h2 className="text-2xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
               Resultados de Búsqueda ({filteredLogos.length})
            </h2>
            {filteredLogos.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredLogos.map(logo => (
                  <div key={logo.id} className="bg-slate-800/40 border border-emerald-500/40 rounded-3xl overflow-hidden hover:border-emerald-400 transition-all shadow-[0_4px_20px_rgba(16,185,129,0.15)] group">
                    <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                       <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                       <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                    </div>
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-lg text-white">{logo.name}</h3>
                        <span className="text-[10px] bg-slate-900 border border-slate-700 px-2 py-1 rounded-md text-emerald-400 font-bold uppercase tracking-wider">{logo.category}</span>
                      </div>
                      <p className="text-sm text-slate-400 leading-relaxed">{logo.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16 bg-slate-800/20 rounded-3xl border border-slate-700/50">
                <Search className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <h3 className="text-xl text-slate-300 font-bold">No se encontraron sellos</h3>
                <p className="text-slate-500 mt-2">Intenta buscar con otro nombre o palabra clave.</p>
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
              <div key={logo.id} className="bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl group">
                <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                   <div className="absolute bottom-2 right-3 text-white/50 text-[10px] font-bold uppercase tracking-widest">
                     Recreación Visual
                   </div>
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-lg text-white mb-2">{logo.name}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{logo.description}</p>
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
              <div key={logo.id} className="bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl flex flex-col sm:flex-row group">
                <div className={`h-full sm:w-40 bg-gradient-to-br ${logo.color} flex items-center justify-center p-8 sm:p-0 relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out flex-shrink-0`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
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
              <div key={logo.id} className="bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl flex flex-col sm:flex-row group">
                <div className={`h-full sm:w-40 bg-gradient-to-br ${logo.color} flex items-center justify-center p-8 sm:p-0 relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out flex-shrink-0`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
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

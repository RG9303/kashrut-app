'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, BookOpen, Clock, CheckCircle2, AlertTriangle, Calendar } from 'lucide-react';

export default function ChaguimPage() {
  const [userOrigin, setUserOrigin] = useState('ashkenazi');
  const [daysLeft, setDaysLeft] = useState(0);
  
  useEffect(() => {
    const origin = localStorage.getItem('userOrigin');
    if (origin) setUserOrigin(origin);
    const pesajDate = new Date('2026-04-01T18:00:00');
    const today = new Date();
    const diff = Math.ceil((pesajDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setDaysLeft(diff > 0 ? diff : 0);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans pb-20 selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto p-4 lg:p-8">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-10 px-2 mt-4 lg:mt-0">
          <div className="flex items-center gap-4">
            <Link href="/" className="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center border border-slate-700 hover:bg-slate-700 transition-colors shadow-lg">
              <ArrowLeft className="text-slate-400 w-6 h-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">Guía Chaguim</h1>
              <p className="text-emerald-500 font-medium text-sm flex items-center gap-1">
                Preparación Activa
              </p>
            </div>
          </div>
        </div>

        {/* Hero Section */}
        <div className="bg-gradient-to-br from-emerald-900/40 to-slate-800/80 p-8 rounded-[2.5rem] shadow-lg border border-emerald-500/30 backdrop-blur-xl mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 flex flex-col items-center text-center">
            <div className="w-24 h-24 bg-emerald-500/20 rounded-full flex items-center justify-center mb-6 border border-emerald-500/40">
              <span className="text-5xl">🍷</span>
            </div>
            
            <h2 className="text-emerald-400 font-bold tracking-widest uppercase text-sm mb-2 flex items-center gap-2 justify-center">
              <Calendar className="w-4 h-4"/> Próxima Festividad
            </h2>
            <h3 className="text-5xl font-black text-white mb-4 drop-shadow-md">Pesaj 2026</h3>
            
            <div className="bg-slate-950/50 py-3 px-8 rounded-full border border-slate-700/50 mb-4 inline-block shadow-inner">
              <span className="text-slate-300 font-medium text-lg">Faltan <span className="text-emerald-400 font-black text-2xl mx-1">{daysLeft}</span> días</span>
            </div>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              Del 1 al 9 de Abril de 2026. Es la festividad de la libertad, donde se prohíbe el consumo y posesión de Jametz.
            </p>
          </div>
        </div>

        {/* Content Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Card: Prohibición de Jametz */}
          <div className="bg-slate-800/50 rounded-[2rem] p-6 border border-slate-700/50 hover:border-slate-600 transition-colors">
            <div className="flex gap-4 items-start mb-4">
              <div className="w-10 h-10 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
                <AlertTriangle className="w-5 h-5 text-red-400" />
              </div>
              <div>
                <h3 className="text-white font-bold text-lg">Venta y Limpieza</h3>
                <p className="text-slate-400 text-sm mt-1">El Jametz debe desaparecer.</p>
              </div>
            </div>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>Limpiar minuciosamente toda la casa, cajones, cocina y auto antes del 1 de Abril.</span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>Vender el Jametz sobrante a través de tu Rabino local.</span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>Realizar Bedikat Jametz (Búsqueda) la noche anterior con vela y pluma.</span>
              </li>
            </ul>
          </div>

          {/* Card: Custom Rules (Ashkenazi/Sephardi) */}
          <div className="bg-slate-800/50 rounded-[2rem] p-6 border border-slate-700/50 hover:border-slate-600 transition-colors">
            <div className="flex gap-4 items-start mb-4">
              <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                <BookOpen className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <h3 className="text-white font-bold text-lg">Leyes de {userOrigin === 'ashkenazi' ? 'Ashkenazím' : 'Sefaradim'}</h3>
                <p className="text-slate-400 text-sm mt-1">Reglas basadas en tu costumbre actual.</p>
              </div>
            </div>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>
                  {userOrigin === 'ashkenazi' 
                    ? 'Prohibición absoluta de Kitniyot. No se permite arroz, maíz, frijoles, lentejas ni derivados como jarabe de maíz.' 
                    : 'Permitido el consumo de Kitniyot (arroz, frijoles, etc.) si se revisan meticulosamente según la tradición familiar.'}
                </span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>
                  {userOrigin === 'ashkenazi'
                    ? 'Los productos Kosher L\'Pesach que dicen "Leojlei Kitniyot" NO son aptos para ti.'
                    : 'Puedes consumir productos marcados como Kosher L\'Pesach "Leojlei Kitniyot".'}
                </span>
              </li>
            </ul>
          </div>

          {/* Card: Kasherización */}
          <div className="bg-slate-800/50 rounded-[2rem] p-6 border border-slate-700/50 hover:border-slate-600 transition-colors md:col-span-2">
            <div className="flex gap-4 items-start mb-4">
              <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
                <Clock className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <h3 className="text-white font-bold text-lg">Kasherización de la Cocina</h3>
                <p className="text-slate-400 text-sm mt-1">Preparando el entorno físico.</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">Hornos</strong>
                <p className="text-xs text-slate-300">No usar 24 horas. Limpiar con químico fuerte. Encender a máxima temperatura por 1 hora o usar función Self-Clean.</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">Microondas</strong>
                <p className="text-xs text-slate-300">No usar 24 horas. Limpiar bien. Hervir un vaso de agua dentro por 10 minutos hasta que el vapor cubra las paredes.</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">Bacha / Tarja</strong>
                <p className="text-xs text-slate-300">Limpiar y dejar secar 24h. Verter agua hirviendo directamente de una olla al fuego sobre todas las superficies.</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">Cubiertos de Metal</strong>
                <p className="text-xs text-slate-300">Hagalá: Sumergir individualmente en una olla con agua hirviendo a borbotones (previamente kasherizada para Pesaj).</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

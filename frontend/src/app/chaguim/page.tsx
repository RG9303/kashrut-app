'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, BookOpen, Clock, CheckCircle2, AlertTriangle, Calendar } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';

const TEXTS = {
  esp: {
    title: "Guía Chaguim",
    subtitle: "Preparación Activa",
    next: "Próxima Festividad",
    daysLeft: "Faltan",
    days: "días",
    heroDesc: "Del 1 al 9 de Abril de 2026. Es la festividad de la libertad, donde se prohíbe el consumo y posesión de Jametz.",
    cleanTitle: "Venta y Limpieza",
    cleanDesc: "El Jametz debe desaparecer.",
    clean1: "Limpiar minuciosamente toda la casa, cajones, cocina y auto antes del 1 de Abril.",
    clean2: "Vender el Jametz sobrante a través de tu Rabino local.",
    clean3: "Realizar Bedikat Jametz (Búsqueda) la noche anterior con vela y pluma.",
    lawsTitleAshk: "Leyes de Ashkenazím",
    lawsTitleSef: "Leyes de Sefaradim",
    lawsDesc: "Reglas basadas en tu costumbre actual.",
    laws1Ashk: "Prohibición absoluta de Kitniyot. No se permite arroz, maíz, frijoles, lentejas ni derivados como jarabe de maíz.",
    laws1Sef: "Permitido el consumo de Kitniyot (arroz, frijoles, etc.) si se revisan meticulosamente según la tradición familiar.",
    laws2Ashk: 'Los productos Kosher L\'Pesach que dicen "Leojlei Kitniyot" NO son aptos para ti.',
    laws2Sef: 'Puedes consumir productos marcados como Kosher L\'Pesach "Leojlei Kitniyot".',
    kashTitle: "Kasherización de la Cocina",
    kashDesc: "Preparando el entorno físico.",
    ovens: "Hornos",
    ovensDesc: "No usar 24 horas. Limpiar con químico fuerte. Encender a máxima temperatura por 1 hora o usar función Self-Clean.",
    micro: "Microondas",
    microDesc: "No usar 24 horas. Limpiar bien. Hervir un vaso de agua dentro por 10 minutos hasta que el vapor cubra las paredes.",
    sink: "Bacha / Tarja",
    sinkDesc: "Limpiar y dejar secar 24h. Verter agua hirviendo directamente de una olla al fuego sobre todas las superficies.",
    cutlery: "Cubiertos de Metal",
    cutleryDesc: "Hagalá: Sumergir individualmente en una olla con agua hirviendo a borbotones (previamente kasherizada para Pesaj)."
  },
  eng: {
    title: "Chaguim Guide",
    subtitle: "Active Preparation",
    next: "Next Holiday",
    daysLeft: "Remaining",
    days: "days",
    heroDesc: "From April 1 to 9, 2026. It is the festival of freedom, where the consumption and possession of Chametz is prohibited.",
    cleanTitle: "Sale and Cleaning",
    cleanDesc: "Chametz must disappear.",
    clean1: "Thoroughly clean the whole house, drawers, kitchen and car before April 1.",
    clean2: "Sell the remaining Chametz through your local Rabbi.",
    clean3: "Perform Bedikat Chametz (Search) the night before with a candle and feather.",
    lawsTitleAshk: "Laws of Ashkenazim",
    lawsTitleSef: "Laws of Sephardim",
    lawsDesc: "Rules based on your current custom.",
    laws1Ashk: "Absolute prohibition of Kitniyot. Rice, corn, beans, lentils or derivatives like corn syrup are not allowed.",
    laws1Sef: "Consumption of Kitniyot (rice, beans, etc.) is allowed if meticulously checked according to family tradition.",
    laws2Ashk: 'Kosher L\'Pesach products that say "L\'Ochlei Kitniyot" are NOT suitable for you.',
    laws2Sef: 'You can consume products marked as Kosher L\'Pesach "L\'Ochlei Kitniyot".',
    kashTitle: "Kitchen Koshering",
    kashDesc: "Preparing the physical environment.",
    ovens: "Ovens",
    ovensDesc: "Do not use for 24 hours. Clean with strong chemical. Turn on at max temperature for 1 hour or use Self-Clean function.",
    micro: "Microwave",
    microDesc: "Do not use for 24 hours. Clean well. Boil a glass of water inside for 10 minutes until the steam covers the walls.",
    sink: "Sink",
    sinkDesc: "Clean and let dry 24h. Pour boiling water directly from a pot on the fire over all surfaces.",
    cutlery: "Metal Cutlery",
    cutleryDesc: "Hagalah: Submerge individually in a pot with boiling bubbling water (previously koshered for Pesach)."
  }
};

export default function ChaguimPage() {
  const { lang } = useLanguage();
  const t = TEXTS[lang as keyof typeof TEXTS] || TEXTS['esp'];

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
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">{t.title}</h1>
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
              <Calendar className="w-4 h-4"/> {t.next}
            </h2>
            <h3 className="text-5xl font-black text-white mb-4 drop-shadow-md">Pesaj 2026</h3>
            
            <div className="bg-slate-950/50 py-3 px-8 rounded-full border border-slate-700/50 mb-4 inline-block shadow-inner">
              <span className="text-slate-300 font-medium text-lg">{t.daysLeft} <span className="text-emerald-400 font-black text-2xl mx-1">{daysLeft}</span> {t.days}</span>
            </div>
            <p className="text-slate-400 text-sm max-w-md mx-auto">
              {t.heroDesc}
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
                <h3 className="text-white font-bold text-lg">{t.cleanTitle}</h3>
                <p className="text-slate-400 text-sm mt-1">{t.cleanDesc}</p>
              </div>
            </div>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>{t.clean1}</span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>{t.clean2}</span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>{t.clean3}</span>
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
                <p className="text-slate-400 text-sm mt-1">{t.lawsDesc}</p>
              </div>
            </div>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>
                  {userOrigin === 'ashkenazi' 
                    ? t.laws1Ashk 
                    : t.laws1Sef}
                </span>
              </li>
              <li className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <span>
                  {userOrigin === 'ashkenazi'
                    ? t.laws2Ashk
                    : t.laws2Sef}
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
                <h3 className="text-white font-bold text-lg">{t.kashTitle}</h3>
                <p className="text-slate-400 text-sm mt-1">{t.kashDesc}</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">{t.ovens}</strong>
                <p className="text-xs text-slate-300">{t.ovensDesc}</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">{t.micro}</strong>
                <p className="text-xs text-slate-300">{t.microDesc}</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">{t.sink}</strong>
                <p className="text-xs text-slate-300">{t.sinkDesc}</p>
              </div>
              <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <strong className="text-emerald-400 block mb-1">{t.cutlery}</strong>
                <p className="text-xs text-slate-300">{t.cutleryDesc}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

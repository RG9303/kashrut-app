'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Gift, Wine, CloudRain, Apple, Flame, Tent, CalendarDays } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';

const TEXTS = {
  esp: {
    title: "Calendario Hebreo",
    subtitle: "Ciclo Anual 2026 • 5786/5787",
    heroTitle: "Cronograma Kashrut",
    heroDesc: "Cada festividad judía trae consigo leyes culinarias únicas y atmósferas especiales. Desplázate por el calendario para planificar estratégicamente tus próximos Chaguim y evitar contratiempos dietéticos.",
    advisor: "Kashrut Advisor",
    purimDesc: "Fiesta de la alegría, disfraces y la lectura de la Meguilá.",
    purimTip: 'Asegúrate de que todos los dulces, vinos y alimentos incluidos en tus "Mishloaj Manot" (regalos de comida) tengan certificación Kosher y sellos verificables para que quien lo reciba pueda disfrutarlos con absoluta confianza.',
    pesajDesc: 'La liberación de Egipto. Prohibición absoluta de consumir o poseer Jametz (leudados).',
    pesajTip: 'Se requiere una limpieza milimétrica del hogar. Todo alimento empacado durante estos 8 días requiere explícitamente el sello "Kosher L\'Pesach". Ashknenazím evitan comer Kitniyot (arroz, maíz, legumbres).',
    pesajLink: 'Ver Mega-Guía de Pesaj',
    shavuotDesc: 'Celebra la entrega sublime de la Torá en el Monte Sinaí.',
    shavuotTip: 'Es tradición consumir majestuosos banquetes lácteos (Cheesecakes, pastas). Presta especial atención al sello de "Jalav Israel" (leche supervisada) y no olvides esperar el tiempo reglamentario tras comer carne antes de consumir los lácteos festivos.',
    roshDesc: 'El Año Nuevo Judío. Días del juicio y la coronación divina.',
    roshTip: 'Comemos Simanim (señales místicas de buen augurio) como manzana con miel, granada y cabeza de pescado. Asegura que la miel sea 100% pura abeja y revisa intensamente la granada, poro y espinacas en búsqueda de insectos.',
    kipurDesc: 'El sagrado Día del Perdón. Dedicado completamente al rezo espiritual.',
    kipurTip: 'Ayuno profundo y absoluto de 25 horas. No hay preparación de alimentos para este Chag, pero tu cena previa de "Seuda Mafseket" debe ser ligera, cocinada con rigor Kosher y sin alimentos demasiado salados.',
    sukotDesc: 'La festividad de las Cabañas, recordando los 40 años en el desierto.',
    sukotTip: 'Cualquier comida establecida (pan, jalá, mezonot fuertes) debe ser consumida exclusivamente dentro de la estructura rabínicamente legal de la Sucá. Reúne las 4 Especies (Lulav y Etrog) con sellos de supervisión agraria validada.',
    janucaDesc: 'El milagro de las luces y el rescate del Sagrado Templo.',
    janucaTip: 'Costumbre de consumir alimentos fritos brillantes en aceite, como Latkes y Sufganiyot (donas). Compra aceite Kosher de alta calidad y revisa muy bien los lácteos de los postres fritos cruzando las listas internacionales Kashrut.'
  },
  eng: {
    title: "Hebrew Calendar",
    subtitle: "Annual Cycle 2026 • 5786/5787",
    heroTitle: "Kashrut Timeline",
    heroDesc: "Each Jewish holiday brings unique culinary laws and special atmospheres. Scroll through the calendar to strategically plan your upcoming Chaguim and avoid dietary setbacks.",
    advisor: "Kashrut Advisor",
    purimDesc: "Festival of joy, costumes, and the reading of the Megillah.",
    purimTip: 'Ensure that all sweets, wines, and foods included in your "Mishloach Manot" (food gifts) have Kosher certification and verifiable seals so the recipient can enjoy them with absolute confidence.',
    pesajDesc: 'The liberation from Egypt. Absolute prohibition of consuming or possessing Chametz (leavened bread).',
    pesajTip: 'Meticulous home cleaning is required. All packaged food during these 8 days explicitly requires the "Kosher L\'Pesach" seal. Ashkenazim avoid eating Kitniyot (rice, corn, legumes).',
    pesajLink: 'View Pesach Mega-Guide',
    shavuotDesc: 'Celebrates the sublime giving of the Torah at Mount Sinai.',
    shavuotTip: 'It is a tradition to consume majestic dairy banquets (Cheesecakes, pastas). Pay special attention to the "Cholov Yisroel" (supervised milk) seal and do not forget to wait the required time after eating meat before consuming festive dairy.',
    roshDesc: 'The Jewish New Year. Days of judgment and divine coronation.',
    roshTip: 'We eat Simanim (mystical signs of good omen) such as apple with honey, pomegranate, and fish head. Ensure the honey is 100% pure bee and intensely check the pomegranate, leek, and spinach for insects.',
    kipurDesc: 'The holy Day of Atonement. Completely dedicated to spiritual prayer.',
    kipurTip: 'Deep and absolute fast of 25 hours. There is no food preparation for this Chag, but your previous "Seudah Mafseket" dinner should be light, cooked with Kosher rigor and without excessively salty foods.',
    sukotDesc: 'The Festival of Booths, remembering the 40 years in the desert.',
    sukotTip: 'Any established meal (bread, challah, strong mezonot) must be consumed exclusively within the rabbinically legal structure of the Sukkah. Gather the 4 Species (Lulav and Etrog) with validated agricultural supervision seals.',
    janucaDesc: 'The miracle of lights and the rescue of the Holy Temple.',
    janucaTip: 'Custom of consuming bright foods fried in oil, such as Latkes and Sufganiyot (donuts). Buy high-quality Kosher oil and check the dairy of fried desserts very well by cross-referencing international Kashrut lists.'
  }
};

export default function CalendarioPage() {
  const { lang } = useLanguage();
  const t = TEXTS[lang as keyof typeof TEXTS] || TEXTS['esp'];


  const timeline = [
    {
      id: 'purim',
      name: 'Purim',
      hebrewDate: '14 Adar 5786',
      civilDate: 'Marzo 3, 2026',
      icon: <Gift className="w-6 h-6 text-fuchsia-400" />,
      color: 'bg-fuchsia-500',
      description: t.purimDesc,
      kashrutTip: t.purimTip,
      linkText: null,
      linkHref: null
    },
    {
      id: 'pesaj',
      name: 'Pesaj',
      hebrewDate: '15 Nisan 5786',
      civilDate: 'Abril 1 - Abril 9, 2026',
      icon: <Wine className="w-6 h-6 text-emerald-400" />,
      color: 'bg-emerald-500',
      description: t.pesajDesc,
      kashrutTip: t.pesajTip,
      linkText: t.pesajLink,
      linkHref: '/chaguim'
    },
    {
      id: 'shavuot',
      name: 'Shavuot',
      hebrewDate: '6 Sivan 5786',
      civilDate: 'Mayo 22, 2026',
      icon: <CloudRain className="w-6 h-6 text-sky-400" />,
      color: 'bg-sky-500',
      description: t.shavuotDesc,
      kashrutTip: t.shavuotTip,
      linkText: null,
      linkHref: null
    },
    {
      id: 'rosh-hashana',
      name: 'Rosh Hashaná',
      hebrewDate: '1 Tishrei 5787',
      civilDate: 'Septiembre 11 - 13, 2026',
      icon: <Apple className="w-6 h-6 text-rose-400" />,
      color: 'bg-rose-500',
      description: t.roshDesc,
      kashrutTip: t.roshTip,
      linkText: null,
      linkHref: null
    },
    {
      id: 'yom-kipur',
      name: 'Yom Kipur',
      hebrewDate: '10 Tishrei 5787',
      civilDate: 'Septiembre 20, 2026',
      icon: <Flame className="w-6 h-6 text-amber-400" />,
      color: 'bg-amber-500',
      description: t.kipurDesc,
      kashrutTip: t.kipurTip,
      linkText: null,
      linkHref: null
    },
    {
      id: 'sukot',
      name: 'Sukot',
      hebrewDate: '15 Tishrei 5787',
      civilDate: 'Septiembre 25 - Oct 2, 2026',
      icon: <Tent className="w-6 h-6 text-emerald-400" />,
      color: 'bg-emerald-600',
      description: t.sukotDesc,
      kashrutTip: t.sukotTip,
      linkText: null,
      linkHref: null
    },
    {
      id: 'januca',
      name: 'Janucá',
      hebrewDate: '25 Kislev 5787',
      civilDate: 'Diciembre 4 - 12, 2026',
      icon: <Flame className="w-6 h-6 text-orange-400" />,
      color: 'bg-orange-500',
      description: t.janucaDesc,
      kashrutTip: t.janucaTip,
      linkText: null,
      linkHref: null
    }
  ];

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
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">{t.title}</h1>
              <p className="text-slate-400 font-medium text-sm">{t.subtitle}</p>
            </div>
          </div>
        </div>

        {/* Hero Banner */}
        <div className="bg-slate-800/50 p-6 md:p-8 rounded-[2.5rem] shadow-xl border border-slate-700/50 backdrop-blur-xl mb-12 relative overflow-hidden">
           <div className="absolute -right-10 -bottom-10 opacity-5 pointer-events-none">
             <CalendarDays className="w-64 h-64" />
           </div>
           <div className="relative z-10">
             <div className="w-16 h-16 rounded-3xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-6 border border-emerald-500/20 shadow-inner">
               <CalendarDays className="w-8 h-8" />
             </div>
             <h2 className="text-3xl font-bold text-white mb-2">{t.heroTitle}</h2>
             <p className="text-slate-400 text-lg max-w-2xl leading-relaxed">
               {t.heroDesc}
             </p>
           </div>
        </div>

        {/* Timeline Sequence */}
        <div className="relative pl-6 md:pl-0">
          {/* Vertical central line (desktop) / left line (mobile) */}
          <div className="absolute left-[36px] md:left-1/2 md:-ml-[2px] top-0 bottom-0 w-[4px] bg-slate-800/80 rounded-full"></div>

          <div className="space-y-12 md:space-y-0 relative">
            {timeline.map((chag, idx) => {
              const isEven = idx % 2 === 0;

              return (
                <div key={chag.id} className={`relative flex flex-col md:flex-row items-center md:justify-center group ${isEven ? 'md:flex-row-reverse' : ''}`}>
                  
                  {/* Timeline Node Ring */}
                  {/* Mobile pos is absolutely positioned to line up with the left line. Desktop uses flex gap spacing. */}
                  <div className={`absolute md:static left-0 md:bg-slate-900 border-4 border-slate-900 z-10 w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-transform duration-500 group-hover:scale-110 md:mx-4 bg-slate-800`}>
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center bg-slate-800/50 border border-slate-600/50 shadow-inner group-hover:bg-slate-700/80 transition-colors`}>
                      {chag.icon}
                    </div>
                  </div>

                  {/* Card Module */}
                  <div className={`ml-20 md:ml-0 md:w-1/2 ${isEven ? 'md:pr-12' : 'md:pl-12'} w-full`}>
                    <div className="bg-slate-800/40 p-6 rounded-3xl shadow-xl border border-slate-700/40 backdrop-blur-xl hover:border-emerald-500/40 transition-colors duration-500 relative overflow-hidden">
                      {/* Top colored gradient aura */}
                      <div className={`absolute top-0 left-0 right-0 h-1.5 ${chag.color}`}></div>
                      
                      <div className="flex justify-between items-start mb-4 gap-2">
                        <div>
                          <h3 className="text-2xl font-black text-white leading-none mb-1">{chag.name}</h3>
                          <span className="text-sm font-bold text-emerald-400 capitalize bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 inline-block mt-2">{chag.hebrewDate}</span>
                        </div>
                        <span className="text-sm text-slate-400 font-mono text-right shrink-0 bg-slate-900/50 px-3 py-1.5 rounded-xl border border-slate-800">{chag.civilDate}</span>
                      </div>

                      <p className="text-slate-300 mb-6 leading-relaxed">
                        {chag.description}
                      </p>

                      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-700/50 relative">
                        <span className="absolute -top-3 left-4 bg-slate-900 px-2 text-[10px] font-black tracking-widest uppercase text-slate-400 border border-slate-700/50 rounded-full">
                          {t.advisor}
                        </span>
                        <p className="text-emerald-100/80 text-sm leading-relaxed font-medium">
                          {chag.kashrutTip}
                        </p>
                      </div>

                      {chag.linkHref && chag.linkText && (
                        <Link href={chag.linkHref} className="mt-5 w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 rounded-xl flex items-center justify-center transition-all shadow-[0_4px_15px_rgba(16,185,129,0.15)] hover:shadow-emerald-500/30">
                           {chag.linkText}
                        </Link>
                      )}
                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}

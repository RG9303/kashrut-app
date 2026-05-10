with open("src/app/logos/page.tsx", "w") as f:
    f.write("""'use client';

import React, { useState } from 'react';
import { useLanguage } from '@/hooks/useLanguage';
import Link from 'next/link';
import { ArrowLeft, Globe, MapPin, Search, XCircle, Info, BookOpen, ShieldCheck, Tag, ExternalLink, Lightbulb } from 'lucide-react';

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
    examples: string[];
    notes: string;
    officialWebsite: string | null;
  };
}

export default function LogosPage() {
  const { lang } = useLanguage();
  const isEng = lang === 'eng';
  
  const TEXTS = {
    esp: {
      global: "Globales",
      israel: "Israelíes",
      local: "Locales",
      title: "Catálogo Enciclopédico",
      subtitle: "Diccionario Kashrut Global",
      searchPlaceholder: "Busca cualquier certificado...",
      searchHint: "Escribe cualquier letra (ej. OU, cRc) para abrir instantáneamente la enciclopedia oculta del sello.",
      results: "Resultados Enciclopédicos",
      studyDetails: "Estudiar Detalle",
      notFound: "No encontrado en Enciclopedia",
      notFoundDesc: "No tenemos este sello pre-programado. Utiliza la cámara principal en la pantalla de \\"Inicio\\" para que la Inteligencia Artificial analice visualmente el sello desconocido que tienes en tus manos.",
      backToScanner: "Volver al Escáner IA",
      globalSeals: "Sellos Globales",
      israelAgencies: "Agencias en Israel",
      localLatam: "Locales (Latinoamérica)",
      clickForEncyclopedia: "Clic para Enciclopedia",
      historyOfAgency: "Historia de la Agencia",
      halachicLevel: "Nivel Halájico (Strictness)",
      rabbinicAuth: "Autoridad Rabínica",
      mainRegion: "Región Principal",
      closeEncyclopedia: "Cerrar Enciclopedia",
      examplesTitle: "Ejemplos de Productos",
      notesTitle: "Nota Importante",
      visitWebsite: "Visitar Sitio Oficial",
      noWebsite: "Sin Sitio Oficial"
    },
    eng: {
      global: "Global",
      israel: "Israeli",
      local: "Local",
      title: "Encyclopedic Catalog",
      subtitle: "Global Kashrut Dictionary",
      searchPlaceholder: "Search any certificate...",
      searchHint: "Type any letter (e.g. OU, cRc) to instantly open the hidden encyclopedia of the seal.",
      results: "Encyclopedic Results",
      studyDetails: "Study Detail",
      notFound: "Not Found in Encyclopedia",
      notFoundDesc: "We do not have this seal pre-programmed. Use the main camera on the \\"Home\\" screen for Artificial Intelligence to visually analyze the unknown seal you have in your hands.",
      backToScanner: "Back to AI Scanner",
      globalSeals: "Global Seals",
      israelAgencies: "Agencies in Israel",
      localLatam: "Local (Latin America)",
      clickForEncyclopedia: "Click for Encyclopedia",
      historyOfAgency: "Agency History",
      halachicLevel: "Halachic Level (Strictness)",
      rabbinicAuth: "Rabbinic Authority",
      mainRegion: "Main Region",
      closeEncyclopedia: "Close Encyclopedia",
      examplesTitle: "Product Examples",
      notesTitle: "Important Note",
      visitWebsite: "Visit Official Website",
      noWebsite: "No Official Website"
    }
  };
  
  const t = TEXTS[isEng ? 'eng' : 'esp'];

  const logos: LogoInfo[] = [
    {
      id: 1,
      category: isEng ? 'Global' : 'Globales',
      name: 'Orthodox Union (OU)',
      description: isEng ? 'The largest and most widely recognized certifying agency globally. Certifies over 65% of the global kosher market.' : 'La agencia certificadora más grande y reconocida a nivel mundial. Certifica más del 65% del mercado kosher global.',
      color: 'from-blue-600 to-indigo-900',
      symbol: (
        <div className="relative w-16 h-16 border-[4px] border-white rounded-full flex items-center justify-center font-black text-white text-3xl shadow-lg">
          U
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Founded in 1898, the Orthodox Union introduced modern corporate supervision, creating the concept of the industrial Mashgiach.' : 'Fundada en 1898, la Unión Ortodoxa introdujo la supervisión moderna corporativa, creando el concepto del Mashguíaj industrial.',
         rabbi: 'Rabbi Menachem Genack',
         strictness: isEng ? 'Highly Reliable (Global Gold Standard).' : 'Altamente Confiable (Estándar de Oro Global).',
         regions: isEng ? 'United States, Europe, Israel and over 100 countries.' : 'Estados Unidos, Europa, Israel y más de 100 países.',
         examples: ['Oreo', 'Coca-Cola', 'Heinz Ketchup', 'M&Ms', 'Pringles'],
         notes: isEng ? 'When you see an OU-D, it means it contains dairy. OU-Pareve means it has no meat or dairy.' : 'Cuando veas un OU-D, significa que contiene lácteos. OU-Pareve significa que no tiene carne ni lácteos.',
         officialWebsite: 'https://oukosher.org'
      }
    },
    {
      id: 2,
      category: isEng ? 'Global' : 'Globales',
      name: 'OK Kosher',
      description: isEng ? 'Headquartered in Brooklyn, it is the second-largest international agency.' : 'Con sede central en Brooklyn, es la segunda agencia internacional con mayor cantidad de productos certificados.',
      color: 'from-emerald-500 to-teal-800',
      symbol: (
        <div className="relative border-[4px] border-white w-14 h-16 rounded-[40%] flex items-center justify-center font-black text-white text-3xl shadow-lg">
          K
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Started in 1935 by Rabbi Berel Levy, it pioneered the computerization of industrial ingredient data globally.' : 'Iniciada en 1935 por el Rabino Berel Levy, fue pionera en informatizar los datos de ingredientes industriales a nivel mundial.',
         rabbi: 'Rabbi Chaim Fogelman',
         strictness: isEng ? 'Mehadrin. Usually strict on Cholov Yisroel and Pas Yisroel.' : 'Mehadrin. Suelen exigir lineamientos "Cholov Yisroel" y "Pas Yisroel" en lácteos y panadería.',
         regions: isEng ? 'North America, Asia, Eastern Europe.' : 'Norteamérica, Asia y Países del Este.',
         examples: ['Snapple', 'Post Cereals', 'Tropicana', 'Breyers'],
         notes: isEng ? 'The OK symbol is one of the most counterfeited in the world. Always verify on their official site.' : 'El símbolo OK es uno de los más falsificados del mundo. Siempre verifica en su sitio oficial.',
         officialWebsite: 'https://www.ok.org'
      }
    },
    {
      id: 3,
      category: isEng ? 'Global' : 'Globales',
      name: 'Star-K',
      description: isEng ? 'Leader in technology and halacha (Baltimore). Main authority in certifying appliances.' : 'Líder en tecnología y halajá (Baltimore). Son la autoridad principal en la certificación de software y electrodomésticos.',
      color: 'from-amber-500 to-orange-800',
      symbol: (
        <div className="relative w-20 h-20 flex items-center justify-center scale-90">
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-b-[50px] border-b-white opacity-80 mt-[-15px]"></div>
          <div className="absolute w-0 h-0 border-l-[30px] border-l-transparent border-r-[30px] border-r-transparent border-t-[50px] border-t-white opacity-80 mt-[15px]"></div>
          <span className="font-black text-amber-800 z-10 text-2xl">K</span>
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Started as a local Baltimore council and grew by dictating worldwide regulations on Sabbath Mode appliances.' : 'Empezó como un consejo local de Baltimore y creció dictando regulaciones mundiales sobre el uso sabático ("Sabbath Mode").',
         rabbi: 'Rabbi Moshe Heinemann',
         strictness: isEng ? 'Top level. Strict Glatt Kosher standards.' : 'Nivel superior. Estrictos estándares Glatt Kosher.',
         regions: isEng ? 'North America, Eastern Europe, China, India.' : 'Norteamérica, Europa del Este, China e India.',
         examples: ['Samsung Appliances', 'GE Appliances', 'Sabra Hummus'],
         notes: isEng ? 'Look for the "Sabbath Mode" certification on modern refrigerators and ovens.' : 'Busca su certificación "Sabbath Mode" en refrigeradores y hornos modernos.',
         officialWebsite: 'https://www.star-k.org'
      }
    },
    {
      id: 8,
      category: isEng ? 'Global' : 'Globales',
      name: 'Kof-K (Kosher Supervision)',
      description: isEng ? 'Pioneering agency based in New Jersey. Highly popular in American food items.' : 'Agencia pionera ubicada en New Jersey. Destaca por el uso de tecnologías de rastreo y es sumamente popular en alimentos estadounidenses.',
      color: 'from-red-500 to-pink-800',
      symbol: (
        <div className="relative w-16 h-16 flex items-center justify-center font-black text-white text-[40px] shadow-lg">
          <span className="absolute text-5xl opacity-40">כ</span>
          <span className="z-10">K</span>
        </div>
      ),
      fullDetails: {
         history: isEng ? 'KOF-K was the first Kashrut agency to use a global computer system to monitor millions of ingredients.' : 'KOF-K fue la primera agencia Kashrut en utilizar un sistema informático global para monitorear millones de ingredientes.',
         rabbi: 'Rabbi Aharon Yehuda Dr. Zecharia Senter (Z"L)',
         strictness: isEng ? 'Excellent Orthodox Reliability.' : 'Confiabilidad Ortodoxa Excelente.',
         regions: isEng ? 'North America, Israel, Asia Continental.' : 'América del Norte, Israel, Asia Continental.',
         examples: ['Ben & Jerry\\'s', 'Baskin-Robbins', 'Quaker Oats'],
         notes: isEng ? 'Widely used in the flavor industry (flavorings and extracts).' : 'Muy utilizado en la industria de saborizantes y extractos aromáticos.',
         officialWebsite: 'https://www.kof-k.org'
      }
    },
    {
      id: 9,
      category: isEng ? 'Global' : 'Globales',
      name: 'cRc (Chicago Rabbinical Council)',
      description: isEng ? 'One of the largest regional agencies, famous for its beverage and fish recommendations lists.' : 'Una de las agencias regionales más gigantes y respetadas, famosa por sus listas de bebidas y recomendaciones de pescados.',
      color: 'from-slate-700 to-slate-900',
      symbol: (
        <div className="relative w-20 h-16 flex flex-col items-center justify-center">
            <div className="w-0 h-0 border-l-[35px] border-l-transparent border-r-[35px] border-r-transparent border-b-[55px] border-b-white absolute"></div>
            <span className="z-10 font-bold text-slate-800 text-sm mt-3 tracking-widest">cRc</span>
        </div>
      ),
      fullDetails: {
         history: isEng ? 'The cRc operates as a non-profit in the Midwest. Its documents, apps, and liquor lists are consulted worldwide.' : 'El cRc opera como una entidad sin fines de lucro en el Medio Oeste. Sus documentos, apps y listas de licores son consultados mundialmente.',
         rabbi: 'Rabbi Sholem Fishbane',
         strictness: isEng ? 'Rigorous Orthodox, widely recommended.' : 'Ortodoxa Rigurosa, recomendada extensamente.',
         regions: isEng ? 'Central North America and International.' : 'Norteamérica central e internacional.',
         examples: ['Gatorade', 'Jim Beam', 'Slurpee (7-Eleven)'],
         notes: isEng ? 'Their liquor list is the gold standard for global consumers.' : 'Su lista de licores es el estándar de oro para los consumidores globales.',
         officialWebsite: 'https://www.crcweb.org'
      }
    },
    {
      id: 4,
      category: isEng ? 'Israeli' : 'Israelíes',
      name: 'Badatz Edah HaChareidis',
      description: isEng ? 'Considered one of the most rigorous (Mehadrin) standards in Jerusalem. Highly reliable worldwide.' : 'Considerado uno de los estándares más rigurosos (Mehadrin) de Jerusalén. Altamente confiable mundialmente.',
      color: 'from-red-600 to-rose-900',
      symbol: (
        <div className="font-bold text-white text-2xl tracking-widest bg-red-950/40 px-3 py-2 rounded-xl border border-white/20">
          בָדָ״ץ
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Formed before the creation of the State of Israel, governs the most ultra-orthodox communities of Jerusalem.' : 'Formado antes de la creación del Estado de Israel, rige sobre las comunidades más ultraortodoxas de Jerusalén.',
         rabbi: 'Rabbinical Court of the Edah HaChareidis',
         strictness: isEng ? 'Maximum rigor (Chumra). Universally accepted without question (Glatt / Mehadrin).' : 'Máximo rigor (Chumra). Aceptada universalmente sin cuestionamientos (Glatt / Mehadrin).',
         regions: isEng ? 'Jerusalem, Bet Shemesh, and premium Israeli imports.' : 'Jerusalén, Bet Shemesh, e importaciones premium israelíes.',
         examples: ['Osem (some)', 'Bamba (premium)', 'Elite Chocolate'],
         notes: isEng ? 'Products with this seal are often significantly more expensive due to the extreme supervision process.' : 'Los productos con este sello suelen ser significativamente más caros por el extremo proceso de supervisión.',
         officialWebsite: null
      }
    },
    {
      id: 5,
      category: isEng ? 'Israeli' : 'Israelíes',
      name: 'Chief Rabbinate of Israel',
      description: isEng ? 'Rabbanut. Base state seal required for any legal sale of a Kosher product in Israel.' : 'Rabbanut. Sello estatal base requerido para cualquier producción, importación o venta legal de un producto Kosher dentro del Estado de Israel.',
      color: 'from-sky-500 to-blue-800',
      symbol: (
        <div className="w-16 h-14 bg-white rounded-md flex flex-col items-center justify-center text-sky-800 font-bold shadow-lg border-2 border-white/80">
          <span className="text-[10px] uppercase">Kosher</span>
          <span className="text-xl leading-none">כשר</span>
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Created by the State of Israel, acts as the national base law of Kashrut.' : 'Creado por el Estado de Israel, funciona como la ley base nacional de Kashrut.',
         rabbi: 'Chief Rabbinate (Rishon LeZion & Ashkenazi Chief Rabbi)',
         strictness: isEng ? 'Basic (Regular) sometimes relies on Heter Mechira. Mehadrin is more rigorous.' : 'Básico (Regular) a veces depende de permisos (Heter Mejira). El Mehadrin es más riguroso.',
         regions: isEng ? 'National (Entire State of Israel).' : 'Nacional (Todo el territorio del Estado de Israel).',
         examples: ['Tnuva Dairy', 'Strauss Group', 'Carmel Winery'],
         notes: isEng ? 'Look for the "Mehadrin" text within the shield if you hold by stricter standards.' : 'Busca el texto "Mehadrin" dentro del escudo si sigues estándares más estrictos.',
         officialWebsite: 'https://www.gov.il/he/departments/chief_rabbinate_of_israel'
      }
    },
    {
      id: 6,
      category: isEng ? 'Local' : 'Locales',
      name: 'KMD (Maguen David México)',
      description: isEng ? 'The main certifying authority of the Jewish-Mexican community in Mexico City.' : 'La principal autoridad certificadora de la comunidad Judeo-Mexicana en Ciudad de México. Manejan directrices estrictas.',
      color: 'from-slate-600 to-slate-900',
      symbol: (
        <div className="flex border-4 border-white h-12 items-center px-2 bg-blue-600 font-black text-white text-xl tracking-tighter">
          KMD
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Pillar of the Kosher resurgence in Mexico, the KMD is the most prolific local seal.' : 'Pilar del resurgimiento Kosher en México, el KMD es el sello local más prolífico.',
         rabbi: 'Rabbinical Committee of the Maguen David Community',
         strictness: isEng ? 'Strict Orthodox and rigorous local Chalav Yisroel policy.' : 'Ortodoxo Estricto y rigurosa política de Jalav Israel y Bishul Yisroel local.',
         regions: isEng ? 'Mexico City, Cancun, Central America.' : 'Ciudad de México, Cancún, Centroamérica.',
         examples: ['Bimbo (some breads)', 'Jumex', 'San Rafael (Kosher lines)'],
         notes: isEng ? 'They offer an excellent mobile app for scanning products within Mexico.' : 'Ofrecen una excelente aplicación móvil para escanear productos dentro de México.',
         officialWebsite: 'https://kmdmexico.com'
      }
    },
    {
      id: 7,
      category: isEng ? 'Local' : 'Locales',
      name: 'One Kosher',
      description: isEng ? 'International certifier based in Mexico expanding its reach certifying industrialized foods for all Latam.' : 'Certificadora internacional basada en México que expande su alcance y popularidad certificando alimentos industrializados para toda Latinoamérica.',
      color: 'from-purple-600 to-fuchsia-900',
      symbol: (
        <div className="flex items-center gap-1 font-black text-white text-2xl">
          <span className="bg-white text-purple-800 px-2 py-1 rounded">1</span>
          <span>K</span>
        </div>
      ),
      fullDetails: {
         history: isEng ? 'Founded as a dynamic and corporate solution in Mexico to digitize Latam Kashrut libraries.' : 'Fundada como una solución dinámica y corporativa en México para digitalizar bibliotecas de Kashrut en Latam.',
         rabbi: 'Rabbi Nissim L. Michan',
         strictness: isEng ? 'Rigorous International Standard.' : 'Riguroso Estándar Internacional.',
         regions: isEng ? 'Mexico, South America, Caribbean, USA.' : 'México, Sudamérica, el Caribe, USA (importaciones hispanas).',
         examples: ['Barcel', 'Sabritas', 'Nestle Latam'],
         notes: isEng ? 'Highly prominent in Mexican snacks and exported Latin candies.' : 'Altamente prominente en botanas mexicanas y dulces latinos de exportación.',
         officialWebsite: 'https://onekosher.org'
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
      
      {selectedLogo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 animate-in fade-in duration-300">
           <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={() => setSelectedLogo(null)}></div>
           
           <div className="relative bg-slate-900 w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-[2.5rem] shadow-2xl border border-slate-700">
              <div className={`h-40 w-full flex items-center justify-center relative overflow-hidden bg-gradient-to-br ${selectedLogo.color}`}>
                 <button onClick={() => setSelectedLogo(null)} className="absolute top-4 right-4 text-white/50 hover:text-white transition-colors bg-black/20 p-1.5 rounded-full z-20">
                   <XCircle className="w-8 h-8" />
                 </button>
                 <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                 <div className="relative z-10 scale-125 drop-shadow-2xl">{selectedLogo.symbol}</div>
              </div>

              <div className="p-8">
                 <div className="flex items-center gap-3 mb-2">
                   <span className="text-[10px] bg-emerald-500/20 text-emerald-400 font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-emerald-500/20">{selectedLogo.category}</span>
                 </div>
                 <h2 className="text-3xl font-black text-white mb-6 tracking-tight">{selectedLogo.name}</h2>
                 
                 <div className="space-y-6">
                   <div className="bg-slate-800/50 p-5 rounded-2xl border border-slate-700/50">
                     <h4 className="flex items-center gap-2 text-emerald-400 font-bold text-sm mb-2 uppercase tracking-wide">
                        <BookOpen className="w-4 h-4" /> {t.historyOfAgency}
                     </h4>
                     <p className="text-slate-300 text-sm leading-relaxed">{selectedLogo.fullDetails.history}</p>
                   </div>

                   <div className="bg-slate-800/50 p-5 rounded-2xl border border-slate-700/50">
                     <h4 className="flex items-center gap-2 text-blue-400 font-bold text-sm mb-2 uppercase tracking-wide">
                        <ShieldCheck className="w-4 h-4" /> {t.halachicLevel}
                     </h4>
                     <p className="text-slate-300 text-sm leading-relaxed">{selectedLogo.fullDetails.strictness}</p>
                   </div>

                   <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                     <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-700/30">
                       <span className="block text-slate-500 text-xs font-bold uppercase mb-1">{t.rabbinicAuth}</span>
                       <span className="text-slate-200 text-sm">{selectedLogo.fullDetails.rabbi}</span>
                     </div>
                     <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-700/30">
                       <span className="block text-slate-500 text-xs font-bold uppercase mb-1">{t.mainRegion}</span>
                       <span className="text-slate-200 text-sm">{selectedLogo.fullDetails.regions}</span>
                     </div>
                   </div>

                   {/* NEW INTERACTIVE FIELDS */}
                   <div className="bg-slate-800/50 p-5 rounded-2xl border border-slate-700/50">
                     <h4 className="flex items-center gap-2 text-fuchsia-400 font-bold text-sm mb-3 uppercase tracking-wide">
                        <Tag className="w-4 h-4" /> {t.examplesTitle}
                     </h4>
                     <div className="flex flex-wrap gap-2">
                        {selectedLogo.fullDetails.examples.map((example, idx) => (
                           <span key={idx} className="bg-slate-900 border border-slate-600 text-slate-300 px-3 py-1 rounded-full text-xs font-medium">
                             {example}
                           </span>
                        ))}
                     </div>
                   </div>

                   <div className="bg-amber-900/20 p-5 rounded-2xl border border-amber-700/30">
                     <h4 className="flex items-center gap-2 text-amber-500 font-bold text-sm mb-2 uppercase tracking-wide">
                        <Lightbulb className="w-4 h-4" /> {t.notesTitle}
                     </h4>
                     <p className="text-slate-300 text-sm leading-relaxed">{selectedLogo.fullDetails.notes}</p>
                   </div>

                   <div className="flex flex-col gap-3 pt-2">
                     {selectedLogo.fullDetails.officialWebsite ? (
                       <a href={selectedLogo.fullDetails.officialWebsite} target="_blank" rel="noopener noreferrer" className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 flex justify-center items-center gap-2 text-white font-bold rounded-2xl transition-all shadow-[0_4px_15px_rgba(16,185,129,0.2)]">
                         <Globe className="w-5 h-5" /> {t.visitWebsite} <ExternalLink className="w-4 h-4 ml-1 opacity-70"/>
                       </a>
                     ) : (
                       <button disabled className="w-full py-4 bg-slate-800 border border-slate-700 text-slate-500 flex justify-center items-center gap-2 font-bold rounded-2xl cursor-not-allowed">
                         <Globe className="w-5 h-5 opacity-50" /> {t.noWebsite}
                       </button>
                     )}
                   </div>
                 </div>
                 
                 <button onClick={() => setSelectedLogo(null)} className="w-full mt-4 py-4 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white font-bold rounded-2xl transition-all">
                   {t.closeEncyclopedia}
                 </button>
              </div>
           </div>
        </div>
      )}

      <div className="max-w-5xl mx-auto p-4 lg:p-8">
        
        <div className="flex justify-between items-center mb-10 px-2 mt-4 lg:mt-0">
          <div className="flex items-center gap-4">
            <Link href="/" className="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center border border-slate-700 hover:bg-slate-700 transition-colors shadow-lg">
              <ArrowLeft className="text-slate-400 w-6 h-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">{t.title}</h1>
              <p className="text-slate-400 font-medium text-sm flex items-center gap-1">
                {t.subtitle}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-3xl shadow-lg border border-slate-700/50 backdrop-blur-xl mb-10 relative focus-within:border-emerald-500/50 transition-colors">
           <div className="flex items-center gap-4">
             <div className="w-14 h-14 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-black flex-shrink-0">
               <Search className="w-7 h-7" />
             </div>
             <div className="flex-grow">
               <input 
                 type="text"
                 placeholder={t.searchPlaceholder}
                 value={searchTerm}
                 onChange={(e) => setSearchTerm(e.target.value)}
                 className="w-full bg-transparent border-none text-white text-xl md:text-2xl font-bold placeholder-slate-500 focus:outline-none focus:ring-0 p-0"
               />
               <p className="text-slate-400 text-xs md:text-sm mt-1">{t.searchHint}</p>
             </div>
           </div>
        </div>

        {searchTerm ? (
          <div className="mb-10 animate-in fade-in duration-300">
            <h2 className="text-2xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
               {t.results} ({filteredLogos.length})
            </h2>
            {filteredLogos.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredLogos.map(logo => (
                  <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-emerald-500/40 rounded-3xl overflow-hidden hover:border-emerald-400 transition-all shadow-[0_4px_20px_rgba(16,185,129,0.15)] group">
                    <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                       <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                       <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                       <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                         <span className="opacity-0 group-hover:opacity-100 bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-full text-xs transition-opacity transform translate-y-4 group-hover:translate-y-0">{t.studyDetails}</span>
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
                <h3 className="text-xl text-slate-300 font-bold">{t.notFound}</h3>
                <p className="text-slate-500 mt-2 max-w-md mx-auto">{t.notFoundDesc}</p>
                <Link href="/" className="mt-6 inline-block bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white px-6 py-2.5 rounded-xl font-bold transition-colors">{t.backToScanner}</Link>
              </div>
            )}
          </div>
        ) : (
          <>
        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <Globe className="text-blue-400 w-6 h-6" /> {t.globalSeals}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {logos.filter(l => l.category === 'Globales' || l.category === 'Global').map(logo => (
              <div key={logo.id} onClick={() => setSelectedLogo(logo)} className="cursor-pointer bg-slate-800/40 border border-slate-700/40 rounded-3xl overflow-hidden hover:border-slate-500/50 transition-all hover:shadow-xl group relative">
                <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 z-20 transition-opacity bg-black/50 p-1.5 rounded-full backdrop-blur-md">
                   <Info className="w-4 h-4 text-white" />
                </div>
                <div className={`h-32 w-full bg-gradient-to-br ${logo.color} flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-700 ease-out`}>
                   <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                   <div className="relative z-10 drop-shadow-xl">{logo.symbol}</div>
                   <div className="absolute bottom-2 left-3 text-white/40 text-[10px] font-bold uppercase tracking-widest group-hover:opacity-0 transition-opacity">
                     {t.clickForEncyclopedia}
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

        <div className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <MapPin className="text-amber-400 w-6 h-6" /> {t.israelAgencies}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {logos.filter(l => l.category === 'Israelíes' || l.category === 'Israeli').map(logo => (
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

        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
             <MapPin className="text-emerald-400 w-6 h-6" /> {t.localLatam}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {logos.filter(l => l.category === 'Locales' || l.category === 'Local').map(logo => (
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
""")
print("Created comprehensive logos page")

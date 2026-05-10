with open("src/app/chaguim/page.tsx", "w") as f:
    f.write("""'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { ArrowLeft, BookOpen, Clock, CheckCircle2, AlertTriangle, Calendar } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';

function ChaguimContent() {
  const { lang } = useLanguage();
  const searchParams = useSearchParams();
  const jagParam = searchParams.get('jag') || 'pesaj';
  
  const isEng = lang === 'eng';

  const TEXTS_GLOBAL = {
    esp: {
      title: "Guía Chaguim",
      subtitle: "Preparación Activa",
      next: "Festividad",
      daysLeft: "Faltan",
      days: "días",
      lawsTitleAshk: "Leyes de Ashkenazím",
      lawsTitleSef: "Leyes de Sefaradim",
      lawsDesc: "Reglas basadas en tu costumbre actual.",
      kashTitle: "Preparación y Kasherización",
      kashDesc: "Preparando el entorno físico.",
      backBtn: "Volver al Calendario"
    },
    eng: {
      title: "Chaguim Guide",
      subtitle: "Active Preparation",
      next: "Holiday",
      daysLeft: "Remaining",
      days: "days",
      lawsTitleAshk: "Laws of Ashkenazim",
      lawsTitleSef: "Laws of Sephardim",
      lawsDesc: "Rules based on your current custom.",
      kashTitle: "Preparation and Koshering",
      kashDesc: "Preparing the physical environment.",
      backBtn: "Back to Calendar"
    }
  };

  const tGlobal = TEXTS_GLOBAL[isEng ? 'eng' : 'esp'];

  const DATA = {
    'pesaj': {
      date: '2026-04-01T18:00:00',
      name: 'Pesaj',
      esp: {
        heroDesc: "Del 1 al 9 de Abril de 2026. Es la festividad de la libertad, donde se prohíbe el consumo y posesión de Jametz.",
        cleanTitle: "Venta y Limpieza",
        cleanDesc: "El Jametz debe desaparecer.",
        clean1: "Limpiar minuciosamente toda la casa, cajones, cocina y auto antes del 1 de Abril.",
        clean2: "Vender el Jametz sobrante a través de tu Rabino local.",
        clean3: "Realizar Bedikat Jametz (Búsqueda) la noche anterior con vela y pluma.",
        laws1Ashk: "Prohibición absoluta de Kitniyot. No se permite arroz, maíz, frijoles, lentejas ni derivados como jarabe de maíz.",
        laws1Sef: "Permitido el consumo de Kitniyot (arroz, frijoles, etc.) si se revisan meticulosamente según la tradición familiar.",
        laws2Ashk: 'Los productos Kosher L\\'Pesach que dicen "Leojlei Kitniyot" NO son aptos para ti.',
        laws2Sef: 'Puedes consumir productos marcados como Kosher L\\'Pesach "Leojlei Kitniyot".',
        kashItems: [
          { name: "Hornos", desc: "No usar 24 horas. Limpiar con químico fuerte. Encender a máxima temperatura por 1 hora o usar función Self-Clean." },
          { name: "Microondas", desc: "No usar 24 horas. Limpiar bien. Hervir un vaso de agua dentro por 10 minutos hasta que el vapor cubra las paredes." },
          { name: "Bacha / Tarja", desc: "Limpiar y dejar secar 24h. Verter agua hirviendo directamente de una olla al fuego sobre todas las superficies." },
          { name: "Cubiertos de Metal", desc: "Hagalá: Sumergir individualmente en una olla con agua hirviendo a borbotones (previamente kasherizada para Pesaj)." }
        ]
      },
      eng: {
        heroDesc: "From April 1 to 9, 2026. It is the festival of freedom, where the consumption and possession of Chametz is prohibited.",
        cleanTitle: "Sale and Cleaning",
        cleanDesc: "Chametz must disappear.",
        clean1: "Thoroughly clean the whole house, drawers, kitchen and car before April 1.",
        clean2: "Sell the remaining Chametz through your local Rabbi.",
        clean3: "Perform Bedikat Chametz (Search) the night before with a candle and feather.",
        laws1Ashk: "Absolute prohibition of Kitniyot. Rice, corn, beans, lentils or derivatives like corn syrup are not allowed.",
        laws1Sef: "Consumption of Kitniyot (rice, beans, etc.) is allowed if meticulously checked according to family tradition.",
        laws2Ashk: 'Kosher L\\'Pesach products that say "L\\'Ochlei Kitniyot" are NOT suitable for you.',
        laws2Sef: 'You can consume products marked as Kosher L\\'Pesach "L\\'Ochlei Kitniyot".',
        kashItems: [
          { name: "Ovens", desc: "Do not use for 24 hours. Clean with strong chemical. Turn on at max temp for 1 hour or use Self-Clean." },
          { name: "Microwave", desc: "Do not use for 24 hours. Clean well. Boil a glass of water inside for 10 minutes until steam covers walls." },
          { name: "Sink", desc: "Clean and let dry 24h. Pour boiling water directly from a pot on the fire over all surfaces." },
          { name: "Metal Cutlery", desc: "Hagalah: Submerge individually in a pot with boiling bubbling water (previously koshered for Pesach)." }
        ]
      }
    },
    'purim': {
      date: '2026-03-03T18:00:00',
      name: 'Purim',
      esp: {
        heroDesc: "Marzo 3, 2026. Fiesta de la alegría, disfraces, lectura de la Meguilá y regalos de comida (Mishloaj Manot).",
        cleanTitle: "Mishloaj Manot (Regalos)",
        cleanDesc: "Precauciones al armar tus canastas.",
        clean1: "Todos los dulces y alimentos deben tener certificación Kosher verificable.",
        clean2: "Incluye al menos dos tipos diferentes de alimentos listos para comer.",
        clean3: "Si horneas en casa, asegúrate de haber separado Jalá si la masa lo requiere.",
        laws1Ashk: "Los vinos y licores deben ser Kosher. Vinos no 'Mevushal' requieren cuidado extremo al servirse.",
        laws1Sef: "Misma regla para vinos. La Seudá (banquete festivo) debe incluir pan y carne preferentemente.",
        laws2Ashk: "Es obligación escuchar la Meguilá de noche y de día.",
        laws2Sef: "Se mantiene la misma obligación de lectura de Meguilá.",
        kashItems: [
          { name: "Dulces Importados", desc: "Revisa siempre el sello. Caramelos de goma y malvaviscos suelen contener gelatina no kosher si no tienen sello." },
          { name: "Bebidas Alcohólicas", desc: "Tequila puro 100% agave suele ser aceptable, licores saborizados requieren certificación." }
        ]
      },
      eng: {
        heroDesc: "March 3, 2026. Festival of joy, costumes, reading of the Megillah, and food gifts (Mishloach Manot).",
        cleanTitle: "Mishloach Manot (Gifts)",
        cleanDesc: "Precautions when making your baskets.",
        clean1: "All sweets and foods must have verifiable Kosher certification.",
        clean2: "Include at least two different types of ready-to-eat foods.",
        clean3: "If baking at home, ensure you have separated Challah if the dough requires it.",
        laws1Ashk: "Wines and liquors must be Kosher. Non-'Mevushal' wines require extreme care when served.",
        laws1Sef: "Same rule for wines. The Seudah (festive banquet) should preferably include bread and meat.",
        laws2Ashk: "It is an obligation to hear the Megillah at night and during the day.",
        laws2Sef: "The same obligation applies for the reading of the Megillah.",
        kashItems: [
          { name: "Imported Sweets", desc: "Always check the seal. Gummy candies and marshmallows often contain non-kosher gelatin without a seal." },
          { name: "Alcoholic Beverages", desc: "Pure 100% agave Tequila is usually acceptable, flavored liquors require certification." }
        ]
      }
    },
    'shavuot': {
      date: '2026-05-22T18:00:00',
      name: 'Shavuot',
      esp: {
        heroDesc: "Mayo 22, 2026. Celebramos la entrega de la Torá. Es costumbre consumir comidas lácteas de alta calidad.",
        cleanTitle: "Menú Lácteo",
        cleanDesc: "Cuidados especiales con lácteos y carnes.",
        clean1: "Comprar quesos y leches con supervisión estricta (Jalav Israel preferentemente).",
        clean2: "Revisar pastas y bases para pasteles que puedan requerir separación de Jalá.",
        clean3: "Si se come carne en otra comida, esperar el tiempo reglamentario (ej. 6 horas) antes de los lácteos.",
        laws1Ashk: "Costumbre arraigada de consumir lácteos en el primer día. Algunos comen lácteos y luego carne en la misma comida (separando y enjuagando la boca).",
        laws1Sef: "Muchos consumen lácteos como una comida separada y comen carne en la comida principal de la fiesta.",
        laws2Ashk: "Atención a postres fritos o cremosos, verificar sellos.",
        laws2Sef: "Especial atención a productos de panadería (Pas Yisroel).",
        kashItems: [
          { name: "Quesos Duros", desc: "Requieren una supervisión Kashrut mucho más compleja por el uso de cuajo (rennet)." },
          { name: "Utensilios Lácteos", desc: "Asegurarse de no mezclar esponjas ni platos usados para carne." }
        ]
      },
      eng: {
        heroDesc: "May 22, 2026. We celebrate the giving of the Torah. It is customary to consume high-quality dairy foods.",
        cleanTitle: "Dairy Menu",
        cleanDesc: "Special care with dairy and meat.",
        clean1: "Buy cheeses and milks with strict supervision (Cholov Yisroel preferably).",
        clean2: "Check pastas and pie crusts that may require Challah separation.",
        clean3: "If meat is eaten at another meal, wait the required time (e.g., 6 hours) before dairy.",
        laws1Ashk: "Deep-rooted custom of consuming dairy on the first day. Some eat dairy and then meat in the same meal (cleansing the mouth in between).",
        laws1Sef: "Many consume dairy as a separate meal and eat meat at the main festival meal.",
        laws2Ashk: "Pay attention to fried or creamy desserts, verify seals.",
        laws2Sef: "Special attention to bakery products (Pas Yisroel).",
        kashItems: [
          { name: "Hard Cheeses", desc: "Require much more complex Kashrut supervision due to the use of rennet." },
          { name: "Dairy Utensils", desc: "Ensure you do not mix sponges or plates used for meat." }
        ]
      }
    },
    'rosh-hashana': {
      date: '2026-09-11T18:00:00',
      name: 'Rosh Hashaná',
      esp: {
        heroDesc: "Septiembre 11-13, 2026. Año Nuevo Judío. Se consumen alimentos dulces como símbolo de un buen año.",
        cleanTitle: "Símbolos (Simanim)",
        cleanDesc: "Limpieza y revisión de alimentos simbólicos.",
        clean1: "Revisar la granada minuciosamente para evitar ingerir insectos ocultos.",
        clean2: "Usar miel 100% pura de abeja, verificando que no tenga aditivos no kosher.",
        clean3: "El puerro (poro) y la acelga/espinaca deben lavarse con jabón especial para eliminar plagas.",
        laws1Ashk: "Se evita comer nueces porque su valor numérico hebreo equivale a la palabra 'pecado'.",
        laws1Sef: "Generalmente se consumen una mayor variedad de Simanim, como cabeza de cordero o pez.",
        laws2Ashk: "Evitar alimentos amargos o muy ácidos.",
        laws2Sef: "Las costumbres varían según la comunidad específica, pero el enfoque es la dulzura.",
        kashItems: [
          { name: "Cabeza de Pescado", desc: "Debe provenir de un pez kosher (con aletas y escamas)." },
          { name: "Verduras de Hoja", desc: "Requieren revisión intensa contra insectos. Usar mesas de luz de ser posible." }
        ]
      },
      eng: {
        heroDesc: "September 11-13, 2026. Jewish New Year. Sweet foods are consumed as a symbol of a good year.",
        cleanTitle: "Symbols (Simanim)",
        cleanDesc: "Cleaning and checking of symbolic foods.",
        clean1: "Check the pomegranate thoroughly to avoid ingesting hidden insects.",
        clean2: "Use 100% pure bee honey, verifying it has no non-kosher additives.",
        clean3: "Leeks and chard/spinach must be washed with special soap to remove pests.",
        laws1Ashk: "Nuts are avoided because their Hebrew numerical value is equivalent to the word 'sin'.",
        laws1Sef: "Generally a wider variety of Simanim are consumed, such as lamb or fish head.",
        laws2Ashk: "Avoid bitter or very acidic foods.",
        laws2Sef: "Customs vary by specific community, but the focus is on sweetness.",
        kashItems: [
          { name: "Fish Head", desc: "Must come from a kosher fish (with fins and scales)." },
          { name: "Leafy Greens", desc: "Require intense checking for insects. Use light boxes if possible." }
        ]
      }
    },
    'yom-kipur': {
      date: '2026-09-20T18:00:00',
      name: 'Yom Kipur',
      esp: {
        heroDesc: "Septiembre 20, 2026. Día del Perdón. Es un ayuno de 25 horas donde nos abstenemos de comer y beber.",
        cleanTitle: "Seudá Mafseket",
        cleanDesc: "La última comida antes del ayuno.",
        clean1: "Consumir alimentos ligeros y de fácil digestión.",
        clean2: "Evitar alimentos excesivamente salados o picantes para no generar sed.",
        clean3: "Comenzar el ayuno unos minutos antes del atardecer oficial.",
        laws1Ashk: "Muchos acostumbran comer Kreplaj (pasta rellena de carne) en la víspera.",
        laws1Sef: "Se acostumbra comer sopas ligeras y pollo asado.",
        laws2Ashk: "Prohibición total de alimentos, bebidas, uso de cuero y ungüentos durante el ayuno.",
        laws2Sef: "Iguales prohibiciones estrictas para todos los judíos.",
        kashItems: [
          { name: "Rompimiento del Ayuno", desc: "Tener cuidado de no consumir preparaciones calientes cocinadas en Shabat o Yom Kipur por otra persona judía." }
        ]
      },
      eng: {
        heroDesc: "September 20, 2026. Day of Atonement. It is a 25-hour fast where we abstain from eating and drinking.",
        cleanTitle: "Seudah Mafseket",
        cleanDesc: "The last meal before the fast.",
        clean1: "Consume light, easily digestible foods.",
        clean2: "Avoid excessively salty or spicy foods so as not to induce thirst.",
        clean3: "Begin the fast a few minutes before the official sunset.",
        laws1Ashk: "Many have the custom of eating Kreplach (meat-filled dough) on the eve.",
        laws1Sef: "It is customary to eat light soups and roasted chicken.",
        laws2Ashk: "Total prohibition of food, drinks, use of leather, and ointments during the fast.",
        laws2Sef: "Same strict prohibitions apply to all Jews.",
        kashItems: [
          { name: "Breaking the Fast", desc: "Be careful not to consume hot preparations cooked on Shabbat or Yom Kippur by another Jewish person." }
        ]
      }
    },
    'sukot': {
      date: '2026-09-25T18:00:00',
      name: 'Sukot',
      esp: {
        heroDesc: "Septiembre 25 - Oct 2, 2026. Festividad de las Cabañas. Las comidas deben consumirse en la Sucá.",
        cleanTitle: "La Sucá",
        cleanDesc: "Condiciones para comer en la cabaña.",
        clean1: "Cualquier comida que incluya pan (más del volumen de una aceituna) debe comerse allí.",
        clean2: "El 'Sjaj' (techo) debe estar hecho de ramas naturales y no debe impedir ver las estrellas completamente.",
        clean3: "Se deben preparar platillos festivos con antelación.",
        laws1Ashk: "Suelen ser muy estrictos en comer cualquier producto de repostería/masas (Mezonot) en la Sucá.",
        laws1Sef: "La obligación principal recae sobre el pan, pero es meritorio comer todo dentro.",
        laws2Ashk: "Los utensilios llevados a la Sucá deben limpiarse antes del siguiente día festivo.",
        laws2Sef: "Uso de hermosas vajillas es parte de la 'Mitzvá' de embellecer la fiesta.",
        kashItems: [
          { name: "Arba Minim", desc: "Las 4 especies (Etrog, Lulav, Hadás y Aravá) deben provenir de plantaciones supervisadas sin injertos no kosher." }
        ]
      },
      eng: {
        heroDesc: "September 25 - Oct 2, 2026. Festival of Booths. Meals must be consumed in the Sukkah.",
        cleanTitle: "The Sukkah",
        cleanDesc: "Conditions for eating in the booth.",
        clean1: "Any meal including bread (more than the volume of an olive) must be eaten there.",
        clean2: "The 'Schach' (roof) must be made of natural branches and shouldn't completely block the stars.",
        clean3: "Festive dishes must be prepared in advance.",
        laws1Ashk: "Usually very strict about eating any pastry/dough products (Mezonot) in the Sukkah.",
        laws1Sef: "Main obligation falls on bread, but it is praiseworthy to eat everything inside.",
        laws2Ashk: "Utensils brought to the Sukkah must be cleaned before the next holiday.",
        laws2Sef: "Using beautiful tableware is part of the 'Mitzvah' of beautifying the holiday.",
        kashItems: [
          { name: "Arba Minim", desc: "The 4 species (Etrog, Lulav, Hadas, Arava) must come from supervised orchards without non-kosher grafting." }
        ]
      }
    },
    'januca': {
      date: '2026-12-04T18:00:00',
      name: 'Janucá',
      esp: {
        heroDesc: "Diciembre 4 - 12, 2026. Milagro de la luz. Es costumbre comer frituras en aceite y lácteos.",
        cleanTitle: "Alimentos Fritos",
        cleanDesc: "Sufganiyot (donas) y Latkes (tortitas de papa).",
        clean1: "Asegurarse de usar aceite vegetal con supervisión Kosher.",
        clean2: "Si compras donas en panaderías, verificar que tengan certificado activo.",
        clean3: "Freír carne y luego lácteos en la misma sartén o aceite está estrictamente prohibido.",
        laws1Ashk: "Popularidad masiva de los Latkes (tortitas de papa) servidos con puré de manzana o crema agria.",
        laws1Sef: "Suelen preparar frituras en almíbar, como Bimuelos.",
        laws2Ashk: "Atención a la posible mezcla de utensilios lácteos al servir crema agria.",
        laws2Sef: "Revisión meticulosa de quesos y leches si se usan para celebrar el milagro de Yehudit.",
        kashItems: [
          { name: "Aceite Kosher", desc: "Todo el aceite para freír debe estar certificado para asegurar que las líneas de envasado no procesan grasas animales." }
        ]
      },
      eng: {
        heroDesc: "December 4 - 12, 2026. Miracle of light. It is customary to eat foods fried in oil and dairy.",
        cleanTitle: "Fried Foods",
        cleanDesc: "Sufganiyot (donuts) and Latkes (potato pancakes).",
        clean1: "Ensure the use of vegetable oil with Kosher supervision.",
        clean2: "If buying donuts at bakeries, verify they have an active certificate.",
        clean3: "Frying meat and then dairy in the same pan or oil is strictly prohibited.",
        laws1Ashk: "Massive popularity of Latkes (potato pancakes) served with applesauce or sour cream.",
        laws1Sef: "Often prepare fried dough in syrup, like Bimuelos.",
        laws2Ashk: "Pay attention to possible mixing of dairy utensils when serving sour cream.",
        laws2Sef: "Meticulous checking of cheeses and milks if used to celebrate the miracle of Yehudit.",
        kashItems: [
          { name: "Kosher Oil", desc: "All frying oil must be certified to ensure packaging lines do not process animal fats." }
        ]
      }
    }
  };

  const jagData = DATA[jagParam as keyof typeof DATA] || DATA['pesaj'];
  const t = jagData[isEng ? 'eng' : 'esp'];

  const [userOrigin, setUserOrigin] = useState('ashkenazi');
  const [daysLeft, setDaysLeft] = useState(0);
  
  useEffect(() => {
    const origin = localStorage.getItem('userOrigin');
    if (origin) setUserOrigin(origin);
    const jagDate = new Date(jagData.date);
    const today = new Date();
    const diff = Math.ceil((jagDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    setDaysLeft(diff > 0 ? diff : 0);
  }, [jagData.date]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans pb-20 selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto p-4 lg:p-8">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-10 px-2 mt-4 lg:mt-0">
          <div className="flex items-center gap-4">
            <Link href="/calendario" className="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center border border-slate-700 hover:bg-slate-700 transition-colors shadow-lg">
              <ArrowLeft className="text-slate-400 w-6 h-6" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">Mega-Guía: {jagData.name}</h1>
              <p className="text-emerald-500 font-medium text-sm flex items-center gap-1">
                {tGlobal.subtitle}
              </p>
            </div>
          </div>
        </div>

        {/* Hero Alert */}
        <div className="bg-gradient-to-br from-emerald-600/20 to-teal-900/40 border border-emerald-500/30 p-6 rounded-3xl mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 blur-3xl rounded-full"></div>
          <div className="flex flex-col sm:flex-row gap-6 items-start sm:items-center relative z-10">
            <div className="w-16 h-16 bg-emerald-500/20 rounded-2xl flex items-center justify-center flex-shrink-0 border border-emerald-500/30">
              <Calendar className="w-8 h-8 text-emerald-400" />
            </div>
            <div className="flex-grow">
              <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                {tGlobal.next}: {jagData.name}
              </h2>
              <p className="text-emerald-100/80 text-sm leading-relaxed">
                {t.heroDesc}
              </p>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-2xl border border-slate-700/50 text-center min-w-[120px]">
              <span className="block text-3xl font-black text-white">{daysLeft}</span>
              <span className="text-xs font-bold text-emerald-500 uppercase tracking-wider">{tGlobal.daysLeft} {tGlobal.days}</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            
            <section className="bg-slate-800/50 rounded-3xl p-6 lg:p-8 border border-slate-700/50 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500 to-orange-500"></div>
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                <AlertTriangle className="text-amber-500 w-6 h-6" />
                {t.cleanTitle}
              </h3>
              <p className="text-slate-400 text-sm mb-6 pb-6 border-b border-slate-700/50">
                {t.cleanDesc}
              </p>
              <ul className="space-y-4">
                {[t.clean1, t.clean2, t.clean3].map((step, idx) => (
                  <li key={idx} className="flex items-start gap-3 group">
                    <div className="mt-0.5 w-6 h-6 rounded-full bg-slate-900 border border-slate-700 flex items-center justify-center text-slate-500 group-hover:border-emerald-500 group-hover:text-emerald-500 transition-colors flex-shrink-0">
                      <span className="text-xs font-bold">{idx + 1}</span>
                    </div>
                    <span className="text-slate-300 text-sm leading-relaxed">{step}</span>
                  </li>
                ))}
              </ul>
            </section>

            <section className="bg-slate-800/50 rounded-3xl p-6 lg:p-8 border border-slate-700/50 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-indigo-500"></div>
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                <BookOpen className="text-blue-500 w-6 h-6" />
                {userOrigin === 'ashkenazi' ? tGlobal.lawsTitleAshk : tGlobal.lawsTitleSef}
              </h3>
              <p className="text-slate-400 text-sm mb-6 pb-6 border-b border-slate-700/50 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                {tGlobal.lawsDesc}
              </p>
              <div className="space-y-4">
                <div className="bg-blue-900/10 border border-blue-500/20 p-5 rounded-2xl flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                  <p className="text-blue-100/90 text-sm leading-relaxed">
                    {userOrigin === 'ashkenazi' 
                      ? t.laws1Ashk 
                      : t.laws1Sef}
                  </p>
                </div>
                <div className="bg-blue-900/10 border border-blue-500/20 p-5 rounded-2xl flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                  <p className="text-blue-100/90 text-sm leading-relaxed">
                    {userOrigin === 'ashkenazi' 
                      ? t.laws2Ashk 
                      : t.laws2Sef}
                  </p>
                </div>
              </div>
            </section>
          </div>

          {/* Sidebar Info */}
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6 rounded-3xl border border-slate-700 shadow-xl">
              <h4 className="text-white font-bold mb-2">{tGlobal.kashTitle}</h4>
              <p className="text-xs text-slate-400 mb-6">{tGlobal.kashDesc}</p>
              
              <div className="space-y-4">
                {t.kashItems.map((item: any, idx: number) => (
                  <div key={idx} className="border-l-2 border-emerald-500 pl-4 py-1">
                    <span className="block text-emerald-400 font-bold text-sm mb-1">{item.name}</span>
                    <span className="text-xs text-slate-300 leading-relaxed block">{item.desc}</span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}

export default function ChaguimWrapper() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">Loading...</div>}>
      <ChaguimContent />
    </Suspense>
  );
}
""")
print("Generated dynamic chaguim page")

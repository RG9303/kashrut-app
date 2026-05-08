import os

# --- CALENDARIO ---
with open('src/app/calendario/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("import React from 'react';", "import React from 'react';\nimport { useLanguage } from '@/hooks/useLanguage';")
content = content.replace("export default function CalendarioPage() {", """
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
    pesajTip: 'Se requiere una limpieza milimétrica del hogar. Todo alimento empacado durante estos 8 días requiere explícitamente el sello "Kosher L\\'Pesach". Ashknenazím evitan comer Kitniyot (arroz, maíz, legumbres).',
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
    pesajTip: 'Meticulous home cleaning is required. All packaged food during these 8 days explicitly requires the "Kosher L\\'Pesach" seal. Ashkenazim avoid eating Kitniyot (rice, corn, legumes).',
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
""")

reps = {
    "'Fiesta de la alegría, disfraces y la lectura de la Meguilá.'": "t.purimDesc",
    "'Asegúrate de que todos los dulces, vinos y alimentos incluidos en tus \"Mishloaj Manot\" (regalos de comida) tengan certificación Kosher y sellos verificables para que quien lo reciba pueda disfrutarlos con absoluta confianza.'": "t.purimTip",
    "'La liberación de Egipto. Prohibición absoluta de consumir o poseer Jametz (leudados).'": "t.pesajDesc",
    "'Se requiere una limpieza milimétrica del hogar. Todo alimento empacado durante estos 8 días requiere explícitamente el sello \"Kosher L\\'Pesach\". Ashknenazím evitan comer Kitniyot (arroz, maíz, legumbres).'": "t.pesajTip",
    "'Ver Mega-Guía de Pesaj'": "t.pesajLink",
    "'Celebra la entrega sublime de la Torá en el Monte Sinaí.'": "t.shavuotDesc",
    "'Es tradición consumir majestuosos banquetes lácteos (Cheesecakes, pastas). Presta especial atención al sello de \"Jalav Israel\" (leche supervisada) y no olvides esperar el tiempo reglamentario tras comer carne antes de consumir los lácteos festivos.'": "t.shavuotTip",
    "'El Año Nuevo Judío. Días del juicio y la coronación divina.'": "t.roshDesc",
    "'Comemos Simanim (señales místicas de buen augurio) como manzana con miel, granada y cabeza de pescado. Asegura que la miel sea 100% pura abeja y revisa intensamente la granada, poro y espinacas en búsqueda de insectos.'": "t.roshTip",
    "'El sagrado Día del Perdón. Dedicado completamente al rezo espiritual.'": "t.kipurDesc",
    "'Ayuno profundo y absoluto de 25 horas. No hay preparación de alimentos para este Chag, pero tu cena previa de \"Seuda Mafseket\" debe ser ligera, cocinada con rigor Kosher y sin alimentos demasiado salados.'": "t.kipurTip",
    "'La festividad de las Cabañas, recordando los 40 años en el desierto.'": "t.sukotDesc",
    "'Cualquier comida establecida (pan, jalá, mezonot fuertes) debe ser consumida exclusivamente dentro de la estructura rabínicamente legal de la Sucá. Reúne las 4 Especies (Lulav y Etrog) con sellos de supervisión agraria validada.'": "t.sukotTip",
    "'El milagro de las luces y el rescate del Sagrado Templo.'": "t.janucaDesc",
    "'Costumbre de consumir alimentos fritos brillantes en aceite, como Latkes y Sufganiyot (donas). Compra aceite Kosher de alta calidad y revisa muy bien los lácteos de los postres fritos cruzando las listas internacionales Kashrut.'": "t.janucaTip",
    ">Calendario Hebreo<": ">{t.title}<",
    "Ciclo Anual 2026 • 5786/5787</p>": "{t.subtitle}</p>",
    ">Cronograma Kashrut<": ">{t.heroTitle}<",
    "Cada festividad judía trae consigo leyes culinarias únicas y atmósferas especiales. Desplázate por el calendario para planificar estratégicamente tus próximos Chaguim y evitar contratiempos dietéticos.": "{t.heroDesc}",
    "Kashrut Advisor": "{t.advisor}"
}
for k, v in reps.items():
    content = content.replace(k, v)

with open('src/app/calendario/page.tsx', 'w') as f:
    f.write(content)


# --- CHAGUIM ---
with open('src/app/chaguim/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("import React, { useState, useEffect } from 'react';", "import React, { useState, useEffect } from 'react';\nimport { useLanguage } from '@/hooks/useLanguage';")
content = content.replace("export default function ChaguimPage() {", """
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
    laws2Ashk: 'Los productos Kosher L\\'Pesach que dicen "Leojlei Kitniyot" NO son aptos para ti.',
    laws2Sef: 'Puedes consumir productos marcados como Kosher L\\'Pesach "Leojlei Kitniyot".',
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
    laws2Ashk: 'Kosher L\\'Pesach products that say "L\\'Ochlei Kitniyot" are NOT suitable for you.',
    laws2Sef: 'You can consume products marked as Kosher L\\'Pesach "L\\'Ochlei Kitniyot".',
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
""")

reps_c = {
    ">Guía Chaguim<": ">{t.title}<",
    "Preparación Activa</p>": "{t.subtitle}</p>",
    "> Próxima Festividad": "> {t.next}",
    ">Faltan <": ">{t.daysLeft} <",
    "> días<": "> {t.days}<",
    "Del 1 al 9 de Abril de 2026. Es la festividad de la libertad, donde se prohíbe el consumo y posesión de Jametz.": "{t.heroDesc}",
    ">Venta y Limpieza<": ">{t.cleanTitle}<",
    "El Jametz debe desaparecer.": "{t.cleanDesc}",
    "Limpiar minuciosamente toda la casa, cajones, cocina y auto antes del 1 de Abril.": "{t.clean1}",
    "Vender el Jametz sobrante a través de tu Rabino local.": "{t.clean2}",
    "Realizar Bedikat Jametz (Búsqueda) la noche anterior con vela y pluma.": "{t.clean3}",
    "'Leyes de Ashkenazím' : 'Leyes de Sefaradim'": "t.lawsTitleAshk : t.lawsTitleSef",
    "Reglas basadas en tu costumbre actual.": "{t.lawsDesc}",
    "'Prohibición absoluta de Kitniyot. No se permite arroz, maíz, frijoles, lentejas ni derivados como jarabe de maíz.'": "t.laws1Ashk",
    "'Permitido el consumo de Kitniyot (arroz, frijoles, etc.) si se revisan meticulosamente según la tradición familiar.'": "t.laws1Sef",
    "'Los productos Kosher L\\'Pesach que dicen \"Leojlei Kitniyot\" NO son aptos para ti.'": "t.laws2Ashk",
    "'Puedes consumir productos marcados como Kosher L\\'Pesach \"Leojlei Kitniyot\".'": "t.laws2Sef",
    ">Kasherización de la Cocina<": ">{t.kashTitle}<",
    "Preparando el entorno físico.": "{t.kashDesc}",
    ">Hornos<": ">{t.ovens}<",
    "No usar 24 horas. Limpiar con químico fuerte. Encender a máxima temperatura por 1 hora o usar función Self-Clean.": "{t.ovensDesc}",
    ">Microondas<": ">{t.micro}<",
    "No usar 24 horas. Limpiar bien. Hervir un vaso de agua dentro por 10 minutos hasta que el vapor cubra las paredes.": "{t.microDesc}",
    ">Bacha / Tarja<": ">{t.sink}<",
    "Limpiar y dejar secar 24h. Verter agua hirviendo directamente de una olla al fuego sobre todas las superficies.": "{t.sinkDesc}",
    ">Cubiertos de Metal<": ">{t.cutlery}<",
    "Hagalá: Sumergir individualmente en una olla con agua hirviendo a borbotones (previamente kasherizada para Pesaj).": "{t.cutleryDesc}"
}
for k, v in reps_c.items():
    content = content.replace(k, v)

with open('src/app/chaguim/page.tsx', 'w') as f:
    f.write(content)

print("Calendario and Chaguim replaced.")

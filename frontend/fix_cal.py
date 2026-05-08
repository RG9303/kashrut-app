import re
with open('src/app/calendario/page.tsx', 'r') as f:
    content = f.read()

correct_texts = """const TEXTS = {
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
};"""

# extract everything after the TEXTS definition
parts = content.split("export default function CalendarioPage() {")
content = correct_texts + "\n\nexport default function CalendarioPage() {" + parts[1]

with open('src/app/calendario/page.tsx', 'w') as f:
    f.write(content)
print("calendario texts fixed")

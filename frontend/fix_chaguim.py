with open('src/app/chaguim/page.tsx', 'r') as f:
    content = f.read()

correct_texts = """const TEXTS = {
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
};"""

parts = content.split("export default function ChaguimPage() {")

# we must retain imports in chaguim/page.tsx
# In chaguim/page.tsx, the imports were preserved because the replacement was:
# import React, { useState, useEffect } from 'react';\nimport { useLanguage } from '@/hooks/useLanguage';
# but let's just make sure
header = """'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, BookOpen, Clock, CheckCircle2, AlertTriangle, Calendar } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';

"""

content = header + correct_texts + "\n\nexport default function ChaguimPage() {" + parts[1]

with open('src/app/chaguim/page.tsx', 'w') as f:
    f.write(content)
print("chaguim fixed")

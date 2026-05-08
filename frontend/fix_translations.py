with open('src/app/page.tsx', 'r') as f:
    content = f.read()

reps = {
    '/> Activar Cámara': '/> {t.activateCamera}',
    'title="Detener Cámara"': 'title={t.stopCamera}',
    '/> Capturar': '/> {t.capture}',
    '/> Subir desde Galería': '/> {t.uploadGallery}',
    'placeholder="Insertar Código Barras (EAN/UPC)"': 'placeholder={t.insertBarcode}',
    '>Buscar<': '>{t.search}<',
    '>Ashkenazí<': '>{t.ashkenazi}<',
    '>Sefaradí<': '>{t.sephardi}<',
    '>México<': '>{t.mexico}<',
    '>Estados Unidos<': '>{t.usa}<',
    '>Argentina<': '>{t.argentina}<',
    '>Israel<': '>{t.israel}<',
    '>España<': '>{t.spain}<',
    '>Otro País<': '>{t.otherCountry}<',
    '>Nota importante:<': '>{t.importantNote}<',
    '>Esperando Análisis<': '>{t.waitingAnalysis}<',
    '>Estatus Final<': '>{t.finalStatus}<',
    '>Certeza IA<': '>{t.aiConfidence}<',
    '>Resumen Rápido<': '>{t.quickSummary}<',
    '>Sello<': '>{t.seal}<',
    '>Ninguno<': '>{t.none}<',
    '>Categoría<': '>{t.category}<',
    '>Registro OpenFoodFacts<': '>{t.openFoodFacts}<',
    '>Producto<': '>{t.product}<',
    '>Desconocido<': '>{t.unknown}<',
    '>Marca<': '>{t.brand}<',
    '>Alertas Relevantes<': '>{t.relevantAlerts}<',
    '>Filtros Adicionales<': '>{t.additionalFilters}<',
    '>Vegano<': '>{t.vegan}<',
    '>Sin Gluten<': '>{t.glutenFree}<',
    '>Sin Lácteos<': '>{t.dairyFree}<',
    '>Información de dietas no disponible<': '>{t.dietInfoNA}<',
    '>Detalle del Análisis Halájico<': '>{t.halachicDetail}<',
    '>Escanear Otro Producto<': '>{t.scanAnother}<',
    '>Historial Reciente<': '>{t.recentHistory}<',
    '>Ver Receta<': '>{t.viewRecipe}<',
    '>Ingredientes Requeridos<': '>{t.requiredIngredients}<',
    '>Pasos de Preparación<': '>{t.prepSteps}<',
    '>Próxima Festividad<': '>{t.nextHoliday}<',
    '>Faltan<': '>{t.daysLeft}<',
    '>días<': '>{t.days}<',
    '>Preparación<': '>{t.preparation}<',
}

for k, v in reps.items():
    content = content.replace(k, v)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
print("Fixes applied.")

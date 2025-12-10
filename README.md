# 🧾 Sistema de Escaneo de Facturas

Sistema completo de procesamiento OCR de facturas similar a **Amazon Textract**, utilizando **Tesseract + OpenCV** para el backend y **Flutter** para la aplicación móvil.

## 📱 Arquitectura

```
┌─────────────────────┐
│   Flutter App       │
│   (iOS/Android)     │
│   - Captura fotos   │
│   - UI moderna      │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   Backend Python    │
│   Flask API         │
│   - OpenCV          │
│   - Tesseract OCR   │
│   - Extracción datos│
└─────────────────────┘
```

## 🚀 Características

### Backend (Python)
- ✅ **Preprocesamiento avanzado** con OpenCV
  - Conversión a escala de grises
  - Reducción de ruido
  - Corrección automática de inclinación
  - Threshold adaptativo
  - Mejora de contraste
- ✅ **OCR con Tesseract** optimizado para español
- ✅ **Extracción estructurada de datos**:
  - Número de factura
  - Fecha
  - Importe total
  - Subtotal e IVA
  - NIF/CIF
  - Nombre del proveedor
- ✅ **Coordenadas de palabras** (similar a AWS Textract)
- ✅ **Métricas de confianza**

### App Flutter
- ✅ **Captura de fotos** con cámara
- ✅ **Selección de galería**
- ✅ **UI moderna** con Material Design 3
- ✅ **Visualización de resultados** estructurados
- ✅ **Indicadores de confianza** visuales
- ✅ **Manejo de errores** robusto
- ✅ **Soporte iOS y Android**

## 📋 Instalación

### Paso 1: Configurar Backend

#### Instalar Tesseract

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**Windows:**
- Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
- Agregar al PATH

#### Instalar dependencias Python

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Ejecutar backend

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Paso 2: Configurar App Flutter

#### Instalar dependencias

```bash
cd opencv
flutter pub get
```

#### Configurar URL del backend

Edita `lib/main.dart` y configura la URL según tu entorno:

```dart
// Para iOS Simulator
static const String backendUrl = 'http://localhost:5000';

// Para Android Emulator
static const String backendUrl = 'http://10.0.2.2:5000';

// Para dispositivo físico (usa la IP de tu computadora)
static const String backendUrl = 'http://192.168.1.X:5000';
```

#### Ejecutar app

```bash
# iOS
flutter run -d ios

# Android
flutter run -d android

# O seleccionar dispositivo
flutter devices
flutter run -d <device-id>
```

## 🔧 Uso

### 1. Usando la App Flutter

1. **Abre la app** en tu dispositivo
2. **Captura** una foto de la factura o **selecciona** una de la galería
3. **Presiona** "Procesar Factura"
4. **Visualiza** los datos extraídos automáticamente

### 2. Usando el API directamente

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Procesar Factura
```bash
curl -X POST -F "file=@factura.jpg" http://localhost:5000/api/process-invoice
```

#### Respuesta Ejemplo
```json
{
  "success": true,
  "invoice_data": {
    "invoice_number": "F-2024-12345",
    "date": "16/10/2024",
    "total_amount": 250.75,
    "subtotal": 207.23,
    "tax": 43.52,
    "nif_cif": "B12345678",
    "vendor_name": "Empresa Ejemplo SL",
    "confidence": 87.5
  },
  "words": [...],
  "processing_info": {
    "total_words": 156,
    "average_confidence": 88.2
  }
}
```

## 📊 Comparación con Amazon Textract

| Característica | Amazon Textract | Este Sistema |
|---------------|-----------------|--------------|
| Extracción de texto | ✅ | ✅ |
| Detección de campos | ✅ | ✅ |
| Coordenadas de palabras | ✅ | ✅ |
| Métricas de confianza | ✅ | ✅ |
| Preprocesamiento | ✅ | ✅ (OpenCV) |
| Soporte español | ✅ | ✅ (Tesseract) |
| Costo | 💰 Por uso | 🆓 Gratis |
| Privacidad | ☁️ Cloud | 🏠 Local |
| Personalizable | ❌ | ✅ |

## 🛠️ Mejoras Futuras

- [ ] Soporte para múltiples idiomas
- [ ] Entrenamiento de modelo personalizado
- [ ] Reconocimiento de tablas
- [ ] Extracción de productos/líneas
- [ ] Base de datos para historial
- [ ] Exportación a PDF/Excel
- [ ] Modo batch para múltiples facturas
- [ ] Integración con sistemas contables

## 📝 Estructura del Proyecto

```
pruebasfotosopencv/
├── backend/
│   ├── app.py              # Servidor Flask + OCR
│   ├── requirements.txt    # Dependencias Python
│   ├── uploads/            # Carpeta temporal
│   └── README.md          # Documentación backend
├── opencv/                 # App Flutter
│   ├── lib/
│   │   └── main.dart      # Aplicación principal
│   ├── android/           # Configuración Android
│   ├── ios/              # Configuración iOS
│   └── pubspec.yaml      # Dependencias Flutter
└── README.md             # Este archivo
```

## 🐛 Solución de Problemas

### Backend no se conecta

1. Verifica que el backend esté corriendo: `curl http://localhost:5000/health`
2. Revisa la URL en `main.dart`
3. Para dispositivos físicos, usa la IP de tu computadora
4. Asegúrate de que el firewall permita conexiones en el puerto 5000

### Tesseract no funciona

1. Verifica la instalación: `tesseract --version`
2. Verifica idioma español: `tesseract --list-langs` (debe mostrar 'spa')
3. En macOS: `brew reinstall tesseract tesseract-lang`

### Permisos de cámara

- **iOS**: Los permisos ya están configurados en `Info.plist`
- **Android**: Los permisos ya están en `AndroidManifest.xml`
- Si no funciona, desinstala y reinstala la app

### Baja precisión en OCR

1. Asegúrate de que la imagen tenga buena iluminación
2. La factura debe estar en foco
3. Evita sombras y reflejos
4. La imagen debe estar lo más recta posible

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Creado como alternativa gratuita y local a Amazon Textract.

## 🙏 Agradecimientos

- **Tesseract OCR** - Motor de OCR
- **OpenCV** - Procesamiento de imágenes
- **Flutter** - Framework de UI
- **Flask** - Framework web Python


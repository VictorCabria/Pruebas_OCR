# 🏗️ Arquitectura del Sistema

## Vista General

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENTE (Flutter App)                   │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐           │
│  │  Camera    │  │  Gallery   │  │  Results    │           │
│  │  Capture   │  │  Picker    │  │  Display    │           │
│  └────────────┘  └────────────┘  └─────────────┘           │
│         │              │                  ▲                  │
│         └──────────────┴──────────────────┘                  │
│                        │                                     │
│                        │ HTTP POST /api/process-invoice     │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python/Flask)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API Layer (Flask)                  │  │
│  │  - /health                                            │  │
│  │  - /api/process-invoice                              │  │
│  │  - /api/analyze-receipt                              │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────┼─────────────────────────────┐  │
│  │         Image Processing Layer (OpenCV)              │  │
│  │                        │                              │  │
│  │  1. Grayscale ──▶ 2. Denoise ──▶ 3. Deskew          │  │
│  │        ▼                ▼                ▼            │  │
│  │  4. Threshold ◀── 5. Morphology ◀── 6. Enhance      │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────┼─────────────────────────────┐  │
│  │            OCR Layer (Tesseract)                      │  │
│  │                        │                              │  │
│  │  ┌────────────────────────────────────┐              │  │
│  │  │  text = pytesseract.image_to_string│              │  │
│  │  │  data = pytesseract.image_to_data  │              │  │
│  │  └────────────────────────────────────┘              │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────┼─────────────────────────────┐  │
│  │       Data Extraction Layer (Regex + Logic)          │  │
│  │                        │                              │  │
│  │  - Invoice Number  - Date         - Total Amount     │  │
│  │  - NIF/CIF        - Vendor Name   - Tax              │  │
│  │  - Confidence Score                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│                   JSON Response                              │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. Frontend (Flutter)

**Ubicación**: `opencv/lib/main.dart`

**Responsabilidades**:
- Captura de imágenes desde cámara
- Selección de imágenes de galería
- Envío de imágenes al backend via HTTP multipart
- Visualización de resultados estructurados
- Manejo de estados (loading, error, success)
- UI/UX moderna con Material Design 3

**Dependencias clave**:
- `image_picker`: Captura/selección de fotos
- `http`: Comunicación con backend
- `path_provider`: Manejo de rutas

### 2. Backend API (Flask)

**Ubicación**: `backend/app.py`

**Endpoints**:

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/health` | GET | Health check del servicio |
| `/api/process-invoice` | POST | Procesar factura completa |
| `/api/analyze-receipt` | POST | Análisis simplificado de tickets |

**Responsabilidades**:
- Recepción de imágenes
- Orquestación del pipeline de procesamiento
- Validación de entrada
- Respuesta JSON estructurada
- Manejo de errores

### 3. Image Processing (OpenCV)

**Ubicación**: `backend/app.py` función `preprocess_image()`

**Pipeline de Procesamiento**:

```python
1. BGR → Grayscale
   - Reduce complejidad
   - Mejora para OCR

2. Bilateral Filter
   - Reduce ruido
   - Preserva bordes
   - Parámetros: d=9, σ_color=75, σ_space=75

3. Deskew (Corrección de inclinación)
   - Detecta ángulo de rotación
   - Corrige si |ángulo| > 0.5°
   - Usa cv2.warpAffine()

4. Adaptive Threshold
   - Binarización adaptativa
   - Método: Gaussian
   - Block size: 11

5. Morphological Operations
   - Cierre morfológico
   - Limpia pequeños huecos
   - Kernel: 1x1

6. Histogram Equalization
   - Mejora contraste
   - Resalta texto
```

### 4. OCR Engine (Tesseract)

**Configuración**:
```python
config = '--oem 3 --psm 6 -l spa'
```

**Parámetros**:
- `--oem 3`: OCR Engine Mode (LSTM + Legacy)
- `--psm 6`: Page Segmentation Mode (Bloque uniforme)
- `-l spa`: Idioma español

**Modos de extracción**:
1. `image_to_string`: Texto plano
2. `image_to_data`: Texto + coordenadas + confianza

### 5. Data Extraction (Regex + Logic)

**Ubicación**: `backend/app.py` función `extract_invoice_data()`

**Patrones de Extracción**:

| Campo | Técnica | Patrón |
|-------|---------|--------|
| Número de Factura | Regex | `factura.*([A-Z0-9\-/]+)` |
| Fecha | Regex | `\d{1,2}[/-]\d{1,2}[/-]\d{2,4}` |
| NIF/CIF | Regex | `[A-Z]\d{7}[A-Z0-9]` |
| Total | Regex + Max | `\d{1,3}(?:[.,]\d{3})*[.,]\d{2}` |
| IVA | Regex | `IVA.*\d+[.,]\d{2}` |
| Proveedor | Heurística | Primera línea no vacía |

**Cálculo de Confianza**:
```python
confidence = (campos_encontrados / 5) * 100
```

## Flujo de Datos

```
1. Usuario captura/selecciona imagen
   │
   ▼
2. Flutter App envía imagen (multipart/form-data)
   │
   ▼
3. Flask recibe y valida archivo
   │
   ▼
4. OpenCV preprocesa imagen
   │ Binario optimizado
   ▼
5. Tesseract extrae texto
   │ Texto + coordenadas
   ▼
6. Regex extrae campos estructurados
   │ invoice_data: {...}
   ▼
7. Flask retorna JSON
   │
   ▼
8. Flutter muestra resultados con UI bonita
```

## Estructura de Datos

### Request (Multipart)
```http
POST /api/process-invoice HTTP/1.1
Content-Type: multipart/form-data; boundary=---xxx

---xxx
Content-Disposition: form-data; name="file"; filename="factura.jpg"
Content-Type: image/jpeg

[binary image data]
---xxx--
```

### Response (JSON)
```json
{
  "success": true,
  "invoice_data": {
    "raw_text": "...",
    "invoice_number": "F-2024-001",
    "date": "16/10/2024",
    "total_amount": 150.50,
    "subtotal": 124.38,
    "tax": 26.12,
    "nif_cif": "B12345678",
    "vendor_name": "Empresa SA",
    "items": [],
    "confidence": 85.5
  },
  "words": [
    {
      "text": "FACTURA",
      "confidence": 95.2,
      "bounding_box": {
        "x": 100,
        "y": 50,
        "width": 120,
        "height": 30
      }
    }
  ],
  "processing_info": {
    "total_words": 156,
    "average_confidence": 87.3
  }
}
```

## Decisiones de Diseño

### ¿Por qué Flutter?
- ✅ Cross-platform (iOS + Android con un solo código)
- ✅ UI moderna y fluida
- ✅ Hot reload para desarrollo rápido
- ✅ Ecosistema maduro de plugins

### ¿Por qué Flask?
- ✅ Simple y rápido de configurar
- ✅ Integración fácil con OpenCV/Tesseract
- ✅ Escalable con gunicorn/nginx
- ✅ Gran ecosistema Python

### ¿Por qué Tesseract?
- ✅ Gratis y open source
- ✅ Alta precisión
- ✅ Soporte para múltiples idiomas
- ✅ Activamente mantenido
- ✅ Funciona localmente (privacidad)

### ¿Por qué OpenCV?
- ✅ Líder en computer vision
- ✅ Funciones específicas para OCR
- ✅ Alto rendimiento (C++ backend)
- ✅ Amplia documentación

## Escalabilidad

### Horizontal Scaling
```
┌─────────┐       ┌──────────────┐
│ Client  │──────▶│ Load Balancer│
└─────────┘       └───────┬──────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │ Flask 1│      │ Flask 2│      │ Flask N│
    └────────┘      └────────┘      └────────┘
```

### Optimizaciones Futuras
- [ ] Cache de resultados (Redis)
- [ ] Cola de trabajos (Celery)
- [ ] Procesamiento asíncrono
- [ ] Modelo ML entrenado custom
- [ ] CDN para assets
- [ ] Base de datos para historial

## Seguridad

**Implementadas**:
- ✅ Validación de tipo de archivo
- ✅ Límite de tamaño (16MB)
- ✅ CORS configurado
- ✅ Procesamiento local (privacidad)

**Recomendadas para producción**:
- [ ] HTTPS/TLS
- [ ] Autenticación (JWT)
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] File scanning antivirus
- [ ] Audit logging

## Monitoreo

### Métricas Clave
- Tiempo de procesamiento por factura
- Tasa de éxito/fallo
- Confianza promedio de OCR
- Uso de CPU/memoria
- Requests por minuto

### Herramientas Sugeridas
- Prometheus + Grafana
- ELK Stack (logs)
- Sentry (error tracking)

## Testing

### Backend
```bash
pytest backend/tests/
```

### Frontend
```bash
flutter test
```

### Integration
```bash
python backend/test_api.py factura_prueba.jpg
```

---

**Última actualización**: Octubre 2024


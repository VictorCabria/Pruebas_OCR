# 📚 Índice del Sistema de Escaneo de Facturas

> Guía rápida para navegar toda la documentación del proyecto

---

## 🎯 ¿Por dónde empezar?

### 👋 Nuevo en el proyecto
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Resumen ejecutivo del proyecto
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guía paso a paso para comenzar
3. **[QUICKSTART.md](QUICKSTART.md)** - Inicio ultra rápido (5 minutos)

### 💻 Quiero instalarlo ahora
1. **[QUICKSTART.md](QUICKSTART.md)** - Pasos mínimos para empezar
2. **[start_backend.sh](start_backend.sh)** - Script para iniciar backend
3. **[start_flutter.sh](start_flutter.sh)** - Script para iniciar app

### 🔧 Soy desarrollador
1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura técnica completa
2. **[backend/README.md](backend/README.md)** - Documentación del backend
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía para contribuir

---

## 📖 Documentación Completa

### Guías Generales

| Documento | Propósito | Para quién |
|-----------|-----------|------------|
| **[README.md](README.md)** | Documentación principal del proyecto | Todos |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Resumen ejecutivo y features | Managers, evaluadores |
| **[QUICKSTART.md](QUICKSTART.md)** | Inicio rápido en 5 minutos | Usuarios impacientes |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Guía completa paso a paso | Principiantes |
| **[INDEX.md](INDEX.md)** | Este archivo | Navegación |

### Documentación Técnica

| Documento | Propósito | Para quién |
|-----------|-----------|------------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Arquitectura del sistema | Desarrolladores |
| **[backend/README.md](backend/README.md)** | API y backend | Backend devs |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Guía de contribución | Colaboradores |

---

## 🚀 Scripts y Herramientas

### Scripts de Inicio

| Script | Qué hace |
|--------|----------|
| **[start_backend.sh](start_backend.sh)** | Inicia el backend automáticamente |
| **[start_flutter.sh](start_flutter.sh)** | Inicia la app Flutter automáticamente |

### Scripts de Prueba

| Script | Qué hace |
|--------|----------|
| **[backend/test_api.py](backend/test_api.py)** | Prueba el API del backend |
| **[backend/example_usage.py](backend/example_usage.py)** | Ejemplos de uso programático |

### Configuración

| Archivo | Propósito |
|---------|-----------|
| **[backend/config.py](backend/config.py)** | Configuración del backend |
| **[backend/requirements.txt](backend/requirements.txt)** | Dependencias Python |
| **[opencv/pubspec.yaml](opencv/pubspec.yaml)** | Dependencias Flutter |
| **[docker-compose.yml](docker-compose.yml)** | Configuración Docker |
| **[backend/Dockerfile](backend/Dockerfile)** | Dockerfile del backend |

---

## 🎓 Guías por Nivel

### 🟢 Principiante

```
1. Lee: PROJECT_SUMMARY.md
   ↓
2. Sigue: GETTING_STARTED.md
   ↓
3. Ejecuta: ./start_backend.sh
   ↓
4. Ejecuta: ./start_flutter.sh
   ↓
5. ¡Escanea tu primera factura!
```

### 🟡 Intermedio

```
1. Lee: README.md
   ↓
2. Lee: ARCHITECTURE.md
   ↓
3. Revisa: backend/app.py
   ↓
4. Revisa: opencv/lib/main.dart
   ↓
5. Modifica y personaliza
```

### 🔴 Avanzado

```
1. Lee: ARCHITECTURE.md completo
   ↓
2. Revisa todo el código
   ↓
3. Lee: CONTRIBUTING.md
   ↓
4. Implementa mejoras
   ↓
5. Crea Pull Request
```

---

## 🔍 Búsqueda Rápida

### "¿Cómo hago...?"

| Quiero... | Ve a... |
|-----------|---------|
| Instalar el sistema | [QUICKSTART.md](QUICKSTART.md) |
| Entender la arquitectura | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Usar el API | [backend/README.md](backend/README.md) |
| Probar el sistema | [backend/test_api.py](backend/test_api.py) |
| Contribuir | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Resolver problemas | [README.md#solución-de-problemas](README.md#-solución-de-problemas) |
| Personalizar | [backend/config.py](backend/config.py) |
| Usar con Docker | [docker-compose.yml](docker-compose.yml) |

### "¿Dónde está...?"

| Busco... | Ubicación |
|----------|-----------|
| Código del backend | [backend/app.py](backend/app.py) |
| Código de la app | [opencv/lib/main.dart](opencv/lib/main.dart) |
| Preprocesamiento OCR | [backend/app.py](backend/app.py) función `preprocess_image()` |
| Extracción de datos | [backend/app.py](backend/app.py) función `extract_invoice_data()` |
| Configuración | [backend/config.py](backend/config.py) |
| Ejemplos de uso | [backend/example_usage.py](backend/example_usage.py) |
| Tests | [backend/test_api.py](backend/test_api.py) |

---

## 📱 Estructura del Código

### Backend (Python)

```
backend/
├── app.py                    ⭐ Servidor Flask principal
│   ├── preprocess_image()    📸 Preprocesamiento OpenCV
│   ├── extract_invoice_data()🔍 Extracción de datos
│   └── endpoints:
│       ├── /health          ✅ Health check
│       ├── /api/process-invoice 📄 Procesar factura
│       └── /api/analyze-receipt 🧾 Analizar ticket
├── config.py                 ⚙️  Configuración
├── test_api.py              🧪 Tests
└── example_usage.py         💡 Ejemplos
```

### Frontend (Flutter)

```
opencv/lib/
└── main.dart                 ⭐ App completa
    ├── MyApp                 🎨 Widget raíz
    ├── InvoiceScannerPage   📱 Página principal
    ├── _pickImageFromGallery() 🖼️ Galería
    ├── _takePhoto()         📸 Cámara
    ├── _processInvoice()    🔄 Procesar
    └── _buildResults()      📊 Mostrar resultados
```

---

## 🎯 Flujos de Trabajo Comunes

### 1. Instalación Completa

```bash
# 1. Instalar Tesseract
brew install tesseract tesseract-lang  # macOS

# 2. Iniciar backend
./start_backend.sh

# 3. Iniciar app
./start_flutter.sh

# 4. ¡Listo!
```

### 2. Desarrollo Backend

```bash
cd backend
source venv/bin/activate
python app.py  # Servidor con hot reload

# En otra terminal
python test_api.py mi_factura.jpg
```

### 3. Desarrollo Flutter

```bash
cd opencv
flutter pub get
flutter run  # Hot reload automático

# Edita: lib/main.dart
# Guarda para ver cambios
```

### 4. Pruebas

```bash
# Backend
cd backend
python test_api.py factura.jpg

# Flutter
cd opencv
flutter test
```

---

## 📊 Diagrama de Dependencias

```
┌─────────────────────────────────────────┐
│         Tu Aplicación                   │
└──────────────┬──────────────────────────┘
               │
               ├─── Flutter App
               │    ├── image_picker
               │    ├── http
               │    └── Material Design 3
               │
               └─── Backend Python
                    ├── Flask (API)
                    ├── OpenCV (Procesamiento)
                    ├── Tesseract (OCR)
                    ├── NumPy (Arrays)
                    └── Pillow (Imágenes)
```

---

## 🛠️ Recursos Externos

### Aprender más sobre las tecnologías

- **Flask**: https://flask.palletsprojects.com/
- **Flutter**: https://flutter.dev/docs
- **OpenCV**: https://docs.opencv.org/
- **Tesseract**: https://github.com/tesseract-ocr/tesseract
- **Material Design 3**: https://m3.material.io/

### Comunidad

- **Stack Overflow**: Tag `tesseract`, `opencv`, `flutter`
- **GitHub Issues**: Para bugs y features
- **Discord/Slack**: [Agregar si existe]

---

## ✅ Checklist del Proyecto

### Instalación
- [ ] Tesseract instalado y verificado
- [ ] Backend corriendo correctamente
- [ ] App Flutter ejecutándose
- [ ] Primera factura escaneada

### Comprensión
- [ ] Entiendo la arquitectura
- [ ] Sé cómo funciona el OCR
- [ ] Conozco los endpoints del API
- [ ] Puedo modificar la UI

### Personalización
- [ ] He ajustado los patrones regex
- [ ] He personalizado la UI
- [ ] He configurado para mi entorno
- [ ] He probado con mis facturas

### Contribución
- [ ] He leído CONTRIBUTING.md
- [ ] He creado mi fork
- [ ] He implementado mejoras
- [ ] He hecho mi pull request

---

## 🎓 Glosario

| Término | Significado |
|---------|-------------|
| **OCR** | Optical Character Recognition - Reconocimiento de texto |
| **Tesseract** | Motor de OCR open source de Google |
| **OpenCV** | Open Computer Vision - Biblioteca de visión por computadora |
| **Flutter** | Framework de Google para apps multiplataforma |
| **Flask** | Microframework web de Python |
| **Preprocesamiento** | Mejora de imagen antes de OCR |
| **Bounding Box** | Rectángulo que rodea texto detectado |
| **Confianza** | Métrica de precisión del OCR (0-100%) |
| **API REST** | Interfaz de programación web |
| **Endpoint** | URL específica del API |

---

## 📞 Ayuda Rápida

### Algo no funciona

1. **Backend no inicia**
   - Verifica: [GETTING_STARTED.md#-paso-2-configurar-backend-python](GETTING_STARTED.md#-paso-2-configurar-backend-python)
   - Logs: Revisa la salida de `python app.py`

2. **App no se conecta**
   - Verifica: [GETTING_STARTED.md#32-configurar-url-del-backend](GETTING_STARTED.md#32-configurar-url-del-backend)
   - Prueba: `curl http://localhost:5000/health`

3. **OCR impreciso**
   - Tips: [GETTING_STARTED.md#-paso-5-escanear-tu-primera-factura](GETTING_STARTED.md#-paso-5-escanear-tu-primera-factura)
   - Ajusta: [backend/config.py](backend/config.py)

4. **Otro problema**
   - Busca en: [README.md#-solución-de-problemas](README.md#-solución-de-problemas)
   - Abre un Issue en GitHub

---

## 🎉 ¡Empieza Aquí!

**Recomendación según tu objetivo:**

| Si eres... | Empieza aquí... |
|-----------|-----------------|
| 👤 Usuario final | [QUICKSTART.md](QUICKSTART.md) |
| 🧑‍💻 Desarrollador | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 🏢 Decision maker | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| 🎓 Aprendiz | [GETTING_STARTED.md](GETTING_STARTED.md) |
| 🤝 Contribuidor | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

**¡Buena suerte con tu sistema de escaneo de facturas! 🚀**

*Última actualización: Octubre 2024*


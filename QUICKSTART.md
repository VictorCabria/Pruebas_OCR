# 🚀 Inicio Rápido - Sistema de Escaneo de Facturas

Sigue estos pasos para tener el sistema funcionando en **5 minutos**.

## ⚡ Pasos Rápidos

### 1️⃣ Instalar Tesseract (2 minutos)

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**Windows:**
- Descarga: https://github.com/UB-Mannheim/tesseract/wiki
- Instala y agrega al PATH

**Verifica:**
```bash
tesseract --version
tesseract --list-langs  # Debe mostrar 'spa'
```

### 2️⃣ Iniciar Backend (1 minuto)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

✅ Verás: `🚀 Iniciando servidor de procesamiento de facturas...`

### 3️⃣ Configurar Flutter (1 minuto)

```bash
cd opencv
flutter pub get
```

**Configura la URL del backend en `lib/main.dart`:**

- **iOS Simulator**: `http://localhost:5000`
- **Android Emulator**: `http://10.0.2.2:5000`
- **Dispositivo físico**: `http://TU_IP_LOCAL:5000`

**Encuentra tu IP:**
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4
```

### 4️⃣ Ejecutar App (1 minuto)

```bash
flutter run
```

## 🎉 ¡Listo!

Ahora puedes:
1. **Capturar** o **seleccionar** una foto de factura
2. **Presionar** "Procesar Factura"
3. **Ver** los datos extraídos automáticamente

## 🧪 Probar el Backend (Opcional)

```bash
# Descarga una factura de prueba o usa una propia
curl -X POST -F "file=@mi_factura.jpg" http://localhost:5000/api/process-invoice
```

## ❓ Problemas Comunes

### Backend no arranca
- ¿Python 3.7+? → `python3 --version`
- ¿Tesseract instalado? → `tesseract --version`

### App no se conecta
- ¿Backend corriendo? → Abre `http://localhost:5000/health` en navegador
- ¿URL correcta? → Revisa IP en `main.dart`
- ¿Firewall? → Permite conexiones en puerto 5000

### OCR no funciona bien
- ✅ Usa fotos con buena iluminación
- ✅ Mantén la factura recta
- ✅ Evita sombras y reflejos
- ✅ Asegúrate que el texto esté en foco

## 📚 Más Información

- [README completo](README.md)
- [Documentación del Backend](backend/README.md)
- [API Reference](backend/README.md#-endpoints-api)

## 💡 Tips

- **Mejor calidad** → Mejores resultados
- **Luz natural** → Funciona mejor que flash
- **Fondos oscuros** → Contrastan mejor con papel blanco
- **Prueba primero** → Usa el endpoint `/health` para verificar

---

¿Algún problema? Revisa la [sección de troubleshooting](README.md#-solución-de-problemas) en el README principal.


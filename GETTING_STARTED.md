# 🎯 Comenzando - Guía Visual

## 📋 Checklist Rápido

Marca cada paso cuando lo completes:

- [ ] **Paso 1**: Instalar Tesseract
- [ ] **Paso 2**: Configurar Backend Python
- [ ] **Paso 3**: Configurar App Flutter
- [ ] **Paso 4**: Probar el sistema
- [ ] **Paso 5**: ¡Escanear tu primera factura!

---

## 🔧 Paso 1: Instalar Tesseract

### macOS 🍎
```bash
brew install tesseract tesseract-lang
```

### Linux 🐧
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

### Windows 🪟
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar
3. Agregar al PATH del sistema

### ✅ Verificar Instalación
```bash
tesseract --version
# Deberías ver algo como: tesseract 5.x.x

tesseract --list-langs
# Deberías ver 'spa' en la lista
```

---

## 🐍 Paso 2: Configurar Backend Python

### Opción A: Script Automático (Recomendado)
```bash
./start_backend.sh
```

### Opción B: Manual
```bash
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python app.py
```

### ✅ Verificar que funciona
En otra terminal:
```bash
curl http://localhost:5000/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "Invoice OCR Service",
  "version": "1.0.0"
}
```

---

## 📱 Paso 3: Configurar App Flutter

### 3.1 Instalar Dependencias
```bash
cd opencv
flutter pub get
```

### 3.2 Configurar URL del Backend

Edita `lib/main.dart` en la línea ~42:

**Para iOS Simulator:**
```dart
static const String backendUrl = 'http://localhost:5000';
```

**Para Android Emulator:**
```dart
static const String backendUrl = 'http://10.0.2.2:5000';
```

**Para Dispositivo Físico:**
```dart
static const String backendUrl = 'http://192.168.1.XXX:5000';
// Reemplaza XXX con la IP de tu computadora
```

**¿Cómo encontrar tu IP?**

macOS/Linux:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Windows:
```bash
ipconfig | findstr IPv4
```

### 3.3 Ejecutar App

**Automático:**
```bash
./start_flutter.sh
```

**Manual:**
```bash
flutter devices  # Ver dispositivos disponibles
flutter run      # Ejecutar en dispositivo por defecto
# o
flutter run -d <device-id>  # Ejecutar en dispositivo específico
```

---

## 🧪 Paso 4: Probar el Sistema

### Prueba 1: Health Check del Backend
```bash
curl http://localhost:5000/health
```
✅ Deberías ver: `"status": "healthy"`

### Prueba 2: Procesar una Factura de Prueba
```bash
cd backend
python test_api.py ruta/a/tu/factura.jpg
```

### Prueba 3: Usar la App Flutter
1. Abre la app en tu dispositivo
2. Presiona "Capturar con Cámara" o "Seleccionar de Galería"
3. Selecciona/captura una foto de factura
4. Presiona "Procesar Factura"
5. ¡Espera los resultados! 🎉

---

## 📸 Paso 5: Escanear tu Primera Factura

### Tips para Mejores Resultados

#### ✅ HACER
- Usar buena iluminación natural
- Mantener la factura plana y recta
- Enfocar bien el texto
- Usar fondo oscuro para contrastar
- Asegurarse que todo el texto sea visible

#### ❌ EVITAR
- Sombras sobre el documento
- Reflejos de luz
- Documentos arrugados
- Fotos borrosas o movidas
- Fondos muy iluminados

### Ejemplo de Captura Ideal

```
┌─────────────────────────────┐
│                             │
│  ┌─────────────────────┐   │ ← Borde de la cámara
│  │                     │   │
│  │     FACTURA         │   │ ← Documento centrado
│  │                     │   │
│  │  [texto legible]    │   │ ← Texto en foco
│  │                     │   │
│  └─────────────────────┘   │
│                             │
└─────────────────────────────┘
```

---

## 🎯 Casos de Uso

### 1. Autónomos y Freelancers
- Digitalizar facturas recibidas
- Extraer datos para contabilidad
- Archivar con metadatos

### 2. Pequeñas Empresas
- Procesamiento masivo de facturas
- Integración con software contable
- Reducir entrada manual de datos

### 3. Departamentos de Contabilidad
- Acelerar procesamiento de tickets
- Validar datos de facturas
- Auditoría y archivo digital

---

## 📊 Entendiendo los Resultados

La app te mostrará:

```
┌─────────────────────────────────────┐
│ ✅ Resultados del Análisis          │
├─────────────────────────────────────┤
│                                     │
│ 🎯 Confianza: 87.5%                │
│ ━━━━━━━━━━━━━━━━━━━                │
│                                     │
│ 📄 Número de Factura: F-2024-001   │
│ 📅 Fecha: 16/10/2024               │
│ 🏢 Proveedor: Empresa Ejemplo SL   │
│ 🆔 NIF/CIF: B12345678              │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 💰 Total: € 250.75              │ │ ← Destacado
│ └─────────────────────────────────┘ │
│                                     │
│ 📊 IVA: € 52.65                    │
│                                     │
└─────────────────────────────────────┘
```

### Indicador de Confianza

- 🟢 **80-100%**: Excelente - Datos muy confiables
- 🟡 **60-79%**: Bueno - Revisar datos importantes
- 🔴 **0-59%**: Bajo - Verificar todos los datos

---

## 🔧 Solución de Problemas

### ❌ "Backend no detectado"

**Problema**: La app no puede conectarse al backend.

**Soluciones**:
1. Verifica que el backend esté corriendo:
   ```bash
   curl http://localhost:5000/health
   ```
2. Revisa la URL en `main.dart`
3. Si usas dispositivo físico, usa la IP de tu computadora
4. Desactiva firewall temporalmente para probar

### ❌ "Error al procesar la factura"

**Problema**: El OCR no puede leer la imagen.

**Soluciones**:
1. Mejora la calidad de la foto:
   - Más luz
   - Mejor enfoque
   - Documento plano
2. Prueba con otra foto
3. Verifica que Tesseract tenga el idioma español:
   ```bash
   tesseract --list-langs
   ```

### ❌ "Confianza muy baja (<60%)"

**Problema**: El sistema no está seguro de los datos extraídos.

**Soluciones**:
1. Retoma la foto con mejores condiciones
2. Verifica que el texto sea legible
3. Asegúrate que sea una factura real (no un borrador)
4. Verifica que el idioma esté configurado correctamente

### ❌ "Tesseract no encontrado"

**Problema**: Python no encuentra Tesseract.

**Soluciones**:

**macOS/Linux**:
```bash
# Encontrar donde está instalado
which tesseract

# Agregar al PATH si es necesario
export PATH="/usr/local/bin:$PATH"
```

**Windows**:
1. Buscar donde instalaste Tesseract (usualmente `C:\Program Files\Tesseract-OCR`)
2. Agregar al PATH del sistema
3. Reiniciar terminal

---

## 📚 Próximos Pasos

Una vez que tengas todo funcionando:

1. **Lee la arquitectura**: [`ARCHITECTURE.md`](ARCHITECTURE.md)
2. **Explora ejemplos**: `backend/example_usage.py`
3. **Personaliza**: Ajusta patrones regex para tus necesidades
4. **Integra**: Conecta con tu sistema existente
5. **Contribuye**: Lee [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 💡 Recursos Adicionales

- 📖 **Documentación Completa**: [`README.md`](README.md)
- 🚀 **Inicio Rápido**: [`QUICKSTART.md`](QUICKSTART.md)
- 🏗️ **Arquitectura**: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- 🔌 **API del Backend**: [`backend/README.md`](backend/README.md)
- 🤝 **Contribuir**: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 🆘 ¿Necesitas Ayuda?

Si sigues teniendo problemas:

1. Revisa la [sección de troubleshooting](README.md#-solución-de-problemas)
2. Verifica que todos los requisitos estén instalados
3. Prueba los scripts de ejemplo: `backend/test_api.py`
4. Revisa los logs del backend para errores específicos

---

## 🎉 ¡Todo Listo!

Si llegaste hasta aquí y todo funciona:

**¡Felicitaciones! 🎊**

Ahora tienes tu propio sistema de procesamiento de facturas:
- ✅ Gratis y de código abierto
- ✅ Funciona localmente (privacidad)
- ✅ Personalizable a tus necesidades
- ✅ Similar a Amazon Textract

**¡Disfruta escaneando facturas! 📄✨**


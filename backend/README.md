# Backend OCR de Facturas 🧾

Sistema de procesamiento de facturas usando Tesseract + OpenCV similar a Amazon Textract.

## 📋 Requisitos Previos

### 1. Instalar Tesseract OCR

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang  # Para soporte de español
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-spa  # Para español
```

**Windows:**
- Descargar e instalar desde: https://github.com/UB-Mannheim/tesseract/wiki
- Agregar Tesseract al PATH del sistema

### 2. Verificar instalación de Tesseract

```bash
tesseract --version
tesseract --list-langs  # Debe mostrar 'spa' para español
```

## 🚀 Instalación

1. Crear entorno virtual:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar el servidor

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

## 📡 Endpoints API

### 1. Health Check
```
GET /health
```

### 2. Procesar Factura (Principal)
```
POST /api/process-invoice
Content-Type: multipart/form-data

Body:
  file: [imagen de la factura]

Response:
{
  "success": true,
  "invoice_data": {
    "invoice_number": "F-2024-001",
    "date": "15/10/2024",
    "total_amount": 150.50,
    "subtotal": 124.38,
    "tax": 26.12,
    "nif_cif": "B12345678",
    "vendor_name": "Empresa Ejemplo SL",
    "confidence": 85.5
  },
  "words": [...],  // Palabras con coordenadas
  "processing_info": {
    "total_words": 145,
    "average_confidence": 87.3
  }
}
```

### 3. Analizar Ticket/Recibo (Simplificado)
```
POST /api/analyze-receipt
Content-Type: multipart/form-data

Body:
  file: [imagen del ticket]
```

## 🧪 Probar con cURL

```bash
# Procesar factura
curl -X POST -F "file=@factura.jpg" http://localhost:5000/api/process-invoice

# Analizar ticket
curl -X POST -F "file=@ticket.jpg" http://localhost:5000/api/analyze-receipt
```

## 🔧 Características

- ✅ Preprocesamiento avanzado de imágenes con OpenCV
- ✅ Corrección automática de inclinación
- ✅ Reducción de ruido y mejora de contraste
- ✅ OCR optimizado para español
- ✅ Extracción estructurada de datos:
  - Número de factura
  - Fecha
  - Importes (total, subtotal, IVA)
  - NIF/CIF
  - Nombre del proveedor
- ✅ Coordenadas de palabras (similar a Textract)
- ✅ Métricas de confianza

## 📝 Notas

- El servidor acepta imágenes en formato JPG, PNG y PDF
- Tamaño máximo de archivo: 16MB
- Para mejores resultados, usar imágenes con buena iluminación y enfoque
- El sistema está optimizado para facturas en español


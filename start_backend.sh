#!/bin/bash

# Script para iniciar el backend de forma fácil
echo "🚀 Iniciando Backend de Procesamiento de Facturas..."
echo ""

# Ir al directorio del backend
cd backend

# Verificar que Tesseract esté instalado
if ! command -v tesseract &> /dev/null
then
    echo "❌ Error: Tesseract no está instalado"
    echo ""
    echo "Por favor, instálalo primero:"
    echo "  macOS:   brew install tesseract tesseract-lang"
    echo "  Linux:   sudo apt-get install tesseract-ocr tesseract-ocr-spa"
    echo "  Windows: https://github.com/UB-Mannheim/tesseract/wiki"
    exit 1
fi

echo "✅ Tesseract encontrado: $(tesseract --version | head -n 1)"
echo ""

# Verificar idioma español
if ! tesseract --list-langs 2>/dev/null | grep -q "spa"; then
    echo "⚠️  Advertencia: Idioma español no encontrado en Tesseract"
    echo "   Instálalo con: brew install tesseract-lang (macOS)"
    echo ""
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🔧 Activando entorno virtual..."
    source venv/bin/activate
else
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
    echo ""
fi

# Crear carpeta de uploads si no existe
mkdir -p uploads

# Verificar que todas las dependencias estén instaladas
echo "🔍 Verificando dependencias..."
python -c "import flask, cv2, pytesseract, numpy, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Faltan dependencias, instalando..."
    pip install -r requirements.txt
    echo ""
fi

echo "✅ Todo listo"
echo ""
echo "================================================"
echo "🌐 Iniciando servidor en http://localhost:5001"
echo "================================================"
echo ""
echo "Para probar el servidor:"
echo "  curl http://localhost:5001/health"
echo ""
echo "Para procesar una factura:"
echo "  curl -X POST -F \"file=@factura.jpg\" http://localhost:5001/api/process-invoice"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar el servidor
python app.py


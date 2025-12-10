#!/bin/bash

# Script para iniciar la app Flutter de forma fácil
echo "📱 Iniciando App Flutter - Escáner de Facturas"
echo ""

# Ir al directorio de Flutter
cd opencv

# Verificar que Flutter esté instalado
if ! command -v flutter &> /dev/null
then
    echo "❌ Error: Flutter no está instalado"
    echo ""
    echo "Por favor, instálalo desde: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "✅ Flutter encontrado: $(flutter --version | head -n 1)"
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias de Flutter..."
flutter pub get
echo ""

# Verificar dispositivos disponibles
echo "📱 Dispositivos disponibles:"
flutter devices
echo ""

# Verificar que el backend esté corriendo
echo "🔍 Verificando backend..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend está corriendo"
else
    echo "⚠️  Backend no detectado en http://localhost:5000"
    echo "   Por favor, inicia el backend primero:"
    echo "   ./start_backend.sh"
    echo ""
    echo "   O si quieres usar otra URL, edita lib/main.dart"
    echo ""
fi

echo "================================================"
echo "🚀 Iniciando aplicación Flutter..."
echo "================================================"
echo ""
echo "Si tienes múltiples dispositivos, selecciona uno cuando se te solicite"
echo ""

# Iniciar Flutter
flutter run


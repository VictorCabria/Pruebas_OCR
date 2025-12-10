#!/usr/bin/env python3
"""
Ejemplo de uso del sistema de procesamiento de facturas
Este script muestra cómo usar el API programáticamente
"""
import requests
import json
from pathlib import Path

# URL del backend
BACKEND_URL = 'http://localhost:5000'

def check_backend():
    """Verifica que el backend esté corriendo"""
    try:
        response = requests.get(f'{BACKEND_URL}/health')
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
            print(f"   {response.json()}")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend")
        print(f"   Asegúrate de que esté corriendo en {BACKEND_URL}")
        return False

def process_invoice(image_path):
    """
    Procesa una factura y retorna los datos extraídos
    
    Args:
        image_path: Ruta a la imagen de la factura
        
    Returns:
        Diccionario con los datos de la factura o None si hay error
    """
    if not Path(image_path).exists():
        print(f"❌ Archivo no encontrado: {image_path}")
        return None
    
    print(f"\n📄 Procesando: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f'{BACKEND_URL}/api/process-invoice',
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor tardó demasiado en responder")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_results(data):
    """Muestra los resultados de forma legible"""
    if not data or not data.get('success'):
        print("❌ No se pudieron extraer datos de la factura")
        return
    
    invoice = data['invoice_data']
    
    print("\n" + "="*60)
    print("📊 DATOS EXTRAÍDOS DE LA FACTURA")
    print("="*60)
    
    # Información principal
    if invoice.get('vendor_name'):
        print(f"\n🏢 Proveedor: {invoice['vendor_name']}")
    
    if invoice.get('nif_cif'):
        print(f"🆔 NIF/CIF: {invoice['nif_cif']}")
    
    if invoice.get('invoice_number'):
        print(f"📄 Número de Factura: {invoice['invoice_number']}")
    
    if invoice.get('date'):
        print(f"📅 Fecha: {invoice['date']}")
    
    # Importes
    print("\n💰 IMPORTES:")
    if invoice.get('subtotal'):
        print(f"   Base imponible: {invoice['subtotal']:.2f} €")
    
    if invoice.get('tax'):
        print(f"   IVA: {invoice['tax']:.2f} €")
    
    if invoice.get('total_amount'):
        print(f"   ✨ TOTAL: {invoice['total_amount']:.2f} €")
    
    # Confianza
    confidence = invoice.get('confidence', 0)
    confidence_emoji = "🟢" if confidence >= 80 else "🟡" if confidence >= 60 else "🔴"
    print(f"\n{confidence_emoji} Confianza: {confidence:.1f}%")
    
    # Información de procesamiento
    if 'processing_info' in data:
        info = data['processing_info']
        print(f"\n📊 Estadísticas:")
        print(f"   Palabras detectadas: {info.get('total_words', 0)}")
        print(f"   Confianza promedio: {info.get('average_confidence', 0):.1f}%")
    
    print("\n" + "="*60)

def save_to_json(data, output_path):
    """Guarda los resultados en formato JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Resultados guardados en: {output_path}")

def example_batch_processing(image_folder):
    """
    Ejemplo de procesamiento en lote
    
    Args:
        image_folder: Carpeta con imágenes de facturas
    """
    folder = Path(image_folder)
    if not folder.exists():
        print(f"❌ Carpeta no encontrada: {image_folder}")
        return
    
    # Buscar imágenes
    images = list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
    
    if not images:
        print(f"❌ No se encontraron imágenes en: {image_folder}")
        return
    
    print(f"\n🔄 Procesando {len(images)} facturas...")
    
    results = []
    for image in images:
        data = process_invoice(str(image))
        if data:
            results.append({
                'filename': image.name,
                'data': data['invoice_data']
            })
            print(f"   ✅ {image.name}")
        else:
            print(f"   ❌ {image.name}")
    
    # Guardar resultados del lote
    output_file = 'batch_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados del lote guardados en: {output_file}")
    
    # Resumen
    print(f"\n📊 Resumen:")
    print(f"   Total procesadas: {len(images)}")
    print(f"   Exitosas: {len(results)}")
    print(f"   Fallidas: {len(images) - len(results)}")

def main():
    """Ejemplo de uso completo"""
    print("🧾 Sistema de Procesamiento de Facturas")
    print("Ejemplo de Uso Programático\n")
    
    # 1. Verificar conexión
    if not check_backend():
        print("\n💡 Inicia el backend primero:")
        print("   python app.py")
        return
    
    # 2. Ejemplo básico: procesar una sola factura
    print("\n" + "="*60)
    print("EJEMPLO 1: Procesar una sola factura")
    print("="*60)
    
    # Aquí deberías poner la ruta a una factura de prueba
    image_path = 'test_invoice.jpg'
    
    data = process_invoice(image_path)
    if data:
        display_results(data)
        save_to_json(data, 'result.json')
    
    # 3. Ejemplo de procesamiento en lote (comentado)
    # print("\n" + "="*60)
    # print("EJEMPLO 2: Procesamiento en lote")
    # print("="*60)
    # example_batch_processing('facturas/')
    
    # 4. Integración en tu sistema
    print("\n" + "="*60)
    print("💡 INTEGRACIÓN EN TU SISTEMA")
    print("="*60)
    print("""
Para integrar este sistema en tu aplicación:

1. Importa la función process_invoice():
   from example_usage import process_invoice

2. Úsala para procesar facturas:
   data = process_invoice('ruta/a/factura.jpg')
   if data and data['success']:
       invoice = data['invoice_data']
       # Usa los datos extraídos
       print(f"Total: {invoice['total_amount']}")

3. Para casos de uso específicos:
   - Validar facturas antes de contabilizar
   - Extraer datos para entrada automática
   - Archivar digitalmente con metadatos
   - Integrar con sistemas ERP/contables
""")

if __name__ == '__main__':
    main()


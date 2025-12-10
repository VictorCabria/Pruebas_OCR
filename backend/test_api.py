#!/usr/bin/env python3
"""
Script de prueba para el API de procesamiento de facturas
"""
import requests
import sys
import json

def test_health():
    """Prueba el endpoint de health check"""
    print("🔍 Probando health check...")
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Backend está funcionando correctamente")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend")
        print("   Asegúrate de que el servidor esté corriendo: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_process_invoice(image_path):
    """Prueba el endpoint de procesamiento de facturas"""
    print(f"\n📄 Procesando factura: {image_path}")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                'http://localhost:5000/api/process-invoice',
                files=files
            )
        
        if response.status_code == 200:
            print("✅ Factura procesada correctamente")
            data = response.json()
            
            print("\n📊 Resultados:")
            invoice_data = data.get('invoice_data', {})
            
            print(f"   Número: {invoice_data.get('invoice_number', 'No detectado')}")
            print(f"   Fecha: {invoice_data.get('date', 'No detectada')}")
            print(f"   Proveedor: {invoice_data.get('vendor_name', 'No detectado')}")
            print(f"   NIF/CIF: {invoice_data.get('nif_cif', 'No detectado')}")
            
            total = invoice_data.get('total_amount')
            if total:
                print(f"   Total: €{total:.2f}")
            
            tax = invoice_data.get('tax')
            if tax:
                print(f"   IVA: €{tax:.2f}")
            
            confidence = invoice_data.get('confidence', 0)
            print(f"\n   🎯 Confianza: {confidence:.1f}%")
            
            processing_info = data.get('processing_info', {})
            print(f"   📝 Palabras detectadas: {processing_info.get('total_words', 0)}")
            print(f"   ✨ Confianza promedio: {processing_info.get('average_confidence', 0):.1f}%")
            
            # Guardar respuesta completa
            with open('test_response.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Respuesta completa guardada en: test_response.json")
            
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {image_path}")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🧾 Test del Sistema de Procesamiento de Facturas\n")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        sys.exit(1)
    
    # Test 2: Procesar factura (si se proporciona una imagen)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not test_process_invoice(image_path):
            sys.exit(1)
    else:
        print("\n💡 Para probar el procesamiento de facturas, ejecuta:")
        print("   python test_api.py ruta/a/tu/factura.jpg")
    
    print("\n" + "=" * 50)
    print("✅ Todos los tests pasaron correctamente")

if __name__ == '__main__':
    main()


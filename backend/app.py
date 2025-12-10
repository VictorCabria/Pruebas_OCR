from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import re
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """
    Preprocesa la imagen para mejorar el OCR
    ENFOQUE RADICAL para facturas extremadamente problemáticas
    """
    # Paso 1: Upscaling OPTIMIZADO (4x para balance entre calidad y velocidad)
    h, w = image.shape[:2]
    upscaled = cv2.resize(image, (w*4, h*4), interpolation=cv2.INTER_CUBIC)
    
    # Paso 2: Convertir a escala de grises
    gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
    
    # Paso 3: Corrección de rotación ULTRA-AGRESIVA
    try:
        # Detectar líneas con parámetros ultra-sensibles
        edges = cv2.Canny(gray, 20, 80, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=30)
        
        if lines is not None:
            angles = []
            for line in lines:
                rho, theta = line[0]
                angle = theta * 180 / np.pi
                # Considerar líneas en un rango MUY amplio
                if -15 <= angle <= 15 or 165 <= angle <= 195:
                    angles.append(angle)
            
            if angles:
                avg_angle = np.mean(angles)
                if abs(avg_angle) > 0.1:  # Umbral ULTRA bajo
                    center = (w*4//2, h*4//2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, -avg_angle, 1.0)
                    gray = cv2.warpAffine(gray, rotation_matrix, (w*4, h*4))
    except:
        pass
    
    # Paso 4: ESTRATEGIA RADICAL de mejora de contraste
    # Aplicar CLAHE múltiples veces con diferentes parámetros
    clahe1 = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(4,4))
    enhanced1 = clahe1.apply(gray)
    
    clahe2 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(12,12))
    enhanced2 = clahe2.apply(gray)
    
    clahe3 = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(6,6))
    enhanced3 = clahe3.apply(gray)
    
    # Normalización de histograma
    enhanced4 = cv2.equalizeHist(gray)
    
    # Combinar TODAS las estrategias
    temp = cv2.addWeighted(enhanced1, 0.4, enhanced2, 0.3, 0)
    temp = cv2.addWeighted(temp, 0.7, enhanced3, 0.2, 0)
    enhanced = cv2.addWeighted(temp, 0.8, enhanced4, 0.1, 0)
    
    # Paso 5: Filtros de ruido ULTRA-AGRESIVOS
    # Aplicar filtros múltiples veces
    enhanced = cv2.bilateralFilter(enhanced, 15, 80, 80)
    enhanced = cv2.medianBlur(enhanced, 5)
    enhanced = cv2.bilateralFilter(enhanced, 9, 60, 60)
    
    # Paso 6: Sharpening EXTREMO
    kernel_sharpen = np.array([[-1,-1,-1,-1,-1,-1,-1],
                                [-1, 1, 1, 1, 1, 1,-1],
                                [-1, 1, 2, 2, 2, 1,-1],
                                [-1, 1, 2, 8, 2, 1,-1],
                                [-1, 1, 2, 2, 2, 1,-1],
                                [-1, 1, 1, 1, 1, 1,-1],
                                [-1,-1,-1,-1,-1,-1,-1]]) / 8.0
    sharpened = cv2.filter2D(enhanced, -1, kernel_sharpen)
    
    # Paso 7: Múltiples métodos de thresholding RADICALES
    # Método 1: Otsu
    _, thresh1 = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Método 2: Adaptativo ultra-agresivo
    thresh2 = cv2.adaptiveThreshold(
        sharpened, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        7,   # Tamaño de bloque MUY pequeño
        1    # Constante C mínima
    )
    
    # Método 3: Adaptativo por media
    thresh3 = cv2.adaptiveThreshold(
        sharpened, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    
    # Método 4: Threshold manual ultra-agresivo
    p10 = np.percentile(sharpened, 10)
    p90 = np.percentile(sharpened, 90)
    threshold_val = (p10 + p90) / 2
    _, thresh4 = cv2.threshold(sharpened, threshold_val, 255, cv2.THRESH_BINARY)
    
    # Método 5: Threshold muy bajo para capturar texto débil
    _, thresh5 = cv2.threshold(sharpened, 100, 255, cv2.THRESH_BINARY)
    
    # Método 6: Threshold muy alto para texto fuerte
    _, thresh6 = cv2.threshold(sharpened, 200, 255, cv2.THRESH_BINARY)
    
    # Combinar TODOS los métodos
    # Usar Otsu como base y mejorar con otros
    final = thresh1.copy()
    
    # Combinar con threshold adaptativo
    final = cv2.bitwise_and(final, thresh2)
    
    # Paso 8: Operaciones morfológicas ULTRA-AGRESIVAS
    # Cerrar huecos en letras
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    closed = cv2.morphologyEx(final, cv2.MORPH_CLOSE, kernel_close)
    
    # Eliminar ruido pequeño
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open)
    
    # Dilatar para fortalecer texto
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    final = cv2.dilate(opened, kernel_dilate, iterations=2)
    
    # Erosión final para limpiar
    kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    final = cv2.erode(final, kernel_erode, iterations=1)
    
    return final

def extract_invoice_data(text):
    """
    Extrae datos estructurados de la factura
    Similar a Amazon Textract pero personalizado para facturas españolas
    """
    data = {
        'raw_text': text,
        'invoice_number': None,
        'date': None,
        'total_amount': None,
        'currency': 'COP',  # Por defecto pesos colombianos
        'subtotal': None,
        'tax': None,
        'nif_cif': None,
        'vendor_name': None,
        'client_name': None,
        'email': None,
        'items': [],
        'confidence': 0
    }
    
    lines = text.split('\n')
    
    # Buscar número de factura (más flexible para facturas colombianas)
    invoice_patterns = [
        r'(?:factura|invoice|fact\.?|FACTURA|ELECTRONICA)\s*(?:n[úuº°]?\.?|number|#|NUM|No)?\s*:?\s*([A-Z0-9\-/]{3,})',
        r'(?:n[úuº°]?\.?|number|#|NUM|No)\s*(?:factura|invoice)?\s*:?\s*([A-Z0-9\-/]{3,})',
        r'FACTURA\s+ELECTRONICA\s+DE\s+VENTA\s+No\.?\s*([A-Z0-9\-]+)',  # KFC format
        r'FACTURA\s+ELECTRONICA\s*:?\s*([A-Z0-9]+)',
        r'C\d+-\d+',  # Formato KFC C168-152015
        r'F-\d{4}-\d+',  # Formato común F-2024-001
        r'[A-Z]{1,3}\d{8,}',  # Formato tipo AB12345678
    ]
    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.lastindex:
                data['invoice_number'] = match.group(1).strip()
            else:
                data['invoice_number'] = match.group(0).strip()
            break
    
    # Buscar fecha (mejorado para incluir hora)
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}\s+\d{1,2}:\d{2}:\d{2})',  # 9/10/2025 10:37:21
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}\s+\d{1,2}:\d{2})',  # 9/10/2025 10:37
        r'(?:fecha|date|FECHA)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',  # 9/10/2025
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2})',  # 9/10/25
        r'(\d{1,2}\s+(?:de\s+)?(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de\s+)?\d{4})'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['date'] = match.group(1).strip()
            break
    
    # Buscar NIF/CIF/NIT (mejorado para facturas colombianas)
    nif_patterns = [
        r'\b([A-Z]\d{7}[A-Z0-9]|\d{8}[A-Z])\b',  # Formato español
        r'NIT\s*:?\s*(\d{1,3}-\d{1,3})',  # Formato colombiano NIT: 901-2
        r'NIT\s*:?\s*(\d{6,12})',  # NIT sin guiones
        r'(\d{1,3}-\d{1,3})\s*(?:NIT|nit)',  # NIT al final
    ]
    for pattern in nif_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['nif_cif'] = match.group(1)
            break
    
    # Buscar total (mejorado para PESOS COLOMBIANOS con $)
    total_patterns = [
        r'(?:total|TOTAL|amount|IMPORTE)\s*:?\s*[$€]?\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',
        r'\$\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',  # $3,000 o $3.000
        r'(\d{1,3}(?:[.,]\d{3})+)\s*(?:COP|cop|pesos)?',  # 3,000 o 3.000
        r'TOTAL\s*:?\s*\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',  # KFC format
        r'(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})\s*[$€]?\s*(?:total|TOTAL)?',
        r'Total\s*:?\s*\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',  # Case sensitive
    ]
    
    found_amounts = []
    for pattern in total_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                # Normalizar el formato (pesos colombianos suelen usar . como separador de miles)
                amount_str = match.replace(' ', '').replace('$', '').strip()
                
                # Para pesos colombianos: punto como separador de miles, coma como decimal
                # Pero también puede ser al revés según la región
                if '.' in amount_str and ',' in amount_str:
                    # Si tiene ambos, el último es el decimal
                    if amount_str.rfind('.') > amount_str.rfind(','):
                        # punto es decimal: 1,000.50
                        amount_str = amount_str.replace(',', '')
                    else:
                        # coma es decimal: 1.000,50
                        amount_str = amount_str.replace('.', '').replace(',', '.')
                elif '.' in amount_str:
                    # Solo punto: puede ser miles o decimal
                    parts = amount_str.split('.')
                    if len(parts) == 2 and len(parts[1]) == 3:
                        # Es separador de miles: 3.000 -> 3000
                        amount_str = amount_str.replace('.', '')
                    # Si tiene 2 dígitos después del punto, es decimal
                elif ',' in amount_str:
                    # Solo coma: puede ser miles o decimal
                    parts = amount_str.split(',')
                    if len(parts) == 2 and len(parts[1]) == 3:
                        # Es separador de miles: 3,000 -> 3000
                        amount_str = amount_str.replace(',', '')
                    else:
                        # Es decimal
                        amount_str = amount_str.replace(',', '.')
                
                amount = float(amount_str)
                if 1 <= amount <= 999999999:  # Rango razonable para pesos colombianos
                    found_amounts.append(amount)
            except:
                continue
    
    if found_amounts:
        # El total suele ser el mayor valor
        data['total_amount'] = max(found_amounts)
        data['currency'] = 'COP'  # Pesos colombianos
    
    # Buscar IVA/Tax (mejorado para facturas colombianas)
    tax_patterns = [
        r'(?:IVA|VAT|tax)\s*(?:\d{1,2}%)?\s*:?\s*€?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
        r'IVA\s*19%\s*:?\s*\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',  # KFC format
        r'IVA\s*:?\s*\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})',
        r'(\d{1,3}(?:[.,]\d{3})*[.,]?\d{0,2})\s*\$?\s*(?:IVA|VAT)',
    ]
    for pattern in tax_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data['tax'] = float(match.group(1).replace(',', '.').replace('.', '', match.group(1).count('.')-1))
            break
    
    # Buscar EMAIL
    email_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'(?:email|correo|e-mail|EMAIL)\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
    ]
    for pattern in email_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.lastindex:
                data['email'] = match.group(1).strip().lower()
            else:
                data['email'] = match.group(0).strip().lower()
            break
    
    # Buscar CLIENTE (puede aparecer con etiqueta)
    client_patterns = [
        r'(?:cliente|client|CLIENTE)\s*:?\s*\d+\s*\n?\s*([A-Z][A-Za-z\s]{3,50})',
        r'(?:cliente|client|CLIENTE)\s*:?\s*([A-Z][A-Za-z\s]{3,50})',
        r'CLIENTE\s*:\s*\d+\s*\n([^\n]{5,50})',
    ]
    for pattern in client_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            client = match.group(1).strip()
            # Limpiar el nombre del cliente
            if len(client) > 3 and not any(x in client.lower() for x in ['factura', 'fecha', 'total', 'cif', 'nif']):
                data['client_name'] = client
                break
    
    # Si no se encontró cliente con patrón, buscar después de "CLIENTE:"
    if not data['client_name']:
        for i, line in enumerate(lines):
            if 'cliente' in line.lower() and ':' in line:
                # Buscar en las siguientes líneas
                for j in range(i+1, min(i+4, len(lines))):
                    candidate = lines[j].strip()
                    if len(candidate) > 3 and not candidate.isdigit():
                        data['client_name'] = candidate
                        break
                if data['client_name']:
                    break
    
    # Buscar nombre del vendedor/proveedor (primeras líneas no vacías)
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) > 5 and not any(keyword in line.lower() for keyword in ['factura', 'invoice', 'fecha', 'date', 'cliente', 'tel', 'email', 'cif', 'nif']):
            # Buscar líneas que parezcan nombres de empresa
            if any(x in line.upper() for x in ['SL', 'SA', 'S.L.', 'S.A.', 'SRL', 'LTDA']) or line[0].isupper():
                data['vendor_name'] = line
                break
    
    # Calcular confianza basada en datos encontrados
    found_fields = sum([
        1 if data['invoice_number'] else 0,
        1 if data['date'] else 0,
        1 if data['total_amount'] else 0,
        1 if data['nif_cif'] else 0,
        1 if data['vendor_name'] else 0,
        1 if data['client_name'] else 0,
        1 if data['email'] else 0,
    ])
    data['confidence'] = (found_fields / 7) * 100
    
    return data

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servicio está funcionando"""
    return jsonify({
        'status': 'healthy',
        'service': 'Invoice OCR Service',
        'version': '1.0.0'
    })

@app.route('/api/process-invoice', methods=['POST'])
def process_invoice():
    """
    Endpoint principal para procesar facturas
    Acepta una imagen y devuelve datos estructurados
    """
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró ningún archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de archivo no permitido'}), 400
        
        # Leer la imagen
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'No se pudo leer la imagen'}), 400
        
        # Preprocesar la imagen
        processed_image = preprocess_image(image)
        
        # Guardar imagen procesada para debugging (opcional)
        try:
            debug_filename = f"debug_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            debug_path = os.path.join(UPLOAD_FOLDER, debug_filename)
            cv2.imwrite(debug_path, processed_image)
            print(f"🔍 Imagen procesada guardada: {debug_path}")
        except:
            pass
        
        # Realizar OCR con configuraciones OPTIMIZADAS (solo las mejores)
        # Probar solo las configuraciones más efectivas para evitar timeouts
        configs = [
            # Configuraciones básicas más efectivas
            r'--oem 1 --psm 3 -l spa',  # Automático
            r'--oem 1 --psm 6 -l spa',  # Bloque uniforme (mejor para facturas)
            r'--oem 1 --psm 4 -l spa',  # Columna única
            r'--oem 1 --psm 8 -l spa',  # Palabra única
            
            # Configuraciones agresivas más efectivas
            r'--oem 3 --psm 3 -l spa',  # OEM 3 (más agresivo)
            r'--oem 3 --psm 6 -l spa',  # OEM 3 + bloque uniforme
            r'--oem 3 --psm 4 -l spa',  # OEM 3 + columna única
            
            # Sin idioma específico (más flexible)
            r'--oem 1 --psm 3',  # Sin idioma
            r'--oem 3 --psm 3',  # OEM 3 sin idioma
            r'--oem 1 --psm 6',  # Sin idioma + bloque
            r'--oem 3 --psm 6',  # OEM 3 sin idioma + bloque
        ]
        
        best_text = ""
        best_confidence = 0
        best_config = configs[0]
        
        print(f"🔍 Probando {len(configs)} configuraciones OPTIMIZADAS de OCR...")
        
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("OCR timeout")
        
        for i, config in enumerate(configs):
            try:
                # Configurar timeout de 10 segundos por configuración
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                temp_text = pytesseract.image_to_string(processed_image, config=config)
                temp_data = pytesseract.image_to_data(processed_image, config=config, output_type=pytesseract.Output.DICT)
                
                # Cancelar timeout
                signal.alarm(0)
                
                # Calcular confianza promedio
                confidences = [int(conf) for conf in temp_data['conf'] if conf != '-1']
                avg_conf = sum(confidences) / len(confidences) if confidences else 0
                
                # Sistema de scoring INTELIGENTE
                text_length = len(temp_text.strip())
                text_quality = text_length * 0.1
                
                # Bonus por palabras clave de facturas
                keywords = ['factura', 'total', 'iva', 'fecha', 'nit', 'cif', 'cliente', 'proveedor']
                keyword_bonus = sum([1 for keyword in keywords if keyword.lower() in temp_text.lower()]) * 5
                
                # Bonus por números (importante en facturas)
                numbers = len(re.findall(r'\d+', temp_text))
                number_bonus = numbers * 0.5
                
                # Bonus por símbolos de moneda
                currency_bonus = len(re.findall(r'[$€]', temp_text)) * 3
                
                # Penalización por texto muy corto o muy largo
                length_penalty = 0
                if text_length < 50:
                    length_penalty = -10
                elif text_length > 2000:
                    length_penalty = -5
                
                combined_score = avg_conf + text_quality + keyword_bonus + number_bonus + currency_bonus + length_penalty
                
                print(f"  Config {i+1:2d}: Conf={avg_conf:5.1f}%, Text={text_length:4d} chars, KW={keyword_bonus:2.0f}, Num={number_bonus:2.0f}, $={currency_bonus:2.0f}, Score={combined_score:6.1f}")
                
                if combined_score > best_confidence:
                    best_confidence = combined_score
                    best_text = temp_text
                    best_config = config
                    
            except TimeoutError:
                print(f"  Config {i+1:2d}: Timeout - saltando...")
                signal.alarm(0)  # Cancelar timeout
                continue
            except Exception as e:
                print(f"  Config {i+1:2d}: Error - {str(e)}")
                signal.alarm(0)  # Cancelar timeout
                continue
        
        text = best_text if best_text else pytesseract.image_to_string(processed_image, config=configs[0])
        print(f"✅ Mejor configuración: {best_config}")
        print(f"📊 Confianza final: {best_confidence:.1f}")
        print(f"📝 Texto extraído: {len(text)} caracteres")
        
        # Extraer datos estructurados
        invoice_data = extract_invoice_data(text)
        
        # También obtener datos con coordenadas (similar a Textract)
        ocr_data = pytesseract.image_to_data(processed_image, config=configs[0], output_type=pytesseract.Output.DICT)
        
        # Organizar palabras por líneas con coordenadas
        words_with_positions = []
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            if int(ocr_data['conf'][i]) > 30:  # Solo palabras con confianza > 30%
                words_with_positions.append({
                    'text': ocr_data['text'][i],
                    'confidence': float(ocr_data['conf'][i]),
                    'bounding_box': {
                        'x': int(ocr_data['left'][i]),
                        'y': int(ocr_data['top'][i]),
                        'width': int(ocr_data['width'][i]),
                        'height': int(ocr_data['height'][i])
                    }
                })
        
        response = {
            'success': True,
            'invoice_data': invoice_data,
            'words': words_with_positions,
            'processing_info': {
                'total_words': len(words_with_positions),
                'average_confidence': sum([w['confidence'] for w in words_with_positions]) / len(words_with_positions) if words_with_positions else 0
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-receipt', methods=['POST'])
def analyze_receipt():
    """
    Endpoint simplificado para tickets/recibos
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró ningún archivo'}), 400
        
        file = request.files['file']
        
        # Leer la imagen
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Preprocesar
        processed_image = preprocess_image(image)
        
        # OCR más agresivo para tickets
        custom_config = r'--oem 3 --psm 4 -l spa'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Extraer datos básicos
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Buscar total de manera más flexible
        total = None
        for line in lines:
            match = re.search(r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})', line)
            if match and ('total' in line.lower() or 'importe' in line.lower()):
                total = match.group(1)
                break
        
        return jsonify({
            'success': True,
            'text': text,
            'lines': lines,
            'total': total
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor de procesamiento de facturas...")
    print("📄 Similar a Amazon Textract pero con Tesseract + OpenCV")
    print("🌐 Servidor corriendo en http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)


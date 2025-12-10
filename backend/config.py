"""
Configuración del sistema de procesamiento de facturas
"""
import os

class Config:
    """Configuración base"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # Tesseract settings
    TESSERACT_LANG = 'spa'  # Idioma principal
    TESSERACT_CONFIG = r'--oem 3 --psm 6'
    
    # OCR confidence threshold
    MIN_CONFIDENCE = 30  # Palabras con confianza < 30% se descartan
    
    # Image processing
    BILATERAL_D = 9
    BILATERAL_SIGMA_COLOR = 75
    BILATERAL_SIGMA_SPACE = 75
    
    # Regex patterns para extracción
    INVOICE_NUMBER_PATTERNS = [
        r'(?:factura|invoice|fact\.?)\s*(?:n[úuº°]?\.?|number|#)?\s*:?\s*([A-Z0-9\-/]+)',
        r'(?:n[úuº°]?\.?|number|#)\s*(?:factura|invoice)?\s*:?\s*([A-Z0-9\-/]+)'
    ]
    
    DATE_PATTERNS = [
        r'(?:fecha|date)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}\s+(?:de\s+)?(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de\s+)?\d{4})'
    ]
    
    NIF_CIF_PATTERN = r'\b([A-Z]\d{7}[A-Z0-9]|\d{8}[A-Z])\b'
    
    AMOUNT_PATTERNS = [
        r'(?:total|amount)\s*:?\s*€?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
        r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})\s*€?\s*(?:total|amount)?'
    ]
    
    TAX_PATTERNS = [
        r'(?:IVA|VAT|tax)\s*(?:\d{1,2}%)?\s*:?\s*€?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})'
    ]

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    # En producción, usar variables de entorno
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Configuración para tests"""
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = 'test_uploads'

# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env='default'):
    """Obtiene la configuración según el entorno"""
    return config.get(env, config['default'])


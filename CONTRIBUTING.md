# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Escaneo de Facturas!

## 🎯 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no esté ya reportado en Issues
2. Crea un nuevo Issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Screenshots si es aplicable
   - Información del entorno (OS, versiones, etc.)

### Sugerir Mejoras

1. Abre un Issue describiendo:
   - La funcionalidad propuesta
   - Por qué sería útil
   - Ejemplos de uso

### Pull Requests

1. **Fork** el repositorio
2. **Crea** una rama para tu feature: `git checkout -b feature/mi-feature`
3. **Implementa** tus cambios
4. **Asegúrate** de que todo funcione:
   ```bash
   # Backend
   python test_api.py
   
   # Flutter
   flutter test
   ```
5. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "feat: agregar extracción de productos de factura"
   ```
6. **Push** a tu fork: `git push origin feature/mi-feature`
7. **Abre** un Pull Request

## 📝 Estándares de Código

### Python (Backend)

- Seguir PEP 8
- Usar type hints cuando sea posible
- Documentar funciones con docstrings
- Máximo 88 caracteres por línea (Black formatter)

```python
def extract_invoice_data(text: str) -> dict:
    """
    Extrae datos estructurados de la factura.
    
    Args:
        text: Texto extraído por OCR
        
    Returns:
        Diccionario con datos de la factura
    """
    pass
```

### Dart/Flutter (App)

- Seguir las guías de estilo de Dart
- Usar widgets const cuando sea posible
- Nombres descriptivos para variables y funciones
- Comentar código complejo

```dart
/// Procesa la imagen de la factura y envía al backend
Future<void> _processInvoice() async {
  // Implementation
}
```

## 🧪 Tests

### Backend

```bash
cd backend
python -m pytest tests/
```

### Flutter

```bash
cd opencv
flutter test
```

## 📚 Áreas de Mejora

Buscamos contribuciones en:

- ✅ **OCR**: Mejorar precisión de extracción
- ✅ **UI/UX**: Mejorar interfaz de usuario
- ✅ **Idiomas**: Agregar soporte para más idiomas
- ✅ **Documentación**: Mejorar guías y ejemplos
- ✅ **Tests**: Aumentar cobertura de tests
- ✅ **Performance**: Optimizar procesamiento
- ✅ **Features**: Nuevas funcionalidades

## 🎨 Convenciones de Commits

Usamos Conventional Commits:

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, sin cambios en código
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests
- `chore:` - Mantenimiento

Ejemplos:
```
feat: agregar soporte para múltiples idiomas
fix: corregir detección de fechas en formato DD/MM/YYYY
docs: actualizar guía de instalación para Windows
```

## 🔍 Code Review

Todos los PRs serán revisados para:

- Funcionalidad correcta
- Tests apropiados
- Documentación actualizada
- Código limpio y mantenible
- Sin conflictos con main

## 📞 Contacto

¿Tienes preguntas? Abre un Issue con la etiqueta `question`.

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones sean licenciadas bajo la misma licencia del proyecto (MIT).

---

¡Gracias por hacer este proyecto mejor! 🎉


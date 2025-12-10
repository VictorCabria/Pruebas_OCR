import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Escáner de Facturas',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const InvoiceScannerPage(),
    );
  }
}

class InvoiceScannerPage extends StatefulWidget {
  const InvoiceScannerPage({super.key});

  @override
  State<InvoiceScannerPage> createState() => _InvoiceScannerPageState();
}

class _InvoiceScannerPageState extends State<InvoiceScannerPage> {
  File? _selectedImage;
  bool _isProcessing = false;
  Map<String, dynamic>? _invoiceData;
  String? _errorMessage;
  final ImagePicker _picker = ImagePicker();

  // Configura aquí la URL de tu backend
  // Para desarrollo en dispositivo físico, usa la IP de tu computadora
  // Para emulador Android: usa 10.0.2.2
  // Para iOS Simulator: usa localhost o 127.0.0.1
  static const String backendUrl = 'http://192.168.1.14:5001';

  Future<void> _pickImageFromGallery() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
      );

      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          _invoiceData = null;
          _errorMessage = null;
        });
      }
    } catch (e) {
      _showError('Error al seleccionar imagen: $e');
    }
  }

  Future<void> _takePhoto() async {
    try {
      final XFile? photo = await _picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 85,
      );

      if (photo != null) {
        setState(() {
          _selectedImage = File(photo.path);
          _invoiceData = null;
          _errorMessage = null;
        });
      }
    } catch (e) {
      _showError('Error al tomar foto: $e');
    }
  }

  Future<void> _processInvoice() async {
    if (_selectedImage == null) {
      _showError('Por favor selecciona una imagen primero');
      return;
    }

    setState(() {
      _isProcessing = true;
      _errorMessage = null;
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$backendUrl/api/process-invoice'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          _selectedImage!.path,
        ),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _invoiceData = data['invoice_data'];
          _isProcessing = false;
        });
      } else {
        final error = json.decode(response.body);
        _showError(error['error'] ?? 'Error al procesar la factura');
        setState(() {
          _isProcessing = false;
        });
      }
    } catch (e) {
      _showError('Error de conexión: $e\n\nAsegúrate de que el backend esté corriendo en $backendUrl');
      setState(() {
        _isProcessing = false;
      });
    }
  }

  void _showError(String message) {
    setState(() {
      _errorMessage = message;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red.shade700,
        duration: const Duration(seconds: 4),
      ),
    );
  }

  void _reset() {
    setState(() {
      _selectedImage = null;
      _invoiceData = null;
      _errorMessage = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          '🧾 Escáner de Facturas',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        actions: [
          if (_selectedImage != null || _invoiceData != null)
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: _reset,
              tooltip: 'Nueva factura',
            ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Tarjeta de imagen
              _buildImageCard(),
              const SizedBox(height: 20),

              // Botones de acción
              if (_selectedImage == null) _buildActionButtons(),

              // Botón de procesar
              if (_selectedImage != null && _invoiceData == null)
                _buildProcessButton(),

              // Resultados
              if (_invoiceData != null) _buildResults(),

              // Mensaje de error
              if (_errorMessage != null) _buildErrorMessage(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildImageCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        height: 400,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.deepPurple.shade50,
              Colors.blue.shade50,
            ],
          ),
        ),
        child: _selectedImage == null
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.receipt_long,
                      size: 80,
                      color: Colors.deepPurple.shade200,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Selecciona o captura una factura',
                      style: TextStyle(
                        fontSize: 18,
                        color: Colors.grey.shade600,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              )
            : ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.file(
                  _selectedImage!,
                  fit: BoxFit.contain,
                ),
              ),
      ),
    );
  }

  Widget _buildActionButtons() {
    return Column(
      children: [
        ElevatedButton.icon(
          onPressed: _takePhoto,
          icon: const Icon(Icons.camera_alt, size: 28),
          label: const Text(
            'Capturar con Cámara',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            backgroundColor: Colors.deepPurple,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        const SizedBox(height: 12),
        OutlinedButton.icon(
          onPressed: _pickImageFromGallery,
          icon: const Icon(Icons.photo_library, size: 28),
          label: const Text(
            'Seleccionar de Galería',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            side: const BorderSide(color: Colors.deepPurple, width: 2),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildProcessButton() {
    return ElevatedButton.icon(
      onPressed: _isProcessing ? null : _processInvoice,
      icon: _isProcessing
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: Colors.white,
              ),
            )
          : const Icon(Icons.document_scanner, size: 28),
      label: Text(
        _isProcessing ? 'Procesando...' : 'Procesar Factura',
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16),
        backgroundColor: Colors.green.shade600,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }

  Widget _buildResults() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.check_circle, color: Colors.green.shade600, size: 28),
                const SizedBox(width: 12),
                const Text(
                  'Resultados del Análisis',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Confianza
            if (_invoiceData!['confidence'] != null)
              _buildConfidenceIndicator(_invoiceData!['confidence']),

            const SizedBox(height: 20),

            // Datos extraídos
            _buildDataField('Número de Factura', _invoiceData!['invoice_number'], Icons.numbers),
            _buildDataField('Fecha', _invoiceData!['date'], Icons.calendar_today),
            _buildDataField('Proveedor', _invoiceData!['vendor_name'], Icons.business),
            _buildDataField('Cliente', _invoiceData!['client_name'], Icons.person),
            _buildDataField('Email', _invoiceData!['email'], Icons.email),
            _buildDataField('NIF/CIF', _invoiceData!['nif_cif'], Icons.badge),
            
            if (_invoiceData!['total_amount'] != null)
              _buildDataField(
                'Total',
                '\$ ${_invoiceData!['total_amount'].toStringAsFixed(0)}',
                Icons.attach_money,
                isHighlighted: true,
              ),

            if (_invoiceData!['tax'] != null)
              _buildDataField(
                'IVA',
                '\$ ${_invoiceData!['tax'].toStringAsFixed(0)}',
                Icons.percent,
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildConfidenceIndicator(double confidence) {
    Color getColor() {
      if (confidence >= 80) return Colors.green;
      if (confidence >= 60) return Colors.orange;
      return Colors.red;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Confianza',
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.grey,
              ),
            ),
            Text(
              '${confidence.toStringAsFixed(1)}%',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: getColor(),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: LinearProgressIndicator(
            value: confidence / 100,
            minHeight: 8,
            backgroundColor: Colors.grey.shade200,
            valueColor: AlwaysStoppedAnimation<Color>(getColor()),
          ),
        ),
      ],
    );
  }

  Widget _buildDataField(String label, String? value, IconData icon, {bool isHighlighted = false}) {
    if (value == null || value.isEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isHighlighted ? Colors.green.shade50 : Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isHighlighted ? Colors.green.shade200 : Colors.grey.shade200,
          width: isHighlighted ? 2 : 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            icon,
            color: isHighlighted ? Colors.green.shade700 : Colors.deepPurple.shade400,
            size: 24,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: isHighlighted ? 20 : 16,
                    fontWeight: isHighlighted ? FontWeight.bold : FontWeight.w600,
                    color: Colors.black87,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorMessage() {
    return Card(
      color: Colors.red.shade50,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red.shade700, size: 28),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                _errorMessage!,
                style: TextStyle(
                  color: Colors.red.shade700,
                  fontSize: 14,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

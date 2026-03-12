class ApiClient {
  ApiClient({required this.baseUrl});

  final String baseUrl;

  Uri uri(String path) => Uri.parse('$baseUrl$path');
}

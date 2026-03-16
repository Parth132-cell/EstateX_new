import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({required this.baseUrl, http.Client? httpClient}) : _httpClient = httpClient ?? http.Client();

  final String baseUrl;
  final http.Client _httpClient;

  Uri uri(String path, [Map<String, dynamic>? queryParameters]) {
    return Uri.parse('$baseUrl$path').replace(
      queryParameters: queryParameters?.map((key, value) => MapEntry(key, '$value')),
    );
  }

  Future<Map<String, dynamic>> getJson(String path, {Map<String, dynamic>? queryParameters}) async {
    final response = await _httpClient.get(uri(path, queryParameters)).timeout(const Duration(seconds: 5));
    _ensureSuccess(response);
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> getJsonList(String path, {Map<String, dynamic>? queryParameters}) async {
    final response = await _httpClient.get(uri(path, queryParameters)).timeout(const Duration(seconds: 5));
    _ensureSuccess(response);
    final decoded = jsonDecode(response.body);
    if (decoded is List<dynamic>) {
      return decoded;
    }
    if (decoded is Map<String, dynamic> && decoded['results'] is List<dynamic>) {
      return decoded['results'] as List<dynamic>;
    }
    throw const FormatException('Expected list response');
  }

  Future<Map<String, dynamic>> postJson(String path, Map<String, dynamic> payload) async {
    final response = await _httpClient
        .post(
          uri(path),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload),
        )
        .timeout(const Duration(seconds: 5));
    _ensureSuccess(response);
    if (response.body.isEmpty) {
      return <String, dynamic>{};
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  void _ensureSuccess(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return;
    }
    throw HttpException('Request failed (${response.statusCode}): ${response.body}');
  }
}

class HttpException implements Exception {
  const HttpException(this.message);

  final String message;

  @override
  String toString() => message;
}

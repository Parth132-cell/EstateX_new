class NegotiationEntry {
  const NegotiationEntry({required this.message});

  final String message;

  factory NegotiationEntry.fromJson(Map<String, dynamic> json) {
    final amount = json['amount'];
    final actor = json['from_user'] ?? json['actor'] ?? 'Unknown';
    final text = json['message'] ?? '';
    return NegotiationEntry(message: '$actor: ₹$amount ${text.toString().trim()}'.trim());
  }
}

class PropertyListing {
  const PropertyListing({
    required this.id,
    required this.title,
    required this.city,
    required this.price,
    required this.bhk,
    required this.description,
    required this.verified,
  });

  final int id;
  final String title;
  final String city;
  final int price;
  final int bhk;
  final String description;
  final bool verified;

  factory PropertyListing.fromJson(Map<String, dynamic> json) {
    return PropertyListing(
      id: json['id'] as int,
      title: (json['title'] ?? '') as String,
      city: (json['city'] ?? '') as String,
      price: (json['price'] ?? 0) as int,
      bhk: (json['bhk'] ?? 0) as int,
      description: (json['description'] ?? '') as String,
      verified: (json['verification_status'] ?? '') == 'verified' || (json['verified'] ?? false) == true,
    );
  }
}

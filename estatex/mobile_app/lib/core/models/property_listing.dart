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
}

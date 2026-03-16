import 'package:flutter/material.dart';

import '../models/property_listing.dart';

class AppState extends ChangeNotifier {
  String? userName;
  String userRole = 'buyer';
  bool kycSubmitted = false;

  String cityFilter = 'All';
  int maxPriceFilter = 30000000;
  int? bhkFilter;

  final List<PropertyListing> _listings = const [
    PropertyListing(
      id: 1,
      title: 'Skyline Residency',
      city: 'Mumbai',
      price: 18500000,
      bhk: 3,
      description: 'Sea-view apartment near business district.',
      verified: true,
    ),
    PropertyListing(
      id: 2,
      title: 'Green Valley Homes',
      city: 'Pune',
      price: 9800000,
      bhk: 2,
      description: 'Family-friendly gated community with clubhouse.',
      verified: true,
    ),
    PropertyListing(
      id: 3,
      title: 'Palm Enclave',
      city: 'Bengaluru',
      price: 13400000,
      bhk: 3,
      description: 'Tech-corridor villa project with high rental demand.',
      verified: false,
    ),
  ];

  final Map<int, List<String>> offers = {};
  final Map<int, String> paymentStatus = {};
  final Map<int, String> tourStatus = {};

  List<PropertyListing> get filteredListings {
    return _listings.where((listing) {
      final cityMatch = cityFilter == 'All' || listing.city == cityFilter;
      final priceMatch = listing.price <= maxPriceFilter;
      final bhkMatch = bhkFilter == null || listing.bhk == bhkFilter;
      return cityMatch && priceMatch && bhkMatch;
    }).toList();
  }

  PropertyListing? listingById(int id) {
    for (final listing in _listings) {
      if (listing.id == id) return listing;
    }
    return null;
  }

  void login({required String name, required String role}) {
    userName = name;
    userRole = role;
    notifyListeners();
  }

  void submitKyc() {
    kycSubmitted = true;
    notifyListeners();
  }

  void applyFilters({required String city, required int maxPrice, int? bhk}) {
    cityFilter = city;
    maxPriceFilter = maxPrice;
    bhkFilter = bhk;
    notifyListeners();
  }

  void createOffer(int listingId, int amount) {
    final thread = offers.putIfAbsent(listingId, () => []);
    thread.add('You offered ₹$amount');
    thread.add('AI suggestion: Try ₹${(amount * 0.97).round()} for better acceptance chance.');
    notifyListeners();
  }

  void createCounter(int listingId, int amount) {
    final thread = offers.putIfAbsent(listingId, () => []);
    thread.add('Counter offer sent: ₹$amount');
    notifyListeners();
  }

  void createOrder(int listingId) {
    paymentStatus[listingId] = 'order_created';
    notifyListeners();
  }

  void holdFunds(int listingId) {
    paymentStatus[listingId] = 'funds_held';
    notifyListeners();
  }

  void releaseFunds(int listingId) {
    paymentStatus[listingId] = 'released';
    notifyListeners();
  }

  void scheduleTour(int listingId) {
    tourStatus[listingId] = 'scheduled';
    notifyListeners();
  }

  void joinTour(int listingId) {
    tourStatus[listingId] = 'live';
    notifyListeners();
  }
}

class AppStateScope extends InheritedNotifier<AppState> {
  const AppStateScope({required super.notifier, required super.child, super.key});

  static AppState of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AppStateScope>();
    assert(scope != null, 'AppStateScope not found in widget tree.');
    return scope!.notifier!;
  }
}

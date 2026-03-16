import 'package:flutter/material.dart';

import '../models/property_listing.dart';
import '../repositories/estatex_repository.dart';

class AppState extends ChangeNotifier {
  AppState({required EstateXRepository repository}) : _repository = repository;

  final EstateXRepository _repository;

  String? userName;
  String userRole = 'buyer';
  bool kycSubmitted = false;
  bool isLoadingListings = false;
  String? listingError;

  String cityFilter = 'All';
  int maxPriceFilter = 30000000;
  int? bhkFilter;

  List<PropertyListing> _listings = const [];

  final Map<int, List<String>> offers = {};
  final Map<int, String> paymentStatus = {};
  final Map<int, String> paymentReference = {};
  final Map<int, String> tourStatus = {};

  List<PropertyListing> get filteredListings {
    return _listings.where((listing) {
      final cityMatch = cityFilter == 'All' || listing.city == cityFilter;
      final priceMatch = listing.price <= maxPriceFilter;
      final bhkMatch = bhkFilter == null || listing.bhk == bhkFilter;
      return cityMatch && priceMatch && bhkMatch;
    }).toList();
  }

  Future<void> loadListings() async {
    isLoadingListings = true;
    listingError = null;
    notifyListeners();
    try {
      _listings = await _repository.fetchListings(city: cityFilter, maxPrice: maxPriceFilter, bhk: bhkFilter);
    } catch (_) {
      listingError = 'Could not load live listings. Showing offline sample data.';
      _listings = _fallbackListings;
    }
    isLoadingListings = false;
    notifyListeners();
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

  Future<void> applyFilters({required String city, required int maxPrice, int? bhk}) async {
    cityFilter = city;
    maxPriceFilter = maxPrice;
    bhkFilter = bhk;
    notifyListeners();
    await loadListings();
  }

  Future<void> loadOfferHistory(int listingId) async {
    try {
      final history = await _repository.fetchOfferHistory(listingId);
      offers[listingId] = history.map((e) => e.message).toList();
      notifyListeners();
    } catch (_) {
      offers.putIfAbsent(listingId, () => []);
      notifyListeners();
    }
  }

  Future<void> createOffer(int listingId, int amount) async {
    final thread = offers.putIfAbsent(listingId, () => []);
    thread.add('You offered ₹$amount');
    thread.add('AI suggestion: Try ₹${(amount * 0.97).round()} for better acceptance chance.');
    notifyListeners();
    try {
      await _repository.createOffer(
        listingId: listingId,
        fromUser: userName ?? 'Buyer',
        toUser: 'Seller',
        amount: amount,
      );
    } catch (_) {
      thread.add('Server sync pending.');
      notifyListeners();
    }
  }

  Future<void> createCounter(int listingId, int amount) async {
    final thread = offers.putIfAbsent(listingId, () => []);
    thread.add('Counter offer sent: ₹$amount');
    notifyListeners();
    try {
      await _repository.createCounter(
        listingId: listingId,
        fromUser: userName ?? 'Buyer',
        toUser: 'Seller',
        amount: amount,
      );
    } catch (_) {
      thread.add('Server sync pending.');
      notifyListeners();
    }
  }

  Future<void> createOrder(int listingId) async {
    paymentStatus[listingId] = 'order_created';
    paymentReference[listingId] = 'manual_ref_$listingId';
    notifyListeners();
    try {
      await _repository.createEscrowOrder(
        listingId: listingId,
        buyerId: 1001,
        sellerId: 2001,
        amount: listingById(listingId)?.price ?? 0,
      );
    } catch (_) {
      // fallback keeps local state
    }
  }

  Future<void> holdFunds(int listingId) async {
    paymentStatus[listingId] = 'funds_held';
    notifyListeners();
    final reference = paymentReference[listingId];
    if (reference == null) return;
    try {
      await _repository.holdEscrow(providerReference: reference);
    } catch (_) {
      // fallback keeps local state
    }
  }

  Future<void> releaseFunds(int listingId) async {
    paymentStatus[listingId] = 'released';
    notifyListeners();
    final reference = paymentReference[listingId];
    if (reference == null) return;
    try {
      await _repository.releaseEscrow(providerReference: reference);
    } catch (_) {
      // fallback keeps local state
    }
  }

  Future<void> scheduleTour(int listingId) async {
    tourStatus[listingId] = 'scheduled';
    notifyListeners();
    try {
      await _repository.scheduleTour(listingId: listingId, hostId: 3001);
    } catch (_) {
      // fallback keeps local state
    }
  }

  void joinTour(int listingId) {
    tourStatus[listingId] = 'live';
    notifyListeners();
  }
}

const List<PropertyListing> _fallbackListings = [
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

class AppStateScope extends InheritedNotifier<AppState> {
  const AppStateScope({required super.notifier, required super.child, super.key});

  static AppState of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AppStateScope>();
    assert(scope != null, 'AppStateScope not found in widget tree.');
    return scope!.notifier!;
  }
}

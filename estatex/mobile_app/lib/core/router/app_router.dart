import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/ar_preview/presentation/screens/ar_preview_screen.dart';
import '../../features/auth/presentation/screens/login_signup_screen.dart';
import '../../features/broker_dashboard/presentation/screens/broker_dashboard_screen.dart';
import '../../features/escrow/presentation/screens/escrow_payment_screen.dart';
import '../../features/kyc/presentation/screens/kyc_upload_screen.dart';
import '../../features/negotiation/presentation/screens/offer_negotiation_screen.dart';
import '../../features/property_detail/presentation/screens/property_detail_screen.dart';
import '../../features/property_feed/presentation/screens/property_feed_screen.dart';
import '../../features/search_filters/presentation/screens/search_filters_screen.dart';
import '../../features/video_tour/presentation/screens/video_tour_screen.dart';

class AppRouter {
  static final router = GoRouter(
    initialLocation: '/auth',
    routes: [
      GoRoute(path: '/auth', builder: (_, __) => const LoginSignupScreen()),
      GoRoute(path: '/kyc', builder: (_, __) => const KycUploadScreen()),
      GoRoute(path: '/feed', builder: (_, __) => const PropertyFeedScreen()),
      GoRoute(
        path: '/detail/:id',
        builder: (_, state) => PropertyDetailScreen(listingId: int.parse(state.pathParameters['id']!)),
      ),
      GoRoute(path: '/filters', builder: (_, __) => const SearchFiltersScreen()),
      GoRoute(
        path: '/tour/:id',
        builder: (_, state) => VideoTourScreen(listingId: int.parse(state.pathParameters['id']!)),
      ),
      GoRoute(
        path: '/negotiation/:id',
        builder: (_, state) => OfferNegotiationScreen(listingId: int.parse(state.pathParameters['id']!)),
      ),
      GoRoute(
        path: '/escrow/:id',
        builder: (_, state) => EscrowPaymentScreen(listingId: int.parse(state.pathParameters['id']!)),
      ),
      GoRoute(
        path: '/ar/:id',
        builder: (_, state) => ARInteriorPreviewScreen(listingId: int.parse(state.pathParameters['id']!)),
      ),
      GoRoute(path: '/broker', builder: (_, __) => const BrokerDashboardScreen()),
    ],
    errorBuilder: (_, __) => const Scaffold(
      body: Center(child: Text('Route not found')),
    ),
  );
}

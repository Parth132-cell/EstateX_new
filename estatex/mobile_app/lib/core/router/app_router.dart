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
      GoRoute(path: '/detail', builder: (_, __) => const PropertyDetailScreen()),
      GoRoute(path: '/filters', builder: (_, __) => const SearchFiltersScreen()),
      GoRoute(path: '/tour', builder: (_, __) => const VideoTourScreen()),
      GoRoute(path: '/negotiation', builder: (_, __) => const OfferNegotiationScreen()),
      GoRoute(path: '/escrow', builder: (_, __) => const EscrowPaymentScreen()),
      GoRoute(path: '/ar', builder: (_, __) => const ARInteriorPreviewScreen()),
      GoRoute(path: '/broker', builder: (_, __) => const BrokerDashboardScreen()),
    ],
    errorBuilder: (_, __) => const Scaffold(
      body: Center(child: Text('Route not found')),
    ),
  );
}

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppNavigationDrawer extends StatelessWidget {
  const AppNavigationDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        children: [
          const DrawerHeader(child: Text('EstateX Navigation')),
          _item(context, 'Property Feed', '/feed'),
          _item(context, 'KYC Upload', '/kyc'),
          _item(context, 'Search Filters', '/filters'),
          _item(context, 'Broker Dashboard', '/broker'),
        ],
      ),
    );
  }

  Widget _item(BuildContext context, String label, String route) {
    return ListTile(
      title: Text(label),
      onTap: () {
        context.pop();
        context.go(route);
      },
    );
  }
}

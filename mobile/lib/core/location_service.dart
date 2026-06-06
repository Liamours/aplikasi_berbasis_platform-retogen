import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';

class LocationCoordinates {
  final double latitude;
  final double longitude;

  const LocationCoordinates({
    required this.latitude,
    required this.longitude,
  });

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
    };
  }
}

class LocationService {
  const LocationService._();

  static Future<LocationCoordinates?> getCurrentCoordinates() async {
    try {
      final serviceEnabled = await Geolocator.isLocationServiceEnabled()
          .timeout(const Duration(seconds: 4));
      debugPrint('Retogen location: serviceEnabled=$serviceEnabled');
      if (!serviceEnabled) return null;

      var permission = await Geolocator.checkPermission()
          .timeout(const Duration(seconds: 4));
      debugPrint('Retogen location: permission=$permission');
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission()
            .timeout(const Duration(seconds: 8));
        debugPrint('Retogen location: requestedPermission=$permission');
      }

      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever ||
          permission == LocationPermission.unableToDetermine) {
        return null;
      }

      final position = await Geolocator.getCurrentPosition(
        locationSettings: AndroidSettings(
          accuracy: LocationAccuracy.high,
          timeLimit: const Duration(seconds: 15),
        ),
      );
      debugPrint(
        'Retogen location: current=${position.latitude}, ${position.longitude}',
      );

      return LocationCoordinates(
        latitude: position.latitude,
        longitude: position.longitude,
      );
    } on TimeoutException {
      debugPrint('Retogen location: timeout');
      return _getLastKnownCoordinates();
    } catch (error) {
      debugPrint('Retogen location: failed=$error');
      return _getLastKnownCoordinates();
    }
  }

  static Future<LocationCoordinates?> _getLastKnownCoordinates() async {
    try {
      final lastKnown = await Geolocator.getLastKnownPosition(
        forceAndroidLocationManager: true,
      ).timeout(const Duration(seconds: 3));

      if (lastKnown == null) return null;

      final age = DateTime.now().difference(lastKnown.timestamp).abs();
      debugPrint('Retogen location: lastKnownAge=${age.inSeconds}s');
      if (age > const Duration(minutes: 2)) {
        debugPrint('Retogen location: lastKnownIgnored=stale');
        return null;
      }

      debugPrint(
        'Retogen location: lastKnown=${lastKnown.latitude}, ${lastKnown.longitude}',
      );
      return LocationCoordinates(
        latitude: lastKnown.latitude,
        longitude: lastKnown.longitude,
      );
    } catch (error) {
      debugPrint('Retogen location: lastKnownFailed=$error');
      return null;
    }
  }
}

import 'dart:async';

import 'package:geolocator/geolocator.dart';

class MonitorLocation {
  final String location;

  const MonitorLocation({required this.location});

  Map<String, dynamic> toJson() {
    return {'location': location};
  }
}

class _LocationBounds {
  final String location;
  final double minLat;
  final double maxLat;
  final double minLng;
  final double maxLng;

  const _LocationBounds({
    required this.location,
    required this.minLat,
    required this.maxLat,
    required this.minLng,
    required this.maxLng,
  });

  bool contains(double latitude, double longitude) {
    return latitude >= minLat &&
        latitude <= maxLat &&
        longitude >= minLng &&
        longitude <= maxLng;
  }
}

class LocationService {
  const LocationService._();

  static const _bounds = [
    _LocationBounds(
      location: 'Jakarta Pusat',
      minLat: -6.23,
      maxLat: -6.12,
      minLng: 106.78,
      maxLng: 106.88,
    ),
    _LocationBounds(
      location: 'Jakarta Barat',
      minLat: -6.25,
      maxLat: -6.10,
      minLng: 106.68,
      maxLng: 106.82,
    ),
    _LocationBounds(
      location: 'Jakarta Selatan',
      minLat: -6.38,
      maxLat: -6.20,
      minLng: 106.73,
      maxLng: 106.90,
    ),
    _LocationBounds(
      location: 'Jakarta Utara',
      minLat: -6.18,
      maxLat: -6.08,
      minLng: 106.74,
      maxLng: 106.98,
    ),
    _LocationBounds(
      location: 'Jakarta Timur',
      minLat: -6.35,
      maxLat: -6.15,
      minLng: 106.85,
      maxLng: 107.02,
    ),
    _LocationBounds(
      location: 'Bandung',
      minLat: -6.95,
      maxLat: -6.84,
      minLng: 107.55,
      maxLng: 107.74,
    ),
    _LocationBounds(
      location: 'Kab. Bandung',
      minLat: -7.18,
      maxLat: -6.95,
      minLng: 107.50,
      maxLng: 107.95,
    ),
    _LocationBounds(
      location: 'Surabaya',
      minLat: -7.36,
      maxLat: -7.18,
      minLng: 112.60,
      maxLng: 112.86,
    ),
    _LocationBounds(
      location: 'Tangerang',
      minLat: -6.30,
      maxLat: -6.05,
      minLng: 106.55,
      maxLng: 106.75,
    ),
    _LocationBounds(
      location: 'Bekasi',
      minLat: -6.38,
      maxLat: -6.12,
      minLng: 106.95,
      maxLng: 107.10,
    ),
    _LocationBounds(
      location: 'Depok',
      minLat: -6.48,
      maxLat: -6.30,
      minLng: 106.73,
      maxLng: 106.90,
    ),
    _LocationBounds(
      location: 'Bogor',
      minLat: -6.70,
      maxLat: -6.50,
      minLng: 106.70,
      maxLng: 106.90,
    ),
  ];

  static Future<MonitorLocation?> getCurrentLocation() async {
    try {
      final serviceEnabled = await Geolocator.isLocationServiceEnabled()
          .timeout(const Duration(seconds: 4));
      if (!serviceEnabled) return null;

      var permission = await Geolocator.checkPermission().timeout(
        const Duration(seconds: 4),
      );
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission().timeout(
          const Duration(seconds: 8),
        );
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

      return _resolveLocation(position.latitude, position.longitude);
    } on TimeoutException {
      return _getLastKnownLocation();
    } catch (_) {
      return _getLastKnownLocation();
    }
  }

  static Future<MonitorLocation?> _getLastKnownLocation() async {
    try {
      final lastKnown = await Geolocator.getLastKnownPosition(
        forceAndroidLocationManager: true,
      ).timeout(const Duration(seconds: 3));

      if (lastKnown == null) return null;

      final age = DateTime.now().difference(lastKnown.timestamp).abs();
      if (age > const Duration(minutes: 2)) {
        return null;
      }

      return _resolveLocation(lastKnown.latitude, lastKnown.longitude);
    } catch (_) {
      return null;
    }
  }

  static MonitorLocation? _resolveLocation(double latitude, double longitude) {
    for (final bound in _bounds) {
      if (bound.contains(latitude, longitude)) {
        return MonitorLocation(location: bound.location);
      }
    }

    return null;
  }
}

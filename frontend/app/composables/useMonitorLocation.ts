type CoordinateLocation = {
  location: string
  minLat: number
  maxLat: number
  minLng: number
  maxLng: number
}

const LOCATION_BOUNDS: CoordinateLocation[] = [
  { location: 'Jakarta Pusat', minLat: -6.23, maxLat: -6.12, minLng: 106.78, maxLng: 106.88 },
  { location: 'Jakarta Barat', minLat: -6.25, maxLat: -6.10, minLng: 106.68, maxLng: 106.82 },
  { location: 'Jakarta Selatan', minLat: -6.38, maxLat: -6.20, minLng: 106.73, maxLng: 106.90 },
  { location: 'Jakarta Utara', minLat: -6.18, maxLat: -6.08, minLng: 106.74, maxLng: 106.98 },
  { location: 'Jakarta Timur', minLat: -6.35, maxLat: -6.15, minLng: 106.85, maxLng: 107.02 },
  { location: 'Bandung', minLat: -6.95, maxLat: -6.84, minLng: 107.55, maxLng: 107.74 },
  { location: 'Kab. Bandung', minLat: -7.18, maxLat: -6.95, minLng: 107.50, maxLng: 107.95 },
  { location: 'Surabaya', minLat: -7.36, maxLat: -7.18, minLng: 112.60, maxLng: 112.86 },
  { location: 'Tangerang', minLat: -6.30, maxLat: -6.05, minLng: 106.55, maxLng: 106.75 },
  { location: 'Bekasi', minLat: -6.38, maxLat: -6.12, minLng: 106.95, maxLng: 107.10 },
  { location: 'Depok', minLat: -6.48, maxLat: -6.30, minLng: 106.73, maxLng: 106.90 },
  { location: 'Bogor', minLat: -6.70, maxLat: -6.50, minLng: 106.70, maxLng: 106.90 }
]

function resolveMonitorLocation(latitude: number, longitude: number) {
  return LOCATION_BOUNDS.find((item) =>
    latitude >= item.minLat &&
    latitude <= item.maxLat &&
    longitude >= item.minLng &&
    longitude <= item.maxLng
  )?.location ?? null
}

function requestBrowserPosition() {
  return new Promise<GeolocationPosition | null>((resolve) => {
    if (!import.meta.client || !navigator.geolocation) {
      resolve(null)
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => resolve(position),
      () => resolve(null),
      {
        enableHighAccuracy: false,
        maximumAge: 10 * 60 * 1000,
        timeout: 6000
      }
    )
  })
}

export const useMonitorLocation = () => {
  const cachedLocation = useState<string | null>('monitor-location', () => null)
  const hasRequestedLocation = useState('monitor-location-requested', () => false)

  async function getMonitorLocation() {
    if (cachedLocation.value || hasRequestedLocation.value) {
      return cachedLocation.value
    }

    hasRequestedLocation.value = true
    const position = await requestBrowserPosition()
    if (!position) return null

    cachedLocation.value = resolveMonitorLocation(
      position.coords.latitude,
      position.coords.longitude
    )

    return cachedLocation.value
  }

  return {
    getMonitorLocation
  }
}

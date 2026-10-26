const client = require('prom-client');

// Khởi tạo Prometheus Registry
const register = new client.Registry();

// Bật các metric mặc định của Node.js (CPU, Memory, Event Loop, GC)
client.collectDefaultMetrics({
  register,
  prefix: 'hotel_'
});

// Custom Metrics: HTTP Request Counter
const httpRequestCounter = new client.Counter({
  name: 'hotel_http_requests_total',
  help: 'Total number of HTTP requests processed by Hotel App',
  labelNames: ['method', 'route', 'status_code']
});
register.registerMetric(httpRequestCounter);

// Custom Metrics: HTTP Request Duration Histogram
const httpRequestDuration = new client.Histogram({
  name: 'hotel_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
});
register.registerMetric(httpRequestDuration);

// Custom Metrics: Hotel Business Metrics
const roomStatusGauge = new client.Gauge({
  name: 'hotel_rooms_count',
  help: 'Number of hotel rooms by type and status',
  labelNames: ['type', 'status']
});
register.registerMetric(roomStatusGauge);

const bookingStatusGauge = new client.Gauge({
  name: 'hotel_bookings_count',
  help: 'Number of bookings by status',
  labelNames: ['status']
});
register.registerMetric(bookingStatusGauge);

const hotelRevenueGauge = new client.Gauge({
  name: 'hotel_revenue_vnd',
  help: 'Total hotel booking revenue in VND'
});
register.registerMetric(hotelRevenueGauge);

module.exports = {
  register,
  httpRequestCounter,
  httpRequestDuration,
  roomStatusGauge,
  bookingStatusGauge,
  hotelRevenueGauge
};

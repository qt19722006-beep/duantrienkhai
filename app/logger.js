const fs = require('fs');
const path = require('path');

const logDir = process.env.LOG_DIR || path.join(__dirname, 'logs');
if (!fs.existsSync(logDir)) {
  try {
    fs.mkdirSync(logDir, { recursive: true });
  } catch (err) {
    console.error('Could not create log directory:', err.message);
  }
}

const logFilePath = path.join(logDir, 'hotel-app.log');

function writeLog(level, message, meta = {}) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level,
    service: 'hotel-app',
    message,
    ...meta
  };

  const line = JSON.stringify(logEntry) + '\n';
  
  // Ghi ra stdout/stderr cho docker logs
  if (level === 'error') {
    process.stderr.write(line);
  } else {
    process.stdout.write(line);
  }

  // Ghi ra file log để Promtail thu thập trực tiếp
  try {
    fs.appendFileSync(logFilePath, line, 'utf8');
  } catch (err) {
    // ignore append failure if running restricted
  }
}

const logger = {
  info: (msg, meta) => writeLog('info', msg, meta),
  warn: (msg, meta) => writeLog('warn', msg, meta),
  error: (msg, meta) => writeLog('error', msg, meta),
  debug: (msg, meta) => writeLog('debug', msg, meta)
};

module.exports = logger;

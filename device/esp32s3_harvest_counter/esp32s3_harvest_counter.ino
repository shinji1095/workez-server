#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClient.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <time.h>

#include "config.h"

// ---------------------------
// Constants
// ---------------------------
static const char *kLogDir = "/log";
static const char *kPrefsNs = "harvest_dev";
static const uint32_t kDebugAdcIntervalMs = 500;
static const uint32_t kHttpTimeoutMs = 15000;

// ---------------------------
// Config
// ---------------------------
struct Config {
  String wifi_ssid;
  String wifi_pass;

  String server_base_url;  // e.g. http://192.168.1.10
  String api_path;         // e.g. /api/harvest/amount/add
  String jwt_token;
  String token_url;        // e.g. http://192.168.1.10/api/auth/token
  String api_key;          // device API key for token issuance

  String device_id;
  String category_id;

  uint32_t send_interval_sec = 600;
  bool debug = true;
  bool log_to_file = false;

  int adc_pin = A0;
  uint32_t sample_interval_ms = 25;

  int threshold_high = 1800;
  int threshold_low = 1600;
  uint32_t min_presence_ms = 50;
  uint32_t min_gap_ms = 500;

  float ema_alpha = 0.2f;

  bool ntp_enabled = true;
  String ntp_server = "pool.ntp.org";
  int tz_offset_minutes = 540; // JST
};

enum class DetectState {
  IDLE,
  CANDIDATE,
  IN_OBJECT,
  COOLDOWN
};

// ---------------------------
// Globals
// ---------------------------
Config g_cfg;
Preferences g_prefs;

File g_log;
String g_log_path;

DetectState g_state = DetectState::IDLE;

uint32_t g_last_sample_ms = 0;
uint32_t g_candidate_start_ms = 0;
uint32_t g_cooldown_until_ms = 0;

float g_filtered = 0.0f;
int g_last_adc_raw = 0;

uint32_t g_last_send_ms = 0;
uint32_t g_last_debug_adc_ms = 0;

// Pending counter stored in NVS
uint32_t g_pending_count = 0;

// Wi-Fi connection state
static const uint32_t kWifiConnectTimeoutMs = 20000;

// ---------------------------
// Logging
// ---------------------------
static void logLine(const String &level, const String &msg) {
  String line;
  // Use time if valid; else fallback to millis.
  time_t now = time(nullptr);
  if (now > 1700000000) {
    struct tm tm_local;
    localtime_r(&now, &tm_local);
    char buf[32];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm_local);
    line = String(buf) + " [" + level + "] " + msg + "\n";
  } else {
    line = String(millis()) + "ms [" + level + "] " + msg + "\n";
  }

  if (g_cfg.log_to_file && g_log) {
    g_log.print(line);
    g_log.flush();
  }

  if (g_cfg.debug) {
    Serial.print(line);
  }
}

static String iso8601Now(int tz_offset_minutes) {
  time_t now = time(nullptr);
  struct tm tm_local;
  localtime_r(&now, &tm_local);

  char ts[32];
  // "YYYY-MM-DDTHH:MM:SS"
  strftime(ts, sizeof(ts), "%Y-%m-%dT%H:%M:%S", &tm_local);

  int off = tz_offset_minutes;
  char sign = '+';
  if (off < 0) { sign = '-'; off = -off; }
  int hh = off / 60;
  int mm = off % 60;

  char tz[8];
  snprintf(tz, sizeof(tz), "%c%02d:%02d", sign, hh, mm);

  return String(ts) + String(tz);
}

static bool timeIsValid() {
  return (time(nullptr) > 1700000000);
}

// Minimal JSON string escaper for payloads.
static String jsonEscape(const String &s) {
  String out;
  out.reserve(s.length() + 8);
  for (size_t i = 0; i < s.length(); i++) {
    char c = s[i];
    switch (c) {
      case '\\': out += "\\\\"; break;
      case '"': out += "\\\""; break;
      case '\n': out += "\\n"; break;
      case '\r': out += "\\r"; break;
      case '\t': out += "\\t"; break;
      default: out += c; break;
    }
  }
  return out;
}

static String extractJsonString(const String &json, const char *key) {
  String pattern = String("\"") + key + "\":\"";
  int start = json.indexOf(pattern);
  if (start < 0) return "";
  start += pattern.length();
  int end = json.indexOf('"', start);
  if (end < 0) return "";
  return json.substring(start, end);
}

// ---------------------------
// UUID v4 (pseudo) generator
// ---------------------------
static String genUuidV4() {
  uint8_t b[16];
  for (int i = 0; i < 16; i++) {
    b[i] = (uint8_t)(esp_random() & 0xFF);
  }
  // Set version to 4
  b[6] = (b[6] & 0x0F) | 0x40;
  // Set variant to RFC 4122
  b[8] = (b[8] & 0x3F) | 0x80;

  char out[37];
  snprintf(out, sizeof(out),
           "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",
           b[0], b[1], b[2], b[3],
           b[4], b[5],
           b[6], b[7],
           b[8], b[9],
           b[10], b[11], b[12], b[13], b[14], b[15]);
  return String(out);
}

static bool fetchAccessToken() {
  if (g_cfg.token_url.length() == 0 || g_cfg.api_key.length() == 0) {
    logLine("WARNING", "Token fetch skipped: token_url/api_key missing.");
    return false;
  }
  if (WiFi.status() != WL_CONNECTED) {
    logLine("WARNING", "Token fetch skipped: WiFi not connected.");
    return false;
  }

  String body = "{\"sub\":\"" + jsonEscape(g_cfg.device_id) + "\"}";

  WiFiClient client;
  HTTPClient http;
  http.begin(client, g_cfg.token_url.c_str());
  http.setTimeout(kHttpTimeoutMs);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-KEY", g_cfg.api_key);

  logLine("INFO", "POST " + g_cfg.token_url + " (token)");
  int code = http.POST((uint8_t*)body.c_str(), body.length());
  String resp = http.getString();
  http.end();

  if (code != 200) {
    logLine("WARNING", "Token fetch failed. HTTP " + String(code) + " resp=" + resp);
    return false;
  }

  String token = extractJsonString(resp, "access_token");
  if (token.length() == 0) {
    logLine("WARNING", "Token parse failed.");
    return false;
  }

  g_cfg.jwt_token = token;
  logLine("INFO", "Access token updated.");
  return true;
}

static int postHarvestRequest(const String &url, const String &body, String &resp) {
  WiFiClient client;
  HTTPClient http;
  http.begin(client, url.c_str());
  http.setTimeout(kHttpTimeoutMs);
  http.addHeader("Content-Type", "application/json");
  if (g_cfg.jwt_token.length() > 0) {
    http.addHeader("Authorization", String("Bearer ") + g_cfg.jwt_token);
  }

  int code = http.POST((uint8_t*)body.c_str(), body.length());
  resp = http.getString();
  http.end();
  return code;
}

// ---------------------------
// Header Config
// ---------------------------
static void loadConfigFromHeader(Config &out) {
  out.wifi_ssid = CONFIG_WIFI_SSID;
  out.wifi_pass = CONFIG_WIFI_PASS;
  out.server_base_url = CONFIG_SERVER_BASE_URL;
  out.api_path = CONFIG_API_PATH;
  out.jwt_token = CONFIG_JWT_TOKEN;
  out.token_url = CONFIG_TOKEN_URL;
  out.api_key = CONFIG_API_KEY;
  out.device_id = CONFIG_DEVICE_ID;
  out.category_id = CONFIG_CATEGORY_ID;

  out.send_interval_sec = CONFIG_SEND_INTERVAL_SEC;
  out.debug = CONFIG_DEBUG;
  out.log_to_file = CONFIG_LOG_TO_FILE;

  out.adc_pin = CONFIG_ADC_PIN;
  out.sample_interval_ms = CONFIG_SAMPLE_INTERVAL_MS;

  out.threshold_high = CONFIG_THRESHOLD_HIGH;
  out.threshold_low = CONFIG_THRESHOLD_LOW;
  out.min_presence_ms = CONFIG_MIN_PRESENCE_MS;
  out.min_gap_ms = CONFIG_MIN_GAP_MS;

  out.ema_alpha = CONFIG_EMA_ALPHA;

  out.ntp_enabled = CONFIG_NTP_ENABLED;
  out.ntp_server = CONFIG_NTP_SERVER;
  out.tz_offset_minutes = CONFIG_TZ_OFFSET_MINUTES;
}

// ---------------------------
// Log file setup
// ---------------------------
static void openLogFile() {
  if (!g_cfg.log_to_file) {
    return;
  }
  if (!LittleFS.exists(kLogDir)) {
    LittleFS.mkdir(kLogDir);
  }

  String name;
  if (timeIsValid()) {
    time_t now = time(nullptr);
    struct tm tm_local;
    localtime_r(&now, &tm_local);
    char buf[32];
    strftime(buf, sizeof(buf), "%Y%m%d_%H%M%S", &tm_local);
    name = String(buf);
  } else {
    name = String("boot_") + String(millis());
  }

  g_log_path = String(kLogDir) + "/" + name + ".log";
  g_log = LittleFS.open(g_log_path, "a");
}

// ---------------------------
// Wi-Fi + NTP
// ---------------------------
static void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  WiFi.mode(WIFI_STA);
  WiFi.persistent(false);
  // Cancel any in-flight connection attempt to avoid "sta is connecting" errors.
  WiFi.disconnect(true);
  delay(100);
  if (g_cfg.debug) {
    logLine("INFO", "WiFi creds ssid=" + g_cfg.wifi_ssid + " pass=" + g_cfg.wifi_pass);
  }
  WiFi.begin(g_cfg.wifi_ssid.c_str(), g_cfg.wifi_pass.c_str());

  logLine("INFO", "WiFi connecting...");
  const uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - start) < kWifiConnectTimeoutMs) {
    delay(200);
  }

  if (WiFi.status() == WL_CONNECTED) {
    logLine("INFO", "WiFi connected. IP=" + WiFi.localIP().toString());
  } else {
    logLine("WARNING", "WiFi connect timeout.");
    WiFi.disconnect(true);
  }
}

static void setupNtpIfEnabled() {
  if (!g_cfg.ntp_enabled) return;
  if (WiFi.status() != WL_CONNECTED) return;

  // tz handled by offset at formatting time; localtime still needs tz env on ESP32
  // Set TZ to fixed offset (no DST)
  // Example: JST-9 means UTC+9
  // POSIX TZ format: "JST-9"
  char tzbuf[16];
  int off_h = g_cfg.tz_offset_minutes / 60;
  snprintf(tzbuf, sizeof(tzbuf), "JST-%d", off_h);
  setenv("TZ", tzbuf, 1);
  tzset();

  configTime(0, 0, g_cfg.ntp_server.c_str());

  logLine("INFO", "NTP syncing...");
  const uint32_t start = millis();
  while (!timeIsValid() && (millis() - start) < 15000) {
    delay(200);
  }

  if (timeIsValid()) {
    logLine("INFO", "NTP sync OK.");
  } else {
    logLine("WARNING", "NTP sync failed. Upload will be held until time becomes valid.");
  }
}

// ---------------------------
// Detection
// ---------------------------
static int readAdcRaw() {
  int raw = analogRead(g_cfg.adc_pin);
  return raw;
}

static void updateDetector(uint32_t now_ms, float filtered) {
  switch (g_state) {
    case DetectState::IDLE: {
      if ((int)filtered >= g_cfg.threshold_high) {
        g_state = DetectState::CANDIDATE;
        g_candidate_start_ms = now_ms;
        logLine("INFO", "Candidate start. adc=" + String((int)filtered));
      }
      break;
    }
    case DetectState::CANDIDATE: {
      if ((int)filtered < g_cfg.threshold_low) {
        g_state = DetectState::IDLE;
        break;
      }
      if ((now_ms - g_candidate_start_ms) >= g_cfg.min_presence_ms) {
        g_state = DetectState::IN_OBJECT;
        logLine("INFO", "Object detected. adc=" + String((int)filtered));
      }
      break;
    }
    case DetectState::IN_OBJECT: {
      if ((int)filtered <= g_cfg.threshold_low) {
        // Object passed
        g_pending_count += 1;
        g_prefs.putUInt("pending_count", g_pending_count);

        logLine("INFO", "Pass counted. pending_count=" + String(g_pending_count));

        g_state = DetectState::COOLDOWN;
        g_cooldown_until_ms = now_ms + g_cfg.min_gap_ms;
      }
      break;
    }
    case DetectState::COOLDOWN: {
      if (now_ms >= g_cooldown_until_ms) {
        g_state = DetectState::IDLE;
      }
      break;
    }
  }
}

// ---------------------------
// Upload
// ---------------------------
static bool postHarvestDiff(uint32_t count_to_send) {
  if (WiFi.status() != WL_CONNECTED) {
    logLine("WARNING", "Upload skipped: WiFi not connected.");
    return false;
  }
  if (!timeIsValid()) {
    logLine("WARNING", "Upload skipped: time invalid.");
    return false;
  }
  if (count_to_send == 0) {
    return true;
  }

  String url = g_cfg.server_base_url + g_cfg.api_path;

  String body = "{";
  body += "\"event_id\":\"" + jsonEscape(genUuidV4()) + "\",";
  body += "\"device_id\":\"" + jsonEscape(g_cfg.device_id) + "\",";
  body += "\"category_id\":\"" + jsonEscape(g_cfg.category_id) + "\",";
  body += "\"count\":" + String((int)count_to_send) + ",";
  body += "\"occurred_at\":\"" + jsonEscape(iso8601Now(g_cfg.tz_offset_minutes)) + "\"";
  body += "}";

  logLine("INFO", "POST " + url + " body=" + body);

  if (g_cfg.jwt_token.length() == 0) {
    if (!fetchAccessToken()) {
      logLine("WARNING", "Upload skipped: access token missing.");
      return false;
    }
  }

  String resp;
  int code = postHarvestRequest(url, body, resp);
  if (code == 401) {
    logLine("WARNING", "Unauthorized. Refreshing access token...");
    if (fetchAccessToken()) {
      code = postHarvestRequest(url, body, resp);
    }
  }

  logLine("INFO", "HTTP " + String(code) + " resp=" + resp);

  // 201: success, 409: duplicate (idempotency)
  if (code == 201 || code == 200 || code == 409) {
    return true;
  }
  return false;
}

// ---------------------------
// Setup / Loop
// ---------------------------
void setup() {
  Serial.begin(115200);
  delay(200);

  loadConfigFromHeader(g_cfg);

  if (g_cfg.log_to_file) {
    if (!LittleFS.begin(true)) {
      Serial.println("LittleFS mount failed. File logging disabled.");
      g_cfg.log_to_file = false;
    }
  }

  g_prefs.begin(kPrefsNs, false);
  g_pending_count = g_prefs.getUInt("pending_count", 0);

  // ADC settings
  analogReadResolution(12); // 0..4095
  pinMode(g_cfg.adc_pin, INPUT);

  // Start Wi-Fi early
  connectWiFi();
  setupNtpIfEnabled();
  fetchAccessToken();

  // Open log after time sync attempt (filename prefers time)
  openLogFile();
  if (g_cfg.log_to_file) {
    logLine("INFO", "Boot. log=" + g_log_path);
  }
  logLine("INFO", "pending_count restored=" + String(g_pending_count));

  // Initialize filter
  int raw = readAdcRaw();
  g_last_adc_raw = raw;
  g_filtered = (float)raw;

  g_last_sample_ms = millis();
  g_last_send_ms = millis();
  g_last_debug_adc_ms = millis();
}

void loop() {
  const uint32_t now_ms = millis();

  // Keep Wi-Fi
  if (WiFi.status() != WL_CONNECTED) {
    static uint32_t last_retry_ms = 0;
    if (now_ms - last_retry_ms > 5000) {
      last_retry_ms = now_ms;
      connectWiFi();
      setupNtpIfEnabled();
    }
  } else {
    // If time invalid, keep trying NTP occasionally
    if (g_cfg.ntp_enabled && !timeIsValid()) {
      static uint32_t last_ntp_retry_ms = 0;
      if (now_ms - last_ntp_retry_ms > 15000) {
        last_ntp_retry_ms = now_ms;
        setupNtpIfEnabled();
      }
    }
  }

  // Sampling
  if (now_ms - g_last_sample_ms >= g_cfg.sample_interval_ms) {
    g_last_sample_ms = now_ms;

    int raw = readAdcRaw();
    g_last_adc_raw = raw;
    g_filtered = g_cfg.ema_alpha * (float)raw + (1.0f - g_cfg.ema_alpha) * g_filtered;

    if (g_cfg.debug) {
      // Light debug; comment out if too noisy
      // logLine("DEBUG", "adc_raw=" + String(raw) + " filtered=" + String((int)g_filtered));
    }

    updateDetector(now_ms, g_filtered);
  }

  // Debug ADC output at fixed interval.
  if (g_cfg.debug && (now_ms - g_last_debug_adc_ms >= kDebugAdcIntervalMs)) {
    g_last_debug_adc_ms = now_ms;
    logLine("DEBUG", "adc_raw=" + String(g_last_adc_raw) + " filtered=" + String((int)g_filtered));
  }

  // Periodic upload
  const uint32_t interval_ms = g_cfg.send_interval_sec * 1000UL;
  if (now_ms - g_last_send_ms >= interval_ms) {
    g_last_send_ms = now_ms;

    uint32_t to_send = g_pending_count;
    if (to_send == 0) {
      logLine("INFO", "No diff to upload.");
    } else {
      bool ok = postHarvestDiff(to_send);
      if (ok) {
        g_pending_count = 0;
        g_prefs.putUInt("pending_count", g_pending_count);
        logLine("INFO", "Upload OK. pending_count reset.");
      } else {
        logLine("WARNING", "Upload failed. pending_count kept.");
      }
    }
  }

  delay(1);
}

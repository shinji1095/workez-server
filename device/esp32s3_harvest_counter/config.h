#ifndef HARVEST_COUNTER_CONFIG_H
#define HARVEST_COUNTER_CONFIG_H

#include <Arduino.h>

// NOTE: This file contains device secrets. Handle with care.

static const char *CONFIG_WIFI_SSID = "aterm-cd7784-a";
static const char *CONFIG_WIFI_PASS = "9d1d50c097fc7";

static const char *CONFIG_SERVER_BASE_URL = "http://192.168.10.110";
static const char *CONFIG_API_PATH = "/api/harvest/amount/add";
static const char *CONFIG_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJERVYwMDEiLCJyb2xlIjoiZGV2aWNlIiwiaWF0IjoxNzY2NjI1Mzg5LCJleHAiOjE3NjY2Mjg5ODl9.whf_7zU8Wxg8mLAVsk8ZTaGd2VnGF78p6Rr_7roFuTI";
static const char *CONFIG_TOKEN_URL = "http://192.168.10.110/api/auth/token";
static const char *CONFIG_API_KEY = "1Vax7EOrnxYdQkj4dIQtpFxsZ04n2vsd";

static const char *CONFIG_DEVICE_ID = "DEV001";
static const char *CONFIG_CATEGORY_ID = "C1";

static const uint32_t CONFIG_SEND_INTERVAL_SEC = 10;
static const bool CONFIG_DEBUG = true;
static const bool CONFIG_LOG_TO_FILE = false;

static const int CONFIG_ADC_PIN = A0;
static const uint32_t CONFIG_SAMPLE_INTERVAL_MS = 25;

static const int CONFIG_THRESHOLD_HIGH = 1800;
static const int CONFIG_THRESHOLD_LOW = 1600;
static const uint32_t CONFIG_MIN_PRESENCE_MS = 50;
static const uint32_t CONFIG_MIN_GAP_MS = 500;

static const float CONFIG_EMA_ALPHA = 0.2f;

static const bool CONFIG_NTP_ENABLED = true;
static const char *CONFIG_NTP_SERVER = "192.168.10.110";
static const int CONFIG_TZ_OFFSET_MINUTES = 540;

#endif

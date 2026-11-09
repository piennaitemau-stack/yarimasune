#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ -z "${ANDROID_SDK_ROOT:-}" && -z "${ANDROID_HOME:-}" ]]; then
  if [[ -d "$HOME/android-sdk" ]]; then
    export ANDROID_HOME="$HOME/android-sdk"
  else
    echo "Set ANDROID_HOME to your Android SDK path." >&2
    exit 1
  fi
fi
export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$ANDROID_HOME}"
export ANDROID_HOME="${ANDROID_HOME:-$ANDROID_SDK_ROOT}"
printf 'sdk.dir=%s\n' "$ANDROID_HOME" > "$ROOT/local.properties"

if command -v gradle >/dev/null 2>&1; then
  (cd "$ROOT" && gradle :app:assembleRelease --no-daemon "$@")
elif [[ -x "$ROOT/gradlew" ]]; then
  (cd "$ROOT" && ./gradlew :app:assembleRelease --no-daemon "$@")
else
  echo "Install Gradle 8.7+ or generate the Gradle wrapper." >&2
  exit 1
fi

APK="$ROOT/app/build/outputs/apk/release/app-release.apk"
if [[ -f "$APK" ]]; then
  mkdir -p "$ROOT/../dist"
  cp "$APK" "$ROOT/../dist/kids-gakushu.apk"
  echo "APK: $ROOT/../dist/kids-gakushu.apk"
fi

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ANDROID_HOME="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/android-sdk}}"
export ANDROID_HOME ANDROID_SDK_ROOT="$ANDROID_HOME"

if [[ ! -d "$ANDROID_HOME/platforms" ]]; then
  echo "Android SDK not found at $ANDROID_HOME" >&2
  exit 1
fi

JAVA_HOME="${JAVA_HOME:-$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")}"
export JAVA_HOME

cat > "$ROOT/android/local.properties" <<EOF
sdk.dir=$ANDROID_HOME
EOF

cd "$ROOT/android"
if [[ ! -x ./gradlew ]]; then
  echo "gradlew is missing. Generate the wrapper first." >&2
  exit 1
fi

./gradlew :app:assembleRelease --no-daemon

mkdir -p "$ROOT/dist"
cp -f "$ROOT/android/app/build/outputs/apk/release/kids-gakushu-release.apk" \
  "$ROOT/dist/kids-gakushu.apk"
echo "APK: $ROOT/dist/kids-gakushu.apk"
ls -lh "$ROOT/dist/kids-gakushu.apk"

# こども学習アプリ（Android APK）

`kids-gakushu.html` を Android の WebView アプリとしてパッケージした学習アプリです。ネット接続なしで動きます。

## APK の入れ方

1. [`dist/kids-gakushu.apk`](dist/kids-gakushu.apk) をスマホやタブレットにコピーする（USB、Google ドライブ、メールなど）
2. ファイルアプリで APK を開く
3. 「この提供元からのアプリを許可」と出たらオンにする
4. インストール → 開く
5. ホーム画面の **こども学習** をタップする

| 項目 | 内容 |
| --- | --- |
| アプリ名 | こども学習 |
| パッケージ名 | `jp.kidsgakushu.app` |
| 対応OS | Android 8.0 以降 |
| 署名 | デバッグ署名（ストア公開用ではありません。端末への直接インストール用です） |

読み上げ（音声）を使う場合は、端末に日本語のテキスト読み上げ（Google テキスト読み上げなど）が入っている必要があります。

## 自分でビルドする

Android SDK と JDK 17 以上が必要です。

```bash
export ANDROID_HOME=/path/to/android-sdk
./scripts/build-apk.sh
```

成果物は `dist/kids-gakushu.apk` です。`kids-gakushu.html` を直したら、同じコマンドでもう一度ビルドすれば APK に取り込まれます。

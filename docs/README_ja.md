# Text Tools in Right-Click Menu

エディタの**右クリックメニュー**に **Text Tools** メニューを追加し、よく使う書式設定・挿入・編集コマンドへすばやくアクセスできるようにする Anki アドオンです。

- AnkiWeb: https://ankiweb.net/shared/info/2143302836
- [English README](../README.md)
- [AnkiWeb 説明文ドラフト](ANKIWEB_DESCRIPTION_ja.md)
- [AnkiWeb description draft](ANKIWEB_DESCRIPTION.md)

![スクリーンショット: エディタの右クリックメニュー](Screenshot_right-click_menu.png)

## 主な特徴

- 文字装飾、色、サイズ、配置、リスト、書式クリアを右クリックメニューから実行
- リンク、画像、ルビ、表、日付/時刻、数式、引用、水平線、特殊文字を挿入
- Quick Items と User Words でよく使う項目を上部にまとめられる
- [Edit Field During Review (Cloze)](https://ankiweb.net/shared/info/385888438) と組み合わせると reviewer 側でも多くの機能を利用可能

## リポジトリ構成

- `Text-Tools/`: 配布される Anki アドオン本体
- `docs/`: スクリーンショットと GitHub/AnkiWeb 向けドキュメント
- `scripts/`: `.ankiaddon` 生成などの補助スクリプト
- `tests/`: 設定移行、メニュー定義、アクション分岐、メニュー構築、パッケージ生成を確認する自動テスト

実行時のコードは、一般的な `src/` 構成には移していません。`.ankiaddon` ではアドオンの中身がアーカイブ直下に入る必要があるため、`Text-Tools/` をそのまま配布レイアウトに近い形で保つほうが運用しやすいためです。

## 開発

必要なら Ruff をインストールします。

```bash
py -3 -m pip install ruff
```

lint と整形:

```bash
py -3 -m ruff check .
py -3 -m ruff format .
```

テスト実行:

```bash
py -3 -m unittest discover -s tests -v
```

配布用 `.ankiaddon` の生成:

```bash
py -3 scripts/build_ankiaddon.py
```

`dist/Text-Tools.ankiaddon` が生成され、`Text-Tools/` の中身がアーカイブ直下に入ります。`__pycache__/`、`*.pyc`、および `Text-Tools/user_files/` 内のユーザー固有ファイルは `README.txt` を除いて自動で除外されます。

## リリース手順

1. 上記の lint / format を実行します。
2. `dist/Text-Tools.ankiaddon` を生成します。
3. 生成された `.ankiaddon` を AnkiWeb に手動でアップロードします。

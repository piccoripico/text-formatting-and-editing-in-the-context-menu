# Text Tools in Right-Click Menu

エディタの**右クリックメニュー**に **Text Tools** メニューを追加し、よく使う書式設定・挿入・編集コマンドにすばやくアクセスできるようにする Anki アドオンです。

- AnkiWeb: https://ankiweb.net/shared/info/2143302836
- [GitHub repository](https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu)
- [English README](https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/blob/main/docs/README.md)

![スクリーンショット: エディタの右クリックメニュー](https://raw.githubusercontent.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/main/docs/Screenshot_right-click_menu.png)

## 機能

- **書式設定:** 太字、斜体、下線、取り消し線、小さい文字、上付き文字、下付き文字、等幅フォント、インラインコード
- **色とサイズ:** 文字色、ハイライト色、フォントサイズプリセット、フォント選択ダイアログ
- **レイアウト:** 文字揃え、インデント/インデント解除、番号なしリスト/番号付きリスト
- **挿入:** リンク、画像、ルビ、表、日付/時刻、数式スニペット、引用ブロック、水平線、特殊文字
  ローカル画像ファイルは、挿入前に Anki のメディアコレクションへ取り込みます。
- **編集:** 切り取り、コピー、貼り付け、プレーンテキストとして貼り付け、リンク削除、すべて選択、元に戻す/やり直し、すべての書式をクリア
- **その他:** スタイルプリセット、文字数カウント

### オプション

#### Quick Items

- よく使うコマンドを選択して、すばやく使えるようにできます。
- 既定では、**Text Tools** メニュー内の上部付近に表示されます。
- 右クリックメニューのトップレベルに表示することもできます。

#### User Words

- 自分専用の単語や短い定型文を登録し、**User Words** サブメニューから挿入できます。
- 右クリックメニューのトップレベルに表示することもできます。

## Reviewer サポート

このアドオンは、レビュー画面の右クリックメニューにも **Text Tools** を表示できます。[**Edit Field During Review (Cloze)**](https://ankiweb.net/shared/info/385888438) をインストールしている場合、reviewer 側の機能の多くを利用できます。

reviewer 対応は、このアドオンを開発する元々の動機でした。

## 設定

開き方:

> ツール → アドオン → Text Tools in Right-Click Menu → Config

設定ウィンドウには 3 つのタブがあります。

- **General** — エディタおよび/または reviewer の右クリックメニューに **Text Tools** を表示します
- **Quick Items** — よく使う項目を選び、必要に応じて右クリックメニューのトップレベルに表示します
- **User Words** — 独自の単語を追加・編集・削除・並べ替え・インポート・エクスポートし、必要に応じて右クリックメニューのトップレベルに表示します

![スクリーンショット: 設定ウィンドウ](https://raw.githubusercontent.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/main/docs/Screenshot_config.png)

## ビルド

次のコマンドで、配布用の `.ankiaddon` をクリーンに作成できます。

```bash
py -3 scripts/build_ankiaddon.py
```

`dist/Text-Tools.ankiaddon` が生成され、`Text-Tools/` の中身がアーカイブ直下に入ります。

ビルド時には、次のような生成物は自動で除外されます。

- `__pycache__/`
- `*.pyc`
- `Text-Tools/user_files/` 内のユーザー固有ファイル（`README.txt` を除く）

## 更新履歴

- 2026-03-08
  - アドオンを全面改訂
  - アドオン名を **Text Formatting and Editing in the Context Menu** から **Text Tools in Right-Click Menu** に変更
  - スタイルプリセット、ルビ挿入、表挿入などの機能を追加
- 2025-04-15
  - 設定ウィンドウが開かない問題を修正
- 2023-09-03
  - 設定ウィンドウに reviewer の右クリックメニューに関する注記を追加（フィードバックありがとうございます）
- 2023-08-16
  - User Words 機能を追加
- 2023-07-29
  - Quick Items をコンテキストメニューのトップレベルに表示するオプションを追加
- 2023-07-27
  - 設定ウィンドウを追加（アドオン更新後は Anki を再起動してください）
  - Quick Items 機能を追加
  - いくつかのバグを修正

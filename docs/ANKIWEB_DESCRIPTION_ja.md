エディタの**右クリックメニュー**に **Text Tools** メニューを追加し、よく使う書式設定・挿入・編集コマンドにすばやくアクセスできるようにする Anki アドオンです。

![スクリーンショット: エディタの右クリックメニュー](https://raw.githubusercontent.com/piccoripico/text-formatting-and-editing-in-the-context-menu/main/docs/Screenshot_right-click_menu.png)

## 機能

- **書式設定:** 太字、斜体、下線、取り消し線、小さい文字、上付き文字、下付き文字、等幅フォント、インラインコード
- **色とサイズ:** 文字色、ハイライト色、フォントサイズプリセット、フォント選択ダイアログ
- **レイアウト:** 文字揃え、インデント/インデント解除、番号なしリスト/番号付きリスト
- **挿入:** リンク、画像、ルビ、表、日付/時刻、数式スニペット、引用ブロック、水平線、特殊文字
- **編集:** 切り取り、コピー、貼り付け、プレーンテキストとして貼り付け、リンク削除、すべて選択、元に戻す/やり直し、すべての書式をクリア
- **その他:** スタイルプリセット、文字数カウント

## オプション

### Quick Items

- よく使うコマンドを選択して、すばやく使えるようにできます。
- **Text Tools** メニュー内の上部付近に表示することも、右クリックメニューのトップレベルに表示することもできます。

### User Words

- 自分専用の単語や短い定型文を登録し、**User Words** サブメニューから挿入できます。
- **Text Tools** 内に表示することも、右クリックメニューのトップレベルに表示することもできます。

## Reviewer サポート

このアドオンは、レビュー画面の右クリックメニューにも **Text Tools** を表示できます。[**Edit Field During Review (Cloze)**](https://ankiweb.net/shared/info/385888438) をインストールしている場合、reviewer 側の機能の多くを利用できます。

## 設定

開き方:

> Tools -> Add-ons -> Text Tools in Right-Click Menu -> Config

設定ウィンドウには 3 つのタブがあります。

- **General**: エディタおよび reviewer の右クリックメニューに **Text Tools** を表示します
- **Quick Items**: よく使う項目を選び、必要に応じて右クリックメニューのトップレベルに表示します
- **User Words**: 独自の単語を追加・編集・削除・並べ替え・テキストファイルでインポート/エクスポートし、必要に応じて右クリックメニューのトップレベルに表示します

![スクリーンショット: 設定ウィンドウ](https://raw.githubusercontent.com/piccoripico/text-formatting-and-editing-in-the-context-menu/main/docs/Screenshot_config.png)

## 更新履歴

- 2026-04-04
  - ローカル画像を、そのままローカルパス参照するのではなく、Anki のメディアコレクションに取り込んでから挿入するように改善
  - cut / copy / paste の挙動を改善し、書式を保持しやすくした
- 2026-03-08
  - アドオンを**全面改訂**
  - アドオン名を **Text Formatting and Editing in the Context Menu** から **Text Tools in Right-Click Menu** に変更
  - スタイルプリセット、ルビ挿入、表挿入などの機能を追加
- 2025-04-15
  - 設定ウィンドウが開かない問題を修正
- 2023-09-03
  - 設定ウィンドウに reviewer の右クリックメニューに関する注記を追加
- 2023-08-16
  - User Words 機能を追加
- 2023-07-29
  - Quick Items をコンテキストメニューのトップレベルに表示するオプションを追加
- 2023-07-27
  - 設定ウィンドウを追加
  - Quick Items 機能を追加
  - いくつかのバグを修正

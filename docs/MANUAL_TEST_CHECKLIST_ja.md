# 手動テストチェックリスト

AnkiWeb に新しい `.ankiaddon` をアップロードする前に、このチェックリストで確認します。

## 準備

1. `py -3 scripts/build_ankiaddon.py` で最新のパッケージを生成します。
2. 生成された `dist/Text-Tools.ankiaddon` をテスト用 Anki プロファイルにインストールします。
3. インストール後に Anki を再起動します。
4. editor でノートを 1 件、reviewer でカードを 1 件開きます。

## Editor メニュー

1. editor のフィールド内で右クリックします。
2. `Text Tools` が 1 回だけ表示されることを確認します。
3. `Text Tools` を開き、主要グループがあることを確認します:
   `Style Presets`, `Text Styling`, `Text Color`, `Font Size`, `Alignment / List`, `Insert`, `Edit`
4. 代表的なコマンドをいくつか実行し、選択テキストに反映されることを確認します:
   `Bold`, `Highlight Yellow`, `Justify Center`, `Clear All Formatting`

## Quick Items と User Words

1. Anki のアドオン一覧から設定画面を開きます。
2. Quick Items をいくつか有効化し、トップレベル表示の有無も切り替えます。
3. User Words をいくつか追加し、次の両方を試します:
   トップレベル表示 と `Text Tools > User Words`
4. 右クリックメニューを開き直し、保存した設定どおりに表示されることを確認します。

## クリップボードと挿入系

1. editor 内の書式付きテキストをコピーして貼り付けます。
2. 通常の paste では HTML の書式が保たれることを確認します。
3. `Paste Plain Text` では書式が消えることを確認します。
4. `Insert Link`, `Insert Image`, `Insert Ruby`, `Horizontal Line`, 表の挿入を 1 つずつ試します。
5. `Insert Image` では次の両方を確認します:
   リモート URL と ローカルファイルパス
6. ローカル画像を挿入したあと、Anki を再起動しても画像が表示されることを確認します。

## Reviewer 動作

1. `Edit Field During Review (Cloze)` を入れている場合は、review mode で reviewer の右クリックメニューを開きます。
2. review mode で `Text Tools` が 1 回だけ表示されることを確認します。
3. reviewer 側の代表的な操作を試します:
   `Insert Text`, `Paste`, `Paste Plain Text`, `Copy`, `Cut`, `Clear All Formatting`, `Word Count`
4. review mode 以外の webview ではメニューが出ないことを確認します。

## Config の import / export

1. 設定画面の `User Words` タブを開きます。
2. 現在の一覧を `.txt` に export します。
3. 一覧を空にして `.txt` を import します。
4. カンマを含む語も含めて、順序と値が正しく往復することを確認します。

## Release 前の最終確認

1. 次を再実行します:
   `py -3 -m ruff check .`
2. 次を再実行します:
   `py -3 -m unittest discover -s tests -v`
3. 次を再実行します:
   `py -3 scripts/build_ankiaddon.py`
4. AnkiWeb にアップロードする対象が `dist/Text-Tools.ankiaddon` であることを確認します。

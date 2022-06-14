## 作業手順

main ブランチにいることを確認

```
git branch
```

もし、main にいなければ、main に移動

```
git checkout main
```

GitHub の main ブランチとローカルの main ブランチを同期する

```
git pull
```

作業用ブランチを作成

```
git checkout -b feature/sagyounaiyou
```

作業をする

---

**作業が完了したら**

```
git add -A
git commit -m 'commitメッセージ'
git push origin HEAD
```

GitHub 上で PR(プルリクエスト) の操作をする

レビュー後 merge がされます

## コミットメッセージやブランチ名のルール

### コミットメッセージ

基本的に日本語で書いてください

書き方の format

```
[{作業タグ}}]{機能名}・{編集ファイル名・作成ファイル名}
```

作業タグは作成・修正・削除の三つ

出来るだけ一つのコミットで行う作業を分割するようにしましょう

後でひとまとめにできたりするので

### ブランチ名

こちらは絶対に英語で書いてください

書き方の format

```
feature/{作成・修正・削除する機能の名前}
```

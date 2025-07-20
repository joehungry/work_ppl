# セッションを始める

インストールが終われば、早速プログラムが使えます。でも、すぐにセッションを始められるわけではありません。まずはセッションをセットアップする必要があります。

## セッションの必要設定をセットアップ
このプログラムを使うためには４つの設定をセットアップする必要があります。それはそれぞれ、**ポイントをオンにするか**、**セッション名**、**推定時間**、**セッションのゴール**です。難しい、、、って思う人でも、すぐになれるので一つずつ説明します。

### ポイントをオンにするか
ポイントって何それって思う人が大多数でしょう。実は最初に説明するように書いたのは、ポイントがこのプログラムの根幹を担うからなのです。
このプログラムはセッションを行えば行うほどポイントがもらえます（しかも一日の使用時間によって時間ごとに貰えるポイントは段々増えていきます！）。
そうしてもらったポイントは何をするにも特に制限はしないですけど、ご褒美とかに使うこともできます。ポイントを使用したり、課題をこなして追加のポイントがもらえるプログラムも同封してあるので、ぜひご一緒に使用してください。
とにかく、ポイントをもらわないでセッションを開始することもできます。例えば、プログラム自体を使うことを常習化したいけど、今特にポイントをもらうほどのことはやってない、というときにポイントを付けないで使用することもできます。ポイントなしで使う機会はあまりないとは思いますが、いざというときに役に立ちますよ！
どうオンオフを設定するかというと、`p`を使います。`p`は、ポイントをオン、`p'off`は、ポイントをオフにするときのコマンドです。ポイントは、`p'on`を使ってもオンにできますけど、`p`が圧倒的に楽なので、もう`p`って覚えておきましょう。他のコマンドにも言えることですけど、基本実行するコードは複数あるので、好きなものを使ってください。下に書いておきます。これからも同じように下に書き方の一覧を書いておくのでご参考に。

```
p ←大文字でも小文字でも使えます。ただし、on やoff などは小文字でしか書けないのであしからず。わかりやすくするために下に大文字と小文字を混ぜて書きます。他の項でもおなじように大文字と小文字がないまぜに書いてあったら、どちらでも書けるということで覚えておいてください。

>> P
point system is on

>> p'on 
point system is on 

>> P'off
point system is off

>> p'no
point system is off

>> P'none
point system is off

>> p'\n
point system is off

```



### セッション名
えー、めんどくさい、って思ったかもしれません。ですが、セッション名って意外と大事なんです！　自分が今何をしようとしているかを明確化することはすごく大事なんです。自分が今何をしようとしているのかを見失ったまま別のことを始めることはありませんか？　セッション名をきちんと明確化することで、そうした気の散り方を減少させることが出来ます。
`L'好きな名前`で設定することができます。もしくは`label'好きな名前`でもできますけど、でも長いから前者の方が明らかに良いですよね。`L'\s`で前回と同じものが使えます。ただし、前日のデータはプログラムにはアクセスできないようになっているので、前日分は使えません。

```

>> L'好きな名前
session name = 好きな名前

>> l'好きな名前
session name = 好きな名前

>> label'好きな名前
session name = 好きな名前

```

### 推定時間
セッションを始める前に自分のしようとしている課題がどれだけの長さで終わることが出来るのかを決めます。これ実はポイントシステムに関わる重要な設定なので、慎重に決めましょう。長すぎても短すぎてもいけません。ちょうどいい長さにしましょう。ゴールを決める場所でもう少し具体的に話します。
`T'好きな名前`で設定することができます。もしくは`tim.length'好きな名前`でもできますけど、後者書くのダルすぎてやばいすよね。`L'\s`で前回と同じものが使えます。ただし、前日のデータはプログラムにはアクセスできないようになっているので、前日分は使えません。あと一応、`L'\n`で時間の長さをほぼ無制限にすることができます（すごい適当に作った昨日なので、ただめっちゃ長い指定時間になっているだけです。だから実用性はありません）

```

>>T'2
tim.length = 2 (minutes)

>> t'aa
error

>> tim.length'25
tim.length = 2 (minutes)

```


### セッションのゴール

#### そもそもゴールって何？

ゴールは、セッション内で何をするのか明確化することで、たくさんポイントをもらえる方法です。
このゴールを時間通りに終わらせたら、通常の訳４倍のポイントがもらえます。
時間内に終わらせただけでも通常の倍程度はもらえるのでご心配なく。

#### ゴールの設定方法

ゴールは`goal`コマンドで設定できます。以下のプリセットからゴールを設定できます。
you can set up goals with the `goal` command. the goals you can set up are from the following preset:
- `new` もしくは `nw` (新しいことを学ぶことをさす)
- `correct` もしくは `c` (正答をさす)
- `incorrect` もしくは `x` (誤答をさす)
- `solve` もしくは `sv` (正誤答関わらず問をさす)
- `task` もしくは `t` (タスクを一つ完結することをさす)

- `none` もしくは `n`, または `\n` (ゴールがいらないとき)
- `same` もしくは `s`, または `\s` (前回のセッションと同じゴールのとき。ただ、プログラムを閉じれば、ゴールのデータは消えることを留意しておいてほしいです)

ゴールには下の二つか、具体的な数字が必用です。 数字は`=`で紐づけられます。例えば、タスクを八つ完結したい場合は、

`goal solve = 8`

と書けます。
また、 `done` や `d` を`1`の代わりに書くこともできます。例えば、一つのタスクを完結させたいだけなら、
```
 goal task = done
 goal task = d
 goal task
 
\\\どれもgoal task = 1と同じ意味

 ```
 と書くことが可能です。

`none` and `same`などの代数を除き、`and`や`or`で、タスクを繋げることもできます。

the goals (excluding  of course) can be combined to make an ultimate goal by using `and`.
for instance, if you want to finish a task and also read two research papars you haven't yet, you can type, `goal task = d and new = 2`,

If you want the goal to be answering two questions correctly, or answer ten questions incorrectly, you can type `goal c = 2 or x = 10`

If you want to combine the count of multiple goals, for instance, if you want to count `new` and `correct` at the same time, you can use `goal nw and c = 10` to count both instances until 10.

Of course, if you want to combine an `and` expression and an `or` expression, it is perferred to use parentheses.
Like this `task = d and (new = 2 or x = 10)` ←although this is what `task = d and new = 2 or x = 10` means so you don't really need it. but you would need it for `(task = d and new = 2) or x = 10`

Maybe you want the goal to b
for example,

task = d and new = 2 or x = 10


# autorest!!!

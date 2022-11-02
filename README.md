# ThirdGenPictureSeed

絵画seed乱数調整の自動化（Poke-Controller MODIFIED用）

## インストール

`Poke-Controller-Modified/SerialController/Commands/PythonCommands/`以下にcloneしてください。

```sh
git clone --depth=1 https://github.com/mukai1011/ThirdGenPictureSeed.git
```

## 動作の解説

```mermaid
stateDiagram-v2
    
    Reset: リセット
    StandbyMultiBoot: マルチブート待機
    CancelMultiBoot: マルチブート待ち受け解除
    SkipOpening: オープニングをスキップ
    Load: ロード
    Appreciate: 絵画鑑賞
    Move: 移動
    Encounter: エンカウント
    Wait1: 指定時間待機
    Wait2: 指定時間待機

    [*] --> Reset
    Reset --> StandbyMultiBoot
    
    state fork1 <<fork>>
    state join1 <<join>>
        StandbyMultiBoot --> fork1

        fork1 --> CancelMultiBoot
        CancelMultiBoot --> SkipOpening
        SkipOpening --> Load
        Load --> join1

        fork1 --> Wait1
        Wait1 --> join1

    state fork2 <<fork>>
    state join2 <<join>>
        join1 --> fork2

        fork2 --> Appreciate
        Appreciate --> Move
        Move --> join2

        fork2 --> Wait2
        Wait2 --> join2

    join2 --> Encounter
    Encounter --> [*]
```

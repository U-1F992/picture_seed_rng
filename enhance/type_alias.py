from typing import List, Tuple, Union

from Commands.Keys import Button, Direction, Hat

# Pythonコマンド_作成How_to
# - https://github.com/KawaSwitch/Poke-Controller/wiki/Python%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89_%E4%BD%9C%E6%88%90How_to

#
# pressメソッドの引数buttonが取りうる型
#
ButtonSpecifier = Union[
    Button, 
    Hat, 
    Direction, 

    # 同時入力
    List[
        Union[
            Button, 
            Hat, 
            Direction
        ]
    ]
]

#
# pressメソッドが取りうる引数の組み合わせ
#
# - buttons: 押下するボタン
# - duration: 押下時間[秒] デフォルトは0.1
# - wait: 押下後に待つ時間[秒] デフォルトは0.1
#
PressArgumentCombination = Union[
    Tuple[ButtonSpecifier],
    Tuple[ButtonSpecifier, float],
    Tuple[ButtonSpecifier, float, float],
]

#
# isContainTemplateメソッドが取りうる引数の組み合わせ
#
# - template_path: 探すテンプレート画像のパス(拡張子を含む画像名)
# - threshold: しきい値 デフォルトでは0.7
# - use_gray: 処理をグレースケールで行う デフォルトではTrue
#
IsContainTemplateArgumentCombination = Union[
    Tuple[str],
    Tuple[str, float],
    Tuple[str, float, bool],
]

ArgumentCombination = Union[
    PressArgumentCombination,
    IsContainTemplateArgumentCombination
]

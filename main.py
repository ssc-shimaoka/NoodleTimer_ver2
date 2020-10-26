from microbit import *
import dispTime
import music
###---------------------------------------------------------------
### 変数定義
###---------------------------------------------------------------
blockNumber       = 6   #ブロック数[1-25]
blockSurvivalTime = 30  #ブロック生存時間(秒)[1-60]

timerStatus    = 0      #タイマー状態
setTime        = 0      #設定時間(ミリ秒)
operatingTime  = 0      #稼動時間(ミリ秒)
startTime      = 0      #開始時間(ミリ秒)
elapsedTime    = 0      #経過時間(ミリ秒)
updateInterval = 1000   #更新間隔(ミリ秒)
pauseStartTime = 0      #一時停止 開始稼働時間(ミリ秒)
pauseEndTime   = 0      #一時停止 終了稼働時間(ミリ秒)
pauseTotalTime = 0      #一時停止 トータル時間(ミリ秒)

###---------------------------------------------------------------
#ブロック数取得関数
###---------------------------------------------------------------
def GetRemainingBlocks():
    elapsedTime = running_time() - startTime - pauseTotalTime
    dispTime = int((setTime - elapsedTime) / updateInterval / blockSurvivalTime) + 1
    return dispTime

###---------------------------------------------------------------
#main loop
###---------------------------------------------------------------
display.show(Image.HAPPY)
music.play(music.BA_DING)

while True:
###---------------------------------------------------------------
#A+Bボタン押下
###---------------------------------------------------------------
    if button_a.is_pressed() and button_b.is_pressed():
        #タイマー一時停止状態
        if timerStatus == 2 :
            display.show(Image.CHESSBOARD)
            timerStatus = 0
###---------------------------------------------------------------
#Aボタン押下
###---------------------------------------------------------------
    elif button_a.is_pressed():
        #タイマー未動作状態
        if timerStatus == 0 :
            #タイマー開始時間に現在の時刻を代入（ミリ秒）
            startTime = running_time()
            #タイマー指定時間 設定
            setTime = blockNumber * blockSurvivalTime * updateInterval
            #タイマー状態更新（未動作→動作中）
            timerStatus = 1
            #出力
            display.scroll("start",50)
###---------------------------------------------------------------
#Bボタン押下
###---------------------------------------------------------------
    elif button_b.is_pressed():
        if timerStatus == 1 :
            #タイマー状態更新（動作中→一時停止）
            timerStatus = 2
            pauseStartTime = running_time()
            display.scroll("pause",50)

        elif timerStatus == 2 :
            #タイマー状態更新（一時停止→動作中）
            timerStatus = 1
            pauseEndTime = running_time()
            pauseTotalTime = pauseTotalTime + (pauseEndTime - pauseStartTime)
            display.scroll("restart",50)

###---------------------------------------------------------------
#タイマー未動作状態の処理
###---------------------------------------------------------------
    if timerStatus == 0 :
        #点灯LED表示
        display.show(Image.CHESSBOARD)

###---------------------------------------------------------------
#タイマー動作中状態の場合
###---------------------------------------------------------------
    elif timerStatus == 1 :
        #残りブロック数取得
        blocks = GetRemainingBlocks()

        #ブロックが0個になった場合
        if blocks == 0 :
            #満了演出
            display.show(Image.HAPPY)
            music.play(music.RINGTONE)

            #状態初期化
            sleep(3000)
            display.show(Image.CHESSBOARD)
            timerStatus = 0

        #ブロックが残っている場合
        else :
            #点灯LED表示
            display.show(dispTime.BlockArrey[blocks])
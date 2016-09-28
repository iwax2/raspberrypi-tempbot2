# raspberrypi-tempbot2

Raspberry PiでIoT温湿度計を作ってみました。
基本的には [raspberrypi-tempbot](https://github.com/iwax2/raspberrypi-tempbot) と同じですが、デモに使うので一部見栄えをするものに変更しています。

## 機能
* スイッチを押すと喋る
 VoiceText Web APIを利用させていただいています。
* フルカラーLEDでグラデーション
 アノードコモンのフルカラーLEDをPWMで制御しています
* twitter自動投稿
 トークンは適宜変更が必要です。

## 使い方
### スイッチ機能
`pi% nohup ./pwm.py &`
で実行しておけばフルカラーLEDが自動でグラデーションして、スイッチが押されると
1. 温度取得
2. 音声取得
3. スピーカー出力
をします。

### twitter-bot機能
`pi% sudo crontab -e`
を実行して
`02 */3  * * *   /home/pi/tempbot/sht-21.py`
を追加すればOKです。

## ポスター
![ポスター](poster.png)

## 使用部品
* Raspberry Pi2 Model B
* 温湿度計 [USB-RH](https://strawberry-linux.com/catalog/items?code=52001) (Strawberry-Linux) Sensirion SHT-11使用
* スイッチ ダイソー108円LEDスイッチ？
* [アノードコモン フルカラーLED](http://www.aitendo.com/product/6926)
* 抵抗（100Ωx2 330Ωx1 1kΩx1)
* スピーカー[TPA2006使用　超小型D級アンプキット](http://akizukidenshi.com/catalog/g/gK-08161/) ほか

import chat_bot_
from pygame import mixer
import time

# 語音撥放初始化
mixer.init()
# 先跳出監聽狀態
check_out = False

# 實作CHAT BOX裡的物件
CB = chat_bot_.Bot()

text='你好，公館有許多美食包含，台式、越式、義大利，你喜歡甚麼類型的口味，並提供用餐人數'
CB.speak(text)
time.sleep(1)

# 當不是結束時，就監聽
while not CB.check_out:
    CB.listen()
import speech_recognition as sr#串聯google語音辨識，將語音轉為文字，所以一定要聯網
from gtts import gTTS #也是google語音辨識套件，也要連網使用
from pygame import mixer #用來製造及播放聲音的模組，稱為混音器
import tempfile #會自動創建、執行、刪除檔
import jieba #斷詞語料庫
import time

# 設定判斷語料
# 定義美食分類
eat_list = ['台菜','越式','義大利菜','日式']
# 定義訂位人數
quantity_list=['一','二','兩','三','四','五','六','七','八','九','十','1','2','3','4','5','6','7','8','9','10']
item_list=[]
info={}

class Bot():
    def __init__(self)  :
        self.check_out = False

    # 定義發聲方法
    def speak(self,sentence):
        with tempfile.NamedTemporaryFile(delete=True) as fp :
            tts = gTTS(text = sentence,lang='zh-tw')
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
            while mixer.music.get_busy():
                pass

    def listen(self):
        global item_list
        r = sr.Recognizer()
        with sr.Microphone(device_index=0) as source:
            print('bot litening....')
            audio = r.listen(source)
            print('bot processing')

        try:
            customer_schedule = r.recognize_google(audio, language='zh-tw')
            print('Google Speech Recognition thinks YOU said'+customer_schedule)
            if '結束' in customer_schedule:
                if not item_list:
                    self.speak('請安排行程')
                    time.sleep(2)
                else:
                    print('結束')
                    global check_out
                    self.check_out = True
            elif '重新安排' in customer_schedule:
                item_li = []
                self.speak('行程已刪除，請重新安排')
                time.sleep(2)
            else:
                seg_list = jieba.cut(customer_schedule,cut_all=False)
                print(','.join(seg_list))
                print(customer_schedule)
                print('info:')
                print(info)

                for quantity in quantity_list:
                    if quantity in customer_schedule:
                        info['人數'] = quantity
                        break
                name_count = len(eat_list)
                for name in eat_list:
                    if name_count  == 0:
                        self.speak('目前無提供該活動')
                    elif name in customer_schedule:
                        if name == '義大利麵':
                            info['美食']='蘇活義大利麵'
                        elif name == '台式' or '台':
                            info['美食']='筷子餐廳'
                        elif name == '越式':
                            info['美食'] = '銀座越南美食'
                print('info add:')
                print(info)
                print('item_list:')
                print(item_list)
                self.speak('你安排了{},{}位，說[結束]可完成規劃'.format(info.get['美食'],info.get['人數'],'一'))
                name_count -= 1
        
        except sr.UnknownValueError:
            print('Google Speech Recognition could not undertand audio')
            self.listen()
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service; {0}'.format(e))


    def checkout(self):
        if self.check_out == True:
            for info in item_list:
                self.speak('安排了{},{}位'.format(info.get('美食'),info.get('人數','一')))
                break
            self.speak('請稍等，資訊將寄送至你的簡訊')
            time.sleep(2)
            print('end')
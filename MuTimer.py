###Muシリーズで時計を表示する###
# pygameライブラリが必要です
# 画面付きのMuシリーズが必要です


######動作確認済み機器一覧#######
# Mu128V2
###############################

import pygame
import pygame.midi
import time
import datetime

#メッセージウィンドーのアスキーコード
msg_window_dictionary={
  " ":b"\x20","!":b"\x21",'"':b"\x22","#":b"\x23","$":b"\x24","%":b"\x25","&":b"\x26","'":b"\x27","(":b"\x28",")":b"\x29","*":b"\x2A","+":b"\x2B",",":b"\x2C","-":b"\x2D",".":b"\x2E","/":b"\x2F",
  "0":b"\x30","1":b"\x31","2":b"\x32","3":b"\x33","4":b"\x34","5":b"\x35","6":b"\x36","7":b"\x37","8":b"\x38","9":b"\x39",":":b"\x3A",";":b"\x3B","<":b"\x3C","=":b"\x3D",">":b"\x3E","?":b"\x3F",
  "@":b"\x40","A":b"\x41","B":b"\x42","C":b"\x43","D":b"\x44","E":b"\x45","F":b"\x46","G":b"\x47","H":b"\x48","I":b"\x49","J":b"\x4A","K":b"\x4B","L":b"\x4C","M":b"\x4D","N":b"\x4E","O":b"\x4F",
  "P":b"\x50","Q":b"\x51","R":b"\x52","S":b"\x53","T":b"\x54","U":b"\x55","V":b"\x56","W":b"\x57","X":b"\x58","Y":b"\x59","Z":b"\x5A","[":b"\x5B","￥":b"\x5C","]":b"\x5D","^":b"\x5E","-":b"\x5F",
  "`":b"\x60","a":b"\x61","b":b"\x62","c":b"\x63","d":b"\x64","e":b"\x65","f":b"\x66","g":b"\x67","h":b"\x68","i":b"\x69","j":b"\x6A","k":b"\x6B","l":b"\x6C","m":b"\x6D","n":b"\x6E","o":b"\x6F",
  "p":b"\x70","q":b"\x71","r":b"\x72","s":b"\x73","t":b"\x74","u":b"\x75","v":b"\x76","w":b"\x77","x":b"\x78","y":b"\x79","z":b"\x7A","{":b"\x7B","￤":b"\x7C","}":b"\x7D","~":b"\x7E"
}

#メッセージウィンドーのシステムエクスクルーシブメッセージ
msg_window_top = b"\xF0\x43\x10\x4C\x06\x00\x00"
msg_window_bottom =b"\xF7"


# 関数：文字列を16進数コード群に変換
def strTohexArray(strArray):
  hexstr = b""
  for singlestr in list(strArray):
    hexstr += msg_window_dictionary[singlestr]
  return hexstr



# 初期化
pygame.midi.init()
count = pygame.midi.get_count()

# 一覧を表示し、MIDI OUTを選択させる
print("接続するMIDI OUTを選択してください")
print("No:(interf, name, input, output, opened)")
for i in range(count):
    print("%d:%s" % (i, pygame.midi.get_device_info(i)))

output_number=input()
try:
  out = pygame.midi.Output(int(output_number))
  print(output_number,"が選択されました")
  print("Ctrl+Cを押すと終了します")

  out.write_sys_ex(0,msg_window_top+strTohexArray("Welcome!")+msg_window_bottom)
  out.set_instrument(5)
  out.note_on(72, 127)
  time.sleep(1)
  out.note_off(72, 127)

  #時計を表示(無限ループ)
  while True:
    dt_now = datetime.datetime.now()
    out.write_sys_ex(0,msg_window_top+strTohexArray(dt_now.strftime('%Y/%m/%d(%a)    %H:%M:%S'))+msg_window_bottom)
    
    if dt_now.second == 57:
      out.note_on(60,127)
    elif dt_now.second > 57:
      out.note_off(60,127)
      out.note_on(60,127)
    elif dt_now.second == 0:
      out.note_off(60,127)
      out.note_on(72,127)
    elif dt_now.second == 2:
      out.note_off(72,127)

    time.sleep(1)

except KeyboardInterrupt:
  out.write_sys_ex(0,msg_window_top+strTohexArray("Bye!")+msg_window_bottom)
  out.close()
  pygame.midi.quit()
  print("Ctrl+Cが押されたため終了します")
except Exception:
  out.close()
  pygame.midi.quit()
  import traceback
  traceback.print_exc()
  print("やり直してください")



# CN – HW1 IRC Robot

學號：b04902053

姓名：鄭淵仁

## Program structure

- 我使用的是 `python3.5`。


- files

  | 檔名           | 作用                                       |
  | ------------ | ---------------------------------------- |
  | `config`     | IRC Configuration                        |
  | `main.py`    | Main program                             |
  | `gen_ip.py`  | 給定 ip string，會回傳所有可能的 ip 排法，會被 include 進 main.py |
  | `Report.pdf` | Report                                   |

- functions

  - `gen-ip.py`

    這個檔案會被 include 進 `main.py` 裡面。用到的 function 如下：

    | function          | 作用                                       |
    | ----------------- | ---------------------------------------- |
    | `gen_dot_poses()` | 用 recursive 的方式，在 ip string 的中間的適合的位置插入小數點 |
    | `gen_be_head()`   | 用來事先判斷這個 string 的每一格是不是 `'0'`            |
    | `gen_be_three()`  | 用來事先判斷這個 string 在這一格的時候可不可以做為 3 位數的 ip 的開頭（例如：254 是可以的，而 278 是不行的） |
    | `gen_ips()`       | 會呼叫 `gen_be_head()` 和 `gen_be_three()` 做 preprocessing ，再呼叫 `gen_dot_poses()` 來產生所有可能的 ip 並回傳。 |

  - `main.py`

    | function     | 作用                                       |
    | ------------ | ---------------------------------------- |
    | `joinchan()` | 給一個 channel string，就會 join 進去            |
    | `sendmsg()`  | 給定要送的 message，就會自動把 message 轉成 UTF-8 編碼，再 append 上 channel ，再 send 給 IRC server。 |
    | `ping()`     | 回應 IRC server 傳過來確認 robot 是否還是 alive 的 "PING"。 |
    | `main()`     | - join 到 config 裡面寫的 channel<br>- 不斷接收 IRC server 傳過來的訊息<br>- 辨識 "PING, PONG"<br>- 辨識使用者傳過來的指令，再一一照著 specification 的規定回應。 |

## Challenge & Solution

- **Challenge** : 如果一次傳出去很多資訊的時候，有可能會被判定為 flooding ，導致有一些資料沒有成功傳出去。

  **Solution** : 在傳訊息出去之前，先 `sleep` 一個夠長並 `random` 的秒數，避免被判為洗版。

- **Challenge** : 在跟 IRC "PING, PONG" 之後，傳進 channel 的第一個訊息不會被送進 channel 裡面。

  **Solution** : 在跟 IRC "PING, PONG" 之後，馬上傳一個隨便的字串到 channel ，所以在這之後的訊息就會被正常送進 channel 裡面了。

## Reflections about this homework

我在測試自己的程式的時候，發現如果輸入不是 spec 裡面規定的格式的 string 時，程式很容易就會死掉。雖然助教有說不會測試奇怪的測資，但是如果真的要寫關於網路的程式的話，我想，應該要很小心使用者可能會輸入奇怪的字串。

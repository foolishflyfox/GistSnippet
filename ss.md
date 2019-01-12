1. 安装服务：

```shell
wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks.sh
chmod +x shadowsocks.sh
./shadowsocks.sh 2>&1 | tee shadowsocks.log
```

2. 加速1

  - `echo "echo 3 > /proc/sys/net/ipv4/tcp_fastopen" >> /etc/rc.local`
  - `echo "net.ipv4.tcp_fastopen = 3" >> /etc/systcl.conf`
  - 将 /etc/shadowsocks.json 中的 `"fast_open":false` 修改为 `"fast_open":true`
  - 如果希望多用户一起使用可以将 /etc/shadowsocks.json 的内容改成像下面类似的形式：
```json
{
    "server":"0.0.0.0",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "port_password":{
        "12345":"password1",
        "22345":"password2",
        "33345":"password3"
    },
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":true
}
```
  - 重启ss服务：`/etc/init.d/shadowsocks restart`

3. 用 BBR 加速

3.1 在 ubuntu 16.04 下安装

- 检测 BBR 是否开启 `sysctl net.ipv4.tcp_available_congestion_control`
如果是：`net.ipv4.tcp_available_congestion_control = cubic reno`就是没有开启

- 再次确认：`sysctl net.ipv4.tcp_congestion_control`
输出为：`net.ipv4.tcp_congestion_control = cubic`

- BBR 只能配合 Linux Kernel 4.10 以上的版本，通过 `uname -a` 可以查看内核版本，如果内核版本低于 4.10，就需要安装更新的内核；
安装新内核可以使用命令：`sudo apt-get install linux-generic-hwe-16.04`，重启后再看内核版本应该就满足要求了

- 启动 BBR 服务：`sudo modprobe tcp_bbr; echo "tcp_bbr" | sudo tee -a /etc/modules-load.d/modules.conf`
再检测BBR是否开启:`sysctl net.ipv4.tcp_congestion_control`，应该输出为：`net.ipv4.tcp_congestion_control = bbr`
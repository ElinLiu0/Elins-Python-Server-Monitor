from datetime import date, datetime
import os
import streamlit.components.v1 as components
from numpy.core.numeric import full
from cpu_warrning import ACCOUNT, HTML, PASSWORD
from mem_warning import HTML_MEM
from rich import console
print("[{}] [INFO] Loading For Dependcies Libraries...".format(datetime.now()))
try:
    import sys
    from time import sleep, time
    import psutil
    import streamlit as st
    from psutil import *
    import pandas as pd
    import platform
    import pycuda.driver as drv
    import plotly as py
    import plotly.graph_objs as go
    import os
    import getpass
    #import pycuda as drv
    from rich.console import Console
    import smtplib
    from email.mime.text import MIMEText
    from urllib.request import urlopen
    import subprocess
except Exception as Error:
    print("[{}] [ERROR] During Loading Dependcies Libraries,There was Error Occured In your system : \n {}".format(datetime.now(),Error))
console = Console()
system_kernel = platform.system()
console.print("[{}] [INFO] Monitor Services Were Successful Run!".format(datetime.now()),style="bold green")
if system_kernel == "Linux":
    console.print("[{}] [INFO] Enitity Last Login at {}".format(datetime.now(),os.popen("last login").readlines()),style="bold green")
    subprocess.run("ttyd bash")
console.print("[{}] [INFO] Service Were Listening on Deafult port 8501,browse the working network adapter ip with port to check GUI interfaces.".format(datetime.now()),style="bold green")
console.print("[{}] [WARRNING] Detect System Kernel is {} and some functions will be run under {} mode.".format(datetime.now(),system_kernel,system_kernel),style="bold yellow")
#在这里使用set_page_config()方法定义APP在WEB浏览器上现实的标题和布局
st.set_page_config(page_title="Django实例--{}".format(platform.node()),
layout="wide")
#创建一个selectbox下拉菜单的实例，参数分别为盒子的名称以及其他监视对象的子菜单名称
if system_kernel == "Windows":
    st.warning("检测到当前系统内核为{}，因此部分功能无法正常工作！".format(system_kernel))
    console.print("[{}] [WARNING] Some functions would not be run on a {} entity,sorry.".format(datetime.now(),system_kernel),style="bold yellow")
sidebar = st.selectbox(
    "实例资源监视",
    ("基本信息","网络配置","基础监控","存储监控","进程监控","弹性用户组配置","弹性安全组","GPU管理","命令终端","登录记录")
)
try:
    if sidebar == "基本信息":
        #首先使用platform库下的system()方法获取到当前实例的运行系统内核  
        #写上标题，注意！：这个表题在前端显示的效果为H1，因此在落笔写标题的时候要慎重
        st.title("实例基本信息")
        #使用platform.node()方法获取当当前运行实例的名称
        st.write("设备名称：{}".format(platform.node()))
        # 需要申明：Linux端的返回数据和Windows端的并非相同，因此
        # 针对不同系统内核，你需要单独修改platform和psutil返回值
        # 的格式。本次APP将会以UBuntu系统下的情况为例。
        #检测到当前运行内核为Linux
        if system_kernel == "Linux":
            #使用platform.machine()方法，并截取字符串以获得到当前实例系统的运行位宽
            st.write("系统类型：{}{}位".format(system_kernel,platform.machine()[4:6]))
        #使用platform.platform()方法获取到当前实例下的系统版本
        st.write("系统版本：{}".format(platform.platform()))
        st.write("CPU物理内核数量：{}核心".format(cpu_count()//2))
        st.write("CPU逻辑内核数量：{}线程".format(cpu_count()))
        #因为当前的实例是运行在虚拟机上的，因此
        #platform.processor()方法返回的是x86_64
        #而该方法在实体机下的返回值则是：Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
        #可以看到在实体机下可以看到该实例下处理器的位宽，制造厂商，最大内核数以及步进（Stepping）
        st.write("CPU类型：{}".format(platform.processor()))
        #使用psutil.net_if_stats追踪到当前实例中连接到主网络的设备名称
        if system_kernel == "Linux":
            st.write("基础网路连接：{}".format(list(psutil.net_if_stats())[1]))
        if system_kernel == "Windows":
            st.write("基础网路连接：{}".format(list(psutil.net_if_stats())[0]))
        if system_kernel == "Linux":
            #使用psutil.net_if_addrs()获取对应设备的IP
            st.write("IP：{}".format(list(psutil.net_if_addrs().values())[1][0][1]))
        if system_kernel == "Windows":
            st.write("IP：{}".format(list(psutil.net_if_addrs().values())[1][1][1]))
        #以上两个方法的返回值都是列表，因此与要进行切分
    elif sidebar == "网络配置":
        
        #首先构建存放所有psutil模块下返回值的列表以供存储数据
        network_adpater_name = []
        network_adpater_isup = []
        network_adpater_workmode = []
        network_adpater_runspeed = []
        network_adpater_maximumtrans = []
        network_adpater_ip = []
        network_adpater_mac = []
        network_adpater_ipv6 = []
        network_adpater_netmask = []
        if system_kernel == "Linux":
            #使用循环遍历出当前实例下所有的网络设备
            for i in range(len(list(psutil.net_if_addrs()))):
                network_adpater_name.append(list(psutil.net_if_addrs())[i])
                network_adpater_isup.append(list(psutil.net_if_stats().values())[i][0])
                #需要声明：psutil模块对应网卡工作模式的定义有些特殊，其返回值为整数数据
                #当返回值为2时，代表当前网络设备处于全双工的工作模式
                #当返回值为1时，代表当前网络设备处于半双工的工作模式
                network_adpater_workmode.append(list(psutil.net_if_stats().values())[i][1])
                network_adpater_runspeed.append(str(list(psutil.net_if_stats().values())[i][2])+"Mbps")
                network_adpater_maximumtrans.append(list(psutil.net_if_stats().values())[i][3])
                network_adpater_ip.append(list(psutil.net_if_addrs().values())[i][0][1])
                network_adpater_ipv6.append(list(psutil.net_if_addrs().values())[i][1][1])
                network_adpater_netmask.append(list(psutil.net_if_addrs().values())[i][0][2])
        if system_kernel == "Windows":
            #使用循环遍历出当前实例下所有的网络设备
            for i in range(len(list(psutil.net_if_addrs()))):
                network_adpater_name.append(list(psutil.net_if_addrs())[i])
                network_adpater_isup.append(list(psutil.net_if_stats().values())[i][0])
                #需要声明：psutil模块对应网卡工作模式的定义有些特殊，其返回值为整数数据
                #当返回值为2时，代表当前网络设备处于全双工的工作模式
                #当返回值为1时，代表当前网络设备处于半双工的工作模式
                network_adpater_workmode.append(list(psutil.net_if_stats().values())[i][1])
                network_adpater_runspeed.append(str(list(psutil.net_if_stats().values())[i][2])+"Mbps")
                network_adpater_maximumtrans.append(list(psutil.net_if_stats().values())[i][3])
                network_adpater_ip.append(list(psutil.net_if_addrs().values())[i][1][1])
                network_adpater_mac.append(list(psutil.net_if_addrs().values())[i][0][1])
                try:
                    network_adpater_ipv6.append(list(psutil.net_if_addrs().values())[i][2][1])
                except Exception:
                    network_adpater_ipv6.append(None)
                network_adpater_netmask.append(list(psutil.net_if_addrs().values())[i][1][2])
        #这里必须要用Pandas构建一个数据框，否则会很难看
        network_adpater_info = pd.DataFrame()
        network_adpater_info["网卡名称"] = network_adpater_name
        network_adpater_info["上行"] = network_adpater_isup
        network_adpater_info["工作模式"] = network_adpater_workmode
        network_adpater_info["运行速率"] = network_adpater_runspeed
        network_adpater_info["最大并行转发量"] = network_adpater_maximumtrans
        network_adpater_info["网卡IP"] = network_adpater_ip
        network_adpater_info["IPv6地址"] = network_adpater_ipv6
        if system_kernel == "Windows":
            network_adpater_info["MAC地址"] = network_adpater_mac
        network_adpater_info["子网掩码"] = network_adpater_netmask
        st.title("当前Django实例网络配置信息")
        #使用StreamlitAPI下的table()方法将DataFrame数据框渲染出来
        st.table(network_adpater_info)
    elif sidebar=="基础监控":
        #定义监视器函数并返回占用比
        def CPUMonitorWatchDog():
            usage = []
            while True:
                #在这里因为使用from pustil import *的引入方法
                #因此这里的cpu_percent不需要声明属于那个类下的
                #参数：interval=int用于设置psutil模块获取CPU占比的间隔
                #percpu：用于控制psutil模块在获取占用时是否将内核进行拆分
                usage.append(cpu_percent(interval=1, percpu=False))
                return usage
        def MemMonitorWatchDog():
            mem_usage = []
            while True:
                mem_usage.append(virtual_memory().percent)
                return mem_usage
        def readDiskWatchDog():
            read_speed = []
            while True:
                read_speed.append(psutil.disk_io_counters().read_bytes/1024/100)
                return read_speed
        def writeDiskWatchDog():
            write_speed = []
            while True:
                write_speed.append(disk_io_counters().write_bytes/1024/100)
                return write_speed
        def DownLoadNetMonitorWatchDog():
            download_speed = []
            while True:
                #这里net_ip_counters()中所有的返回值都是bit，因此无需转换为Byte
                #以保证
                first_recv = net_io_counters().bytes_recv
                sleep(1)
                second_recv = net_io_counters().bytes_recv
                download_speed.append((second_recv - first_recv))
                return download_speed
        def UPLoadNetMonitorWatchDog():
            upload_speed = []
            while True:
                first_sent = net_io_counters().bytes_sent
                sleep(1)
                second_sent = net_io_counters().bytes_sent
                upload_speed.append((second_sent - first_sent))
                return upload_speed
        def PackageSentMonitor():
            sent_pack = []
            while True:
                sent_pack.append(net_io_counters().packets_sent)
                return sent_pack
        def PackageReceiveMonitor():
            sent_pack = []
            while True:
                sent_pack.append(net_io_counters().packets_sent)
                return sent_pack
        #构建数据框以实时存储监视器们返回的数据
        df = pd.DataFrame(CPUMonitorWatchDog())
        #设置列长更新，以保证长度Y轴长度能够实时更新
        monitor_columns = [f"CPU占用率" for i in range(len(df.columns))]
        df.columns = monitor_columns  
        df["内存占用"] = MemMonitorWatchDog()
        df['读取速度'] = readDiskWatchDog()
        df["写入速度"] = writeDiskWatchDog()
        df["下载速度"] = DownLoadNetMonitorWatchDog()
        df["上传速度"] = UPLoadNetMonitorWatchDog()
        df["发包数量"] = PackageSentMonitor()
        df["接受包数量"] = PackageReceiveMonitor()
        #st.subheader()方法用于生成子标题，对应HTML中的h3标签
        first_header = st.subheader("CPU占用率")
        #使用st.area_chart()生成一个折线面积图的实例
        monitor_chart = st.area_chart(df[monitor_columns])
        second_header = st.subheader("内存占用率")
        mem_usage_charts= st.area_chart(df["内存占用"])
        third_header = st.subheader("磁盘读取速度(KB/s)")
        read_bytes_charts = st.area_chart(df["读取速度"])
        fourth_headers = st.subheader("磁盘写入速度(KB/s)")
        write_bytes_chart = st.area_chart(df['写入速度'])
        fivth_headers = st.subheader("下载速度(kb/s)")
        download_charts = st.area_chart(df["下载速度"])
        sixth_headers = st.subheader("上传速度(kb/s)")
        upload_charts = st.area_chart(df["上传速度"])
        seventh_headers = st.subheader("收包数量（个）")
        packrecv_charts = st.area_chart(df["接受包数量"])
        eighth_headers = st.subheader("发包数量")
        packsent_charts = st.area_chart(df["发包数量"])
        #开始进行数据迭代与填充
        while True:
            #因为每一个chart的类型属于DeletaGenerator对象，在Steamlit的API下
            #可以使用.add_rows()的方法拓宽数据，在参数中声明一个DataFrame和对应列以构建数据流
            try:
                monitor_chart.add_rows(pd.DataFrame(CPUMonitorWatchDog(), columns=monitor_columns))
                mem_usage_charts.add_rows(pd.DataFrame(MemMonitorWatchDog(),columns=["内存占用"]))
                read_bytes_charts.add_rows(pd.DataFrame(readDiskWatchDog(),columns=["读取速度"]))
                write_bytes_chart.add_rows(pd.DataFrame(writeDiskWatchDog(), columns=['写入速度']))
                download_charts.add_rows(pd.DataFrame(DownLoadNetMonitorWatchDog(),columns=["下载速度"]))
                upload_charts.add_rows(pd.DataFrame(UPLoadNetMonitorWatchDog(),columns=["上传速度"]))
                packrecv_charts.add_rows(pd.DataFrame(PackageReceiveMonitor(),columns=["接受包数量"]))
                packsent_charts.add_rows(pd.DataFrame(PackageSentMonitor(),columns=["发包数量"]))
            except Exception as Error:
                print("[{}] [ERROR] During Psutil Moudle Capturing Entity Source,There was an error occured :\n{}".format(Error))
                break
        #创建过载记录变量
        cpu_overload_times = 0
        #检测WatchDog()返回占用率超过90%时
        if CPUMonitorWatchDog() > 90:
            cpu_overload_times += 1
            if cpu_overload_times >= 20:
                #构建Email数据
                msg = MIMEText(HTML,"html")
                msg["to"] = ""
                msg["from"] = ACCOUNT
                msg["subject"] = "实例超载警告！"
                try:
                    #启动SMTP实例
                    server = smtplib.SMTP()
                    #连接服务器
                    server.connect("smtp.qq.com")
                    server.login(ACCOUNT,PASSWORD)
                    #发送邮件体
                    server.sendmail(msg["from"],msg["to"].split(","),msg.as_string())
                    #登出SMTP服务器
                    server.quit()
                    console.print("[{}] [INFO] A warning Email Has Been Sent On your Target Address,Please Check out the enityt status!".format(datetime.now()),style="bold yellow")
                except Exception as Error:
                    console.print("[{}] [ERROR] Failed to Build SMTP Connections to target SMTP Server!".format(datetime.now()))
            else:
                overload_times = 0
        else:
            pass
        mem_overload_times = 0
        if MemMonitorWatchDog() > 90:
            mem_overload_times += 1
            if mem_overload_times >= 20:
                #构建Email数据
                msg = MIMEText(HTML_MEM,"html")
                msg["to"] = ""
                msg["from"] = ACCOUNT
                msg["subject"] = "实例超载警告！"
                try:
                    #启动SMTP实例
                    server = smtplib.SMTP()
                    #连接服务器
                    server.connect("smtp.qq.com")
                    server.login(ACCOUNT,PASSWORD)
                    #发送邮件体
                    server.sendmail(msg["from"],msg["to"].split(","),msg.as_string())
                    #登出SMTP服务器
                    server.quit()
                    console.print("[{}] [INFO] A warning Email Has Been Sent On your Target Address,Please Check out the enityt status!".format(datetime.now()),style="bold yellow")
                except Exception as Error:
                    console.print("[{}] [ERROR] Failed to Build SMTP Connections to target SMTP Server!".format(datetime.now()))
            else:
                mem_overload_times = 0
        else:
            pass
    elif sidebar == "存储监控":
        #使用disk_usage()方法获取到指定盘符下的磁盘容量
        st.header("当前Django实例存储总量：{}".format(round(disk_usage("/").total/1024/1024/100,2))+"GB")
        #使用disk_partitions()方法获取到当前实例下的所有分区
        st.header("共有{}个分区".format(len(psutil.disk_partitions())))
        total_partitions = []
        each_partion_usage = []
        total_space = []
        used_space = []
        free_space = []
        #通过循环显示出实例下所有的分区，极其名称和占比
        #由于这个APP运行在了虚拟机上，而且虚拟磁盘是被拆分开来的，因此显示时只会获得所有虚拟分区
        for i in range(len(psutil.disk_partitions())):
            total_partitions.append(psutil.disk_partitions()[i].device)
            each_partion_usage.append(disk_usage(psutil.disk_partitions()[i].device).percent)
            total_space.append(round(disk_usage(psutil.disk_partitions()[i].device).total/1024/1024/1024,2))
            used_space.append(round(disk_usage(psutil.disk_partitions()[i].device).used/1024/1024/1024,2))
            free_space.append(round(disk_usage(psutil.disk_partitions()[i].device).free/1024/1024/1024,2))
        #创建一个plotly离线对象用于绘制分区占比
        pyplt = py.offline.plot
        labels = total_partitions
        values = each_partion_usage
        trace = [go.Pie(
        labels = labels, 
        values = values, 
        hole =  0.7,
        hoverinfo = "label + percent")]
        layout = go.Layout(
            title = "当前实例硬盘分区占比"
        )
        fig = go.Figure(data=trace,layout=layout)
        #调用streamlitAPI下的plotly_chart将之前plotly生成的figure写入到streamlit中
        st.plotly_chart(figure_or_data=fig,use_container_width=True)
        #创建数据框以显示实例下的磁盘信息
        df = pd.DataFrame()
        df["分区名称"] = total_partitions
        df["占用率"] = each_partion_usage
        df["总空间"] = total_space
        df["使用空间"] = used_space
        df["可用空间"] = free_space
        df["占用率"] = df["占用率"].apply(lambda x:str(x)+"%")
        df["总空间"] = df["总空间"].apply(lambda x:str(x)+"GB")
        df["使用空间"] = df["使用空间"].apply(lambda x:str(x)+"GB")
        df["可用空间"] = df["可用空间"].apply(lambda x:str(x)+"GB")
        st.subheader("实例磁盘详细信息")
        st.table(df)
        #捕获读写IOPs
        def readIOPsWatchDog():
            read_iops = []
            while True:
                read_iops.append(psutil.disk_io_counters().read_count)
                return read_iops
        def writeIPOsWatchDog():
            write_iops = []
            while True:
                write_iops.append(psutil.disk_io_counters().write_count)
                return write_iops
        df = pd.DataFrame(readIOPsWatchDog())
        readiops_columns = [f"顺序随机读取性能（IOPs）" for i in range(len(df.columns))]
        df.columns = readiops_columns 
        df["顺序随机写入性能（IOPs）"] = writeIPOsWatchDog()
        first_header = st.subheader("顺序随机读取性能（IOPs）")
        readiops_charts= st.area_chart(df["顺序随机读取性能（IOPs）"])
        second_header = st.subheader("顺序随机写入性能（IOPs）")
        writeiops_charts = st.area_chart(df["顺序随机写入性能（IOPs）"])
        while True:
            readiops_charts.add_rows(pd.DataFrame(readIOPsWatchDog(),columns=["顺序随机读取性能（IOPs）"]))
            writeiops_charts.add_rows(pd.DataFrame(writeIPOsWatchDog(),columns=["顺序随机写入性能（IOPs）"]))
    elif sidebar == "弹性安全组":
        #需额外声明，因终端输出值为一个极其不规则的值，因此无法实现十分规整的展示
        #因此如果想查看完整的安全组信息需要仍然在shell内执行
        with st.beta_expander("额外声明！"):
            st.write("如欲获得完整组策略信息，请使用命令终端或服务器Shell端进行查询")
        #设置两个分列
        sidebars = st.sidebar.radio(
            "执行操作",
            (
                "添加规则配置",
                "删除规则配置"
            )
        )
        if sidebars == "添加规则配置":
            st.subheader("添加规则配置")
            rule_type = st.text_input("规则类型")
            port_rule = st.text_input("端口规则")
            add_button = st.button("确认添加")
            if add_button:
                try:
                    os.popen("sudo ufw {} {}".format(rule_type,port_rule))
                    console.print("[{}] [INFO] Port Rule has been successfully add in your entity.".format(datetime.now()),style="bold green")
                    st.success("添加成功！")
                except Exception as Error:
                    console.print("[{}] [ERROR] There was an issuse when fixing the port rules on your entity :\n{}".format(datetime.now(),Error),style="bold red")
                    st.error("配置实例规则时发生异常，请重试！")
        if sidebars == "删除规则配置":
            st.subheader("删除规则配置")
            port_rule = st.text_input("端口规则")
            del_button = st.button("确认删除")
            if del_button:
                try:
                    os.popen("sudo ufw delete {}".format(port_rule))
                    console.print("[{}] [INFO] Port Rules has been Successful Delete",style="bold green")
                    st.success("删除成功！")
                except Exception as Error:
                    print("[{}] [ERROR] There was an issuse when fixing the port rules on your entity :\n{}".format(datetime.now(),Error))
                    st.error("配置实例规则时发生异常，请重试！")
    elif sidebar == "GPU管理":
        st.title("GPU技术由NVIDIA提供",st.image("https://developer.nvidia.com/sites/all/themes/devzone_new/favicon.ico"))
        try:
            #用pycuda.driver()方法初始化pycuda实例
            print("[{}] [INFO] Initializing Pycuda Driver through Python Libraries...".format(datetime.now()))
            drv.init()
            print("[{}] [INFO] Scanning NVIDIA CUDA™ GPUS...".format(datetime.now()))
            #当driver检测设备时
            if drv.Device.count() != 0:
                #显示当前实例装载了多少个CUDA GPU
                st.header("当前实例装载了{}个CUDA GPU.".format(drv.Device.count()))
                #构建CUDA设备信息存放数据的列表
                cuda_device_name = []
                cuda_device_capability = []
                cuda_device_memory = []
                cuda_device_rundriver = []
                #循环输出CUDA信息并填充至之前构建的列表中
                for i in range(drv.Device.count()):
                    device = drv.Device(i)
                    cuda_device_name.append(device.name())
                    cuda_device_capability.append(float("%d.%d" % device.compute_capability()))
                    gpu_memory = str(device.total_memory()//(1024**2)//1024)+"GB"
                    cuda_device_memory.append(gpu_memory)
                    cuda_device_rundriver.append(drv.get_version()[0])
                #构建数据框
                df = pd.DataFrame()
                df["CUDA设备名称"] = cuda_device_name
                df["CUDA设备计算能力"] = cuda_device_capability
                df["CUDA设备内存容量"] = cuda_device_memory
                df["CUDA驱动版本"] = cuda_device_rundriver
                #使用table()方法显示出来
                st.table(df)
            else:
                print("[{}] [WARNING] The Current Entity Has Not load a NVIDIA CUDA™ GPU!")
                st.error("当前Django服务器未装载GPU！")
        except Exception as Error:
            print("[{}] [ERROR] During Scanning NVIDIA GPU`S,The app has not load a runable driver!")
    elif sidebar == "进程监控":
        drop = st.sidebar.text_input(
            "清理进程(请输入PID)"
        )
        try:
            print("[{}] [INFO] Reading Process Through Memory...".format(datetime.now()))
            total = list(psutil.process_iter())
        except Exception as Error:
            st.error("加载了无法识别PID的目标进程！请尝试重新访问内存！")
            print("""[{}] [ERROR] During Scaning Merroy,There Was an unknown PID Progress has been loaded.
                Checkout Current Running Progresses and Rescaning Memory!
                """)
        pid = []
        name = []
        status = []
        for i in range(len(total)):
            pid.append(total[i].pid)
            name.append(total[i].name())
            if total[i].status() == "running":
                status.append("正在运行")
            if total[i].status() == "sleeping":
                status.append("休眠中")
            if total[i].status() == "disk_sleep":
                status.append("磁盘休眠中")
            if total[i].status() == "stopped":
                status.append("已终止")
            if total[i].status() == "tracing_stop":
                status.append("停止追踪")
            if total[i].status() == "zombie":
                status.append("僵尸进程")
            if total[i].status() == "dead":
                status.append("凋亡进程")
            if total[i].status() == "wake_kill":
                status.append("可被终止进程")
            if total[i].status() == "waking":
                status.append("唤醒中")
            if total[i].status() == "parked":
                status.append("延迟进程")
            if total[i].status() == "idle":
                status.append("游离进程")
            if total[i].status() == "locked":
                status.append("锁定进程")
            if total[i].status() == "waiting":
                status.append("等待进程")
            if total[i].status() == "suspended":
                status.append("延迟进程")
        df = pd.DataFrame()
        df["PID"] = pid
        df["进程名称"] = name
        df["进程状态"] = status
        # df["启动时间"] = started
        #创建一个plotly离线对象用于绘制分区占比
        pyplt = py.offline.plot
        labels = df["进程状态"].groupby(df["进程状态"]).count().index.tolist()
        values = df["进程状态"].groupby(df["进程状态"]).count().values.tolist()
        trace = [go.Pie(
        labels = labels, 
        values = values, 
        hole =  0.7,
        hoverinfo = "label + value")]
        layout = go.Layout(
            title = "当前实例进程状态"
        )
        fig = go.Figure(data=trace,layout=layout)
        #调用streamlitAPI下的plotly_chart将之前plotly生成的figure写入到streamlit中
        st.plotly_chart(figure_or_data=fig,use_container_width=True)
        st.table(df)
        if len(drop) != 0:
            second_confirm_drop = st.sidebar.text_input(
                "二次确认（请输入PID）"
            )
            if second_confirm_drop == drop:
                if system_kernel == "Linux":
                    try:
                        os.system("sudo kill -9 {}".format(drop))
                        console.print("[{}] [INFO] PID={} progress has been successfully kiled!".format(datetime.now(),drop),style="bold green")
                        st.success("进程已被终止！")
                    except Exception as Error:
                        console.print("[{}] [ERROR] There was error during killing PID={} progress,try again later!".format(datetime.now(),drop),style="bold red")
                        st.error("终止进程时发生异常！请重试！")
                if system_kernel == "Windows":
                    try:
                        os.system("taskkill -F /pid {}".format(drop))
                        console.print("[{}] [INFO] PID={} progress has been successfully kiled!".format(datetime.now(),drop),style="bold green")
                        st.success("进程已被终止！")
                    except Exception as Error:
                        console.print("[{}] [ERROR] There was error during killing PID={} progress,try again later!".format(datetime.now(),drop),style="bold red")
                        st.error("终止进程时发生异常！请重试！")
    elif sidebar == "命令终端":
        
        side_button_shutdown = st.sidebar.button("终止实例运行")
        side_button_reboot = st.sidebar.button("重启实例")
        run_full_terminal = st.sidebar.button("启动完整终端")
        user_command = st.text_input(getpass.getuser()+"@"+platform.node()+":"+ os.path.expanduser('~'))
        process = os.popen(user_command)
        result = process.read()
        back = st.text_area("运行结果",value=result,height=500)
        if side_button_shutdown:
            if system_kernel == "Linux":
                os.system("sudo poweroff")
            if system_kernel == "Windows":
                os.system("shutdown -s -t 0")
        if side_button_reboot:
            if system_kernel == "Linux":
                os.system("sudo reboot")
            if system_kernel == "Windows":
                os.system("shutdown -r -t 0")
        if run_full_terminal:
            main_ip = list(psutil.net_if_addrs().values())[1][0][1]
            components.iframe(src="http://{}:7681/".format(main_ip),height=500)
    elif sidebar == "弹性用户组配置":
        #先检测一下系统内核
        
        #当系统内核检测为Linux时则执行如下逻辑
        if system_kernel == "Linux":
            st.title("当前实例用户组配置信息")
            #读取/etc/group下的分组信息
            process = os.popen("sudo cat /etc/group").readlines()
            print("[{}] [INFO] Reading System Group Info...".format(datetime.now()))
            #创建四个列表用于存储分列数据
            group_name = []
            group_key = []
            gid = []
            user_list = []
            #开始分列
            for line in process:
                group_name.append(line.replace("\n","").split(":")[0])
                group_key.append(line.replace("\n","").split(":")[1])
                gid.append(line.replace("\n","").split(":")[2])
                user_list.append(line.replace("\n","").split(":")[3])
            #创建数据框
            df = pd.DataFrame()
            df["组名称"] = group_name
            df["组密钥"] = group_key
            df["GID"] = gid
            df["用户群"] = user_list
            st.table(df)
            #创建一个侧边栏用于存放按钮
            sidebars = st.sidebar.radio(
                "执行操作",
                (
                    "添加用户组",
                    "删除用户组",
                    "添加用户",
                    "删除用户"
                )
            )
            #当按钮被按下时
            if sidebars == "添加用户组":
                #使用text_input()方法创建一个输入框用于记录添加的用户组名
                add_confirm = st.text_input("请输入你想添加的用户组")
                #当前长度不等于0时
                if len(add_confirm) != 0:
                    #如果添加的
                    if add_confirm in df["组名称"].values:
                        console.print("[{}] [ERROR] This group were exists on this entity!".format(datetime.now()),style="bold red")
                        st.error("该用户组已存在，无法再次添加")
                    else:
                        os.popen("sudo groupadd {}".format(add_confirm))
                        console.print("[{}] [INFO] Group {} has been successful add on entity!".format(datetime.now(),add_confirm),style="bold green")
                        st.success("添加成功")
            if sidebars == "删除用户组":
                delete_confirm = st.text_input("请确认你删除的用户组对象名称")
                if len(delete_confirm) != 0:
                    #生成一个警告信息
                    st.warning("该操作会影响实例系统下的用户组信息，请输入：我已知晓后果，并承担风险方可执行该操作！")
                    #进行最终确认以防止误删
                    final_confirm = st.text_input(label="最终确认")
                    if final_confirm == "我已知晓后果，并承担风险方可执行该操作":
                        if delete_confirm in df["组名称"].values:
                            os.popen("sudo groupdel {}".format(delete_confirm))
                            console.print("[{}] [INFO] Group {} has been successful moved on entity!".format(datetime.now(),add_confirm),style="bold green")
                            st.success("删除成功")
                        else:
                            st.error("请确认该用户组是否存在")
                            console.print("[{}] [ERROR] Does this Group has been exists on this entity?Please Confirm it and try again!".format(datetime.now()),style="bold red")
            if sidebars == "添加用户":
                add_user_confirm = st.text_input("请输入你想添加的用户")
                if len(add_user_confirm) != 0:
                    all_user = []
                    for i in range(len(df["用户群"])):
                        single_group = df["用户群"][i].split(",")
                        for i in range(len(single_group)):
                            all_user.append(single_group[i])
                    if add_user_confirm in all_user:
                        console.print("[{}] [ERROR] This User has been exists on this Entity!".format(datetime.now()),style="bold red")
                        st.error("无法添加！目标用户已存在！")
                    else:
                        os.popen("sduo adduser {}".format(add_user_confirm))
                        console.print("[{}] [INFO] User {} has been successful add on this entity".format(datetime.now(),add_user_confirm),style="bold green")
            if sidebars == "删除用户":
                delete_user_confirm = st.text_input("请输入你想删除的用户")
                if len(delete_user_confirm) != 0:
                    st.warning("该操作会影响实例系统下的用户组信息，请输入：我已知晓后果，并承担风险方可执行该操作！")
                    final_confirm = st.text_input(label="最终确认")
                    if final_confirm == "我已知晓后果，并承担风险方可执行该操作":
                        if delete_user_confirm in all_user:
                            try:
                                os.popen("sudo userdel --remove {}".format(delete_user_confirm))
                                console.print("[{}] [INFO] User {} has been moved from entity",style="bold green")
                                st.success("删除成功")
                            except Exception as Error:
                                console.print("[{}] [ERROR] During Removing User {},There was an unexcepted error occured".format(datetime.now(),delete_confirm),style="bold red")
                                st.error("删除用户时发生异常，请重试！")
                        else:
                            st.error("请确认该用户组是否存在")
    elif sidebar == "登录记录":
        system_kernel = platform.system()
        if system_kernel == "Linux":
            result = os.popen("last").readlines()
            login = []
            for i in range(len(result)):
                login.append(result[i].strip())
            df = pd.DataFrame()
            df["记录"] = login
            st.subheader("共有{}条登录记录".format(len(result)))
            st.table(df)
    console.print("[{}] [INFO] Functions Tree Has Successfully Load UP.".format(datetime.now()),style="bold green")
except Exception as Error:
    st.error("加载功能树时发生异常！请重试")
    console.print("[{}] [ERROR] During Loading a Child Function,There was an Error occured :\n{}".format(datetime.now(),Error),style="bold red")
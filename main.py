import tkinter as tk
from tkinter import scrolledtext
import wmi
import GPUtil
from screeninfo import get_monitors
from tkinter import ttk

import sv_ttk

# 初始化WMI
c = wmi.WMI()


# 定义系统信息获取函数
def get_cpu_info():
    cpus = c.Win32_Processor()
    cpu_info = []
    for cpu in cpus:
        cpu_info.append(f"名称: {cpu.Name.strip()}")
        cpu_info.append(f"核心数: {cpu.NumberOfCores}")
        cpu_info.append(f"线程数: {cpu.ThreadCount}")
        cpu_info.append(f"最大时钟频率: {cpu.MaxClockSpeed}MHz")
    return '\n'.join(cpu_info)


def get_memory_info():
    memories = c.Win32_PhysicalMemory()
    memory_info = []
    for mem in memories:
        memory_info.append(f"容量: {float(mem.Capacity) / (1024 ** 3):.2f}GB")
        memory_info.append(f"速度: {mem.Speed}MHz")
        memory_info.append(f"制造商: {mem.Manufacturer}")
        memory_info.append(f"数据宽度: {mem.DataWidth} bits")
    return '\n'.join(memory_info)


def get_monitor_info():
    monitors = get_monitors()
    monitor_info = []
    for m in monitors:
        monitor_info.append(f"名称: {m.name}")
        monitor_info.append(f"宽度: {m.width}px")
        monitor_info.append(f"高度: {m.height}px")
        monitor_info.append(f"坐标: x={m.x}, y={m.y}")
        if hasattr(m, 'width_mm'):
            monitor_info.append(f"物理宽度: {m.width_mm}mm")
        if hasattr(m, 'height_mm'):
            monitor_info.append(f"物理高度: {m.height_mm}mm")
    return '\n'.join(monitor_info)


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append(f"名称: {gpu.name}")
        gpu_info.append(f"总显存: {gpu.memoryTotal}MB")
        gpu_info.append(f"空闲显存: {gpu.memoryFree}MB")
        gpu_info.append(f"使用中显存: {gpu.memoryUsed}MB")
        gpu_info.append(f"温度: {gpu.temperature}°C")
    return '\n'.join(gpu_info)


def get_disk_info():
    disks = c.Win32_DiskDrive()
    disk_info = []
    for disk in disks:
        disk_info.append(f"名称: {disk.Caption}")
        disk_info.append(f"型号: {disk.Model}")
        disk_info.append(f"接口类型: {disk.InterfaceType}")
        disk_info.append(f"媒体类型: {disk.MediaType}")
        disk_info.append(f"总大小: {int(disk.Size) / (1024 ** 3):.2f}GB")
    return '\n'.join(disk_info)


def get_sound_info():
    sounds = c.Win32_SoundDevice()
    sound_info = ["{0}".format(sound.Name) for sound in sounds]
    return '\n'.join(sound_info)


def get_network_info():
    adapters = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    network_info = []
    for adapter in adapters:
        network_info.append(f"名称: {adapter.Description}")
        network_info.append(f"物理地址: {adapter.MACAddress}")
        if adapter.IPAddress is not None:
            network_info.append(f"IP地址: {', '.join(adapter.IPAddress)}")
    return '\n'.join(network_info)


def get_system_info():
    system = c.Win32_ComputerSystem()[0]
    os = c.Win32_OperatingSystem()[0]
    system_info = [f"制造商: {system.Manufacturer}", f"型号: {system.Model}", f"系统类型: {system.SystemType}",
                   f"系统家族: {os.Caption}", f"版本: {os.Version}"]
    return '\n'.join(system_info)


class SystemInfoViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        sv_ttk.set_theme("light")
        self.title("Windows系统配置查看器")
        self.geometry("800x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # 创建总览标签页
        self.overview = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.overview, text="总览")

        # 添加其他标签页
        self.tabs = {}
        for name, func in (("CPU", get_cpu_info), ("内存", get_memory_info), ("GPU", get_gpu_info),
                           ("硬盘", get_disk_info), ("声卡", get_sound_info), ("网络", get_network_info),
                           ("系统", get_system_info)):
            tab = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
            info = func()
            tab.insert(tk.INSERT, info)
            tab['state'] = 'disabled'  # 只读
            self.tabs[name] = tab
            self.notebook.add(tab, text=name)
        monitor_tab = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        monitor_info = get_monitor_info()
        monitor_tab.insert(tk.INSERT, monitor_info)
        monitor_tab['state'] = 'disabled'  # 只读
        self.notebook.add(monitor_tab, text="显示器")
        about_tab = tk.Frame(self.notebook)
        about_text = tk.Label(about_tab,
                              text="系统配置查看\n\n本工具可以查看你的电脑硬件和软件信息。\n\n版本: 1.0\n作者: Choyeon\n联系方式: Choyeon@foxmail.com",
                              justify=tk.LEFT)
        about_text.pack(padx=20, pady=20)
        self.notebook.add(about_tab, text="关于")

        self.boot()

    def boot(self):
        # 在总览标签中收集所有信息
        overview_info = []
        for name, tab in self.tabs.items():
            info = tab.get("1.0", tk.END)
            overview_info.append(f"==={name}===\n{info}\n")
        self.overview.insert(tk.INSERT, ''.join(overview_info))
        self.overview['state'] = 'disabled'  # 只读


if __name__ == "__main__":
    app = SystemInfoViewer()
    app.mainloop()

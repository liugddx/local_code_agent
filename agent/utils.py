import sys
import time
import threading

class Spinner:
    """一个简单的命令行加载动画类"""

    def __init__(self, message="Processing", delay=0.1):
        self.spinner_chars = "|/-\\"
        self.delay = delay
        self.message = message
        self.running = False
        self.spinner_thread = None

    def _spin(self):
        """执行旋转动画"""
        idx = 0
        while self.running:
            try:
                sys.stdout.write(f"\r{self.message} {self.spinner_chars[idx % len(self.spinner_chars)]}")
                sys.stdout.flush()
                time.sleep(self.delay)
                idx += 1
            except Exception:
                # 忽略输出错误，继续运行
                pass

    def start(self):
        """开始动画"""
        if not self.running:
            self.running = True
            self.spinner_thread = threading.Thread(target=self._spin, daemon=True)
            self.spinner_thread.start()

    def stop(self):
        """停止动画"""
        if self.running:
            self.running = False
            if self.spinner_thread and self.spinner_thread.is_alive():
                self.spinner_thread.join(timeout=1.0)
            try:
                sys.stdout.write(f"\r{self.message} ✓\n")
                sys.stdout.flush()
            except Exception:
                # 忽略输出错误
                pass
    
    def __enter__(self):
        """进入上下文管理器"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        self.stop()
        # 不抑制异常，让异常继续传播
        return False

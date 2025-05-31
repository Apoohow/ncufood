import multiprocessing

# 工作進程數
workers = 1  # 在免費方案中使用單個工作進程
worker_class = 'gthread'  # 使用 gthread 工作進程
threads = 4  # 每個工作進程的線程數

# 綁定設定
bind = "0.0.0.0:10000"  # 明確指定綁定地址和端口

# 超時設定
timeout = 120  # 增加超時時間
graceful_timeout = 30
keepalive = 2  # 保持連接時間

# 記憶體相關
max_requests = 1000  # 工作進程處理多少請求後重啟
max_requests_jitter = 50  # 添加隨機性以避免同時重啟

# 日誌設定
accesslog = '-'
errorlog = '-'
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True

# 限制請求大小
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 工作進程設定
preload_app = True  # 預加載應用
worker_tmp_dir = '/dev/shm'  # 使用記憶體存儲臨時文件 
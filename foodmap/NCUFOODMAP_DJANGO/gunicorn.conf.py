import multiprocessing

# 工作進程數
workers = 1  # 在免費方案中使用單個工作進程
worker_class = 'sync'  # 使用同步工作進程
threads = 2  # 每個工作進程的線程數

# 超時設定
timeout = 120  # 增加超時時間
graceful_timeout = 30

# 記憶體相關
max_requests = 1000  # 工作進程處理多少請求後重啟
max_requests_jitter = 50  # 添加隨機性以避免同時重啟

# 日誌設定
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# 限制請求大小
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190 
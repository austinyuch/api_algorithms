dic_api = {
    "site_name":"iekchartsapi", 
    "description":"IEK Charts",
    "site_url":"http://localhost:2224",
    "api_url":"https://",
    # "version_note":"",
    # "last_update":"2021/08/05",
    "host": "localhost", #cloud server用0.0.0.0, # windows local不能用 0.0.0.0
    "port": 2224, 
    "reload": False, # 正式佈署時用False比較穩定
    "workers": 1, #開multiprocess
    "log_level": "debug", # debug, info, warning, error, critical
    "debug": True, # 正式佈署時用False比較安全,如果False, API開啟時會載入memory以加速後續讀取    
    }
GLOBAL_LOG_LEVEL="INFO"
lst_origins=["*"]
from pathlib import Path
PATH_PRJ = Path(__file__).resolve().parents[0]
PATH_LOG_FOLDER = PATH_PRJ.joinpath("logs")
LOG_BACKUP_COUNT = 14
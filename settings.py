import environ

root = environ.Path(__file__) - 1
ROOT_DIR = root
APPS_DIR = root


env = environ.Env(DEBUG=(bool, False))
# 不加的话默认是字符串
# 优先会使用环境变量作为配置

# env.read_env(root(env.str("ENV_PATH", ".env")))
env.read_env(root(".env"))

DEBUG = env("DEBUG")
LOG_LEVEL = env("LOG_LEVEL", default="")
ENV = env("ENV")
WECOM_CID = env("WECOM_CID")
WECOM_AID = env("WECOM_AID")
WECOM_SECRET = env("WECOM_SECRET")
sEncodingAESKey = env("sEncodingAESKey")
sToken = env("sToken")
TOUSER = env("TOUSER")
REMIND_USER = env("REMIND_USER")
MARK = env("MARK")
DB_PATH = env("DB_PATH")

import os, sys
sys.argv = ['streamlit']
from dotenv import load_dotenv
import streamlit as st

load_dotenv(override=True)

def get_key(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets[name]
    except Exception as e:
        print(f'  [except 捕获: {type(e).__name__}]')
        return None

# 场景1：环境变量有值（模拟本地 .env）
os.environ['FAKE_TOKEN'] = 'abc123'
print('场景1 本地.env路径:', get_key('FAKE_TOKEN'))

# 场景2：两处都没有（本地无 secrets.toml、无环境变量）
print('场景3 两处皆无:', get_key('NOT_EXIST'))
print('整体不崩溃: OK')

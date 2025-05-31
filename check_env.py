#!/usr/bin/env python3
"""
環境變數檢查腳本
用於驗證部署前的環境變數配置
"""

import os
import sys

def check_env_vars():
    """檢查必要的環境變數"""
    required_vars = {
        'SECRET_KEY': 'Django密鑰',
        'GOOGLE_OAUTH_CLIENT_ID': 'Google OAuth客戶端ID',
        'GOOGLE_OAUTH_CLIENT_SECRET': 'Google OAuth客戶端密鑰',
        'GOOGLE_MAPS_API_KEY': 'Google Maps API金鑰',
        'TOGETHER_API_KEY': 'Together AI API金鑰',
    }
    
    optional_vars = {
        'DEBUG': 'Debug模式（預設：True）',
        'DATABASE_URL': '資料庫URL（Render自動提供）',
    }
    
    print("🔍 檢查環境變數配置...")
    print("=" * 50)
    
    missing_vars = []
    
    # 檢查必要變數
    print("📋 必要環境變數:")
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # 隱藏敏感資訊
            if 'SECRET' in var or 'KEY' in var:
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: 未設定 ({description})")
            missing_vars.append(var)
    
    print("\n📋 可選環境變數:")
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️  {var}: 未設定 ({description})")
    
    print("\n" + "=" * 50)
    
    if missing_vars:
        print(f"❌ 缺少 {len(missing_vars)} 個必要環境變數:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n請在Render的Environment頁面設定這些變數。")
        return False
    else:
        print("✅ 所有必要環境變數都已設定！")
        print("🚀 可以開始部署了！")
        return True

if __name__ == "__main__":
    success = check_env_vars()
    sys.exit(0 if success else 1) 
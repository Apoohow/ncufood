# NCU 食物地圖 - Render 部署指南

## 部署步驟

### 1. 準備 GitHub 倉庫
1. 將專案推送到 GitHub
2. 確保所有文件都已提交

### 2. 在 Render 創建服務
1. 前往 [Render.com](https://render.com)
2. 註冊/登入帳號
3. 點擊 "New +" → "Web Service"
4. 連接您的 GitHub 倉庫

### 3. 配置 Web Service
- **Name**: `ncu-foodmap`
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn ncufoodmap_backend.wsgi:application`
- **Root Directory**: `foodmap/NCUFOODMAP_DJANGO`

### 4. 設定環境變數
在 Render 的 Environment 頁面添加以下環境變數：

#### 基本配置
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
```

#### API金鑰
```
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
TOGETHER_API_KEY=your-together-api-key
```

#### Google OAuth 配置（重要！）
```
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-oauth-client-secret
```

### 5. 更新Google OAuth設定
⚠️ **重要**：部署後需要更新Google Cloud Console設定
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇您的專案
3. 進入「APIs & Services」→「Credentials」
4. 編輯OAuth 2.0客戶端ID
5. 在「Authorized redirect URIs」添加：
   ```
   https://your-app-name.onrender.com/accounts/google/login/callback/
   ```
6. 在「Authorized JavaScript origins」添加：
   ```
   https://your-app-name.onrender.com
   ```

### 6. 資料庫設定
1. 在 Render 創建 PostgreSQL 資料庫
2. 複製 DATABASE_URL 到環境變數

### 7. 部署
1. 點擊 "Create Web Service"
2. 等待部署完成（約 5-10 分鐘）

## 部署後功能
✅ 跨裝置訪問
✅ Google OAuth 登入
✅ 即時聊天功能
✅ 社交功能完整運作
✅ 檔案上傳功能
✅ PostgreSQL 資料庫

## 注意事項
- 首次部署需要運行遷移
- 需要創建超級用戶帳號
- 媒體文件需要額外配置（建議使用 Cloudinary）
- **必須更新Google OAuth重定向URI**

## 測試部署
部署完成後，您可以：
1. 訪問您的 Render URL
2. 測試Google登入功能
3. 註冊新帳號測試功能
4. 邀請朋友測試跨裝置聊天

## 環境變數完整清單
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
TOGETHER_API_KEY=your-together-api-key
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-oauth-client-secret
DATABASE_URL=postgresql://... (由Render自動提供)
``` 
# Graph Report - .  (2026-04-10)

## Corpus Check
- 19 files · ~621,191 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 162 nodes · 369 edges · 21 communities detected
- Extraction: 49% EXTRACTED · 51% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TTSJob` - 32 edges
2. `TTSWorker` - 30 edges
3. `AudioInput` - 27 edges
4. `VADSegmenter` - 27 edges
5. `ASRWorker` - 26 edges
6. `RuleEngine` - 26 edges
7. `Orchestrator` - 24 edges
8. `AudioConfig` - 22 edges
9. `ASRResult` - 20 edges
10. `VADConfig` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Orchestrator` --uses--> `ASRResult`  [INFERRED]
  src\orchestrator.py → src\asr_worker.py
- `語音助理的核心協調器      說明：         Orchestrator 是整個語音助理的心臟，負責：         1. 管理所有子模組的生` --uses--> `ASRResult`  [INFERRED]
  src\orchestrator.py → src\asr_worker.py
- `設定系統狀態 (執行緒安全)          說明：             使用 Lock 保護 _state 變數，確保在多執行緒環境下` --uses--> `ASRResult`  [INFERRED]
  src\orchestrator.py → src\asr_worker.py
- `TTS 完成回調 - 當 TTS 播放完畢時呼叫          說明：             此函式由 TTSWorker 在語音播放完成後呼叫。` --uses--> `ASRResult`  [INFERRED]
  src\orchestrator.py → src\asr_worker.py
- `模擬語句 - 用於測試規則匹配和 TTS          說明：             此函式用於 Mock 模式下模擬語音輸入。` --uses--> `ASRResult`  [INFERRED]
  src\orchestrator.py → src\asr_worker.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (29): ASRResult, ASRWorker, 建構函式 - 建立 ASRWorker 實例          說明：             初始化 ASR Worker，設定模型路徑和回調函式。, 啟動 ASR Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。, 停止 ASR Worker          說明：             優雅地停止 worker 執行緒：             1. 設定停止, 語音辨識結果資料類別      說明：         封裝語音辨識的結果，包含識別出的文字及其他相關資訊。      屬性：         tr, 語音辨識工作者      說明：         負責將音訊資料轉換為文字的 worker 模組。         使用執行緒和佇列實現非同步處理：, AudioConfig (+21 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (16): TTS 完成回調 - 當 TTS 播放完畢時呼叫          說明：             此函式由 TTSWorker 在語音播放完成後呼叫。, 模擬語句 - 用於測試規則匹配和 TTS          說明：             此函式用於 Mock 模式下模擬語音輸入。, TTS 任務資料類別          說明：         封裝要送給 TTS Worker 的任務資料。         由 RuleEngine, TTSJob, 建構函式 - 建立 TTSWorker 實例          說明：             初始化 TTS Worker，設定模型路徑和回調函式。, 檢查是否正在說話          回傳：             bool: True = 正在朗讀, 取得說話事件物件          說明：             此 Event 會在開始說話時設為 True，說完後設為 False。, 啟動 TTS Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的朗讀任務。 (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (12): 語音助理的核心協調器      說明：         Orchestrator 是整個語音助理的心臟，負責：         1. 管理所有子模組的生, 規則引擎          說明：         負責管理所有規則的生命週期和匹配邏輯。         核心功能：         1. 從 JS, 建構函式 - 建立 RuleEngine 實例                  說明：             初始化規則引擎，設定規則檔路徑。, 載入規則檔                  說明：             從 JSON 檔案讀取規則定義，並轉換為 Rule 物件列表。, 檢查是否需要熱重載                  說明：             檢查規則檔是否被修改過，若是則自動重新載入。, 匹配規則                  說明：             根據輸入的文字匹配對應的規則。             匹配流程：, 規則資料類別          說明：         封裝單一規則的所有屬性，包含關鍵字、匹配模式、優先級、冷卻時間等。          屬性：, 檢查關鍵字是否匹配                  說明：             根據規則的 match_mode 欄位，選擇合適的匹配方式： (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (9): AudioInput, 建構函式 - 建立 AudioInput 實例                  說明：             初始化音訊輸入管理器，設定組態和回調函式, 列出所有可用的音訊裝置                  說明：             查詢並顯示系統中所有可用的音訊輸入和輸出裝置。, 啟動音訊串流，開始從麥克風擷取音訊                  說明：             建立 sounddevice InputStream, 停止音訊串流                  說明：             優雅地停止音訊串流並釋放資源。             此函式會：, 音訊資料回調 - sounddevice 每次收到新音訊時呼叫                  說明：             此函式由 soundde, 檢查音訊串流是否正在執行                  參數：             無                  回傳：, 音訊輸入管理器          說明：         負責與系統音訊驅動互動，從麥克風即時擷取音訊資料。         使用 sounddevic (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.24
Nodes (5): main(), parse_args(), 主程式進入點          說明：         此函式是程式的執行起點，負責以下任務：         1. 解析命令列參數, 解析命令列參數          說明：         此函式使用 argparse 模組解析命令列參數，讓使用者可以自訂程式行為，, Orchestrator

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (6): 處理單個音訊框架          說明：             這是 VAD 模組的核心函式，每次收到新的音訊資料時呼叫。, 簡單能量閾值 VAD          說明：             使用簡單的能量計算來判斷是否為語音。             計算音訊的 RMS, Silero VAD 語音活動檢測          說明：             使用 Silero AI 的預訓練 VAD 模型進行語音偵測。, 完成語句處理          說明：             當偵測到語句結束時呼叫此函式。             職責：, 重設內部狀態          說明：             清空緩衝區並重設所有計時器和狀態變數。             用於語句完成後或需要重新, 公開的重設函式          說明：             提供給外部呼叫的重設接口。             會先取得鎖再重設，確保執行緒安全。

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (2): BaseStreamer, TokenStreamer

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (2): Worker 執行緒主迴圈          說明：             在獨立執行緒中運行的主要工作迴圈：             1. 從輸入佇, 執行實際的語音辨識          說明：             這是核心的辨識函式，目前為預留實作：             - 若模型未載入，回

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (1): Logging configuration module

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): 提交音訊進行辨識          說明：             將音訊資料加入任務佇列，等待 worker 執行緒處理。             這

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): 載入 VAD 模型          說明：             嘗試載入 Silero VAD 模型。             若載入失敗 (缺少

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Voice Activated Assistant - Main Package

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): 計算每個音訊區塊的樣本數                  說明：             根據取樣率和區塊持續時間計算每次 Callback 應該處理的

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **42 isolated node(s):** `語音辨識結果資料類別      說明：         封裝語音辨識的結果，包含識別出的文字及其他相關資訊。      屬性：         tr`, `語音辨識工作者      說明：         負責將音訊資料轉換為文字的 worker 模組。         使用執行緒和佇列實現非同步處理：`, `建構函式 - 建立 ASRWorker 實例          說明：             初始化 ASR Worker，設定模型路徑和回調函式。`, `啟動 ASR Worker 執行緒          說明：             建立並啟動 worker 執行緒，開始處理任務佇列中的音訊任務。`, `停止 ASR Worker          說明：             優雅地停止 worker 執行緒：             1. 設定停止` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (2 nodes): `.process()`, `提交音訊進行辨識          說明：             將音訊資料加入任務佇列，等待 worker 執行緒處理。             這`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `bench_gpu.py`, `benchmark_gpu()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `check_speakers.py`, `check_speakers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `載入 VAD 模型          說明：             嘗試載入 Silero VAD 模型。             若載入失敗 (缺少`, `.load_vad()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `__init__.py`, `Voice Activated Assistant - Main Package`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `inspect_tts.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `inspect_tts_v2.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `list_files.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `setup_git_sync.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `test_opencc.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `計算每個音訊區塊的樣本數                  說明：             根據取樣率和區塊持續時間計算每次 Callback 應該處理的`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VADSegmenter` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 12`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Why does `RuleEngine` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `ASRWorker` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 7`, `Community 9`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `TTSJob` (e.g. with `State` and `OrchestratorConfig`) actually correct?**
  _`TTSJob` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `TTSWorker` (e.g. with `State` and `OrchestratorConfig`) actually correct?**
  _`TTSWorker` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `AudioInput` (e.g. with `解析命令列參數          說明：         此函式使用 argparse 模組解析命令列參數，讓使用者可以自訂程式行為，` and `主程式進入點          說明：         此函式是程式的執行起點，負責以下任務：         1. 解析命令列參數`) actually correct?**
  _`AudioInput` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `VADSegmenter` (e.g. with `State` and `OrchestratorConfig`) actually correct?**
  _`VADSegmenter` has 17 INFERRED edges - model-reasoned connections that need verification._
# 超簡易本地 LLM 對話教學! 🚀🤖

感謝大家使用本教學，這次帶給大家的是要如何在本地快速開啟一個聊天機器人應用，並且可以不用聯網的在本地對話，這對商業應用非常重要!!

## 安裝套件
1. Ollama : 開啟LLM對話必不可少的超簡單應用
2. Conda  : 環境安裝工具

## 下載LLM
```bash
ollama pull llama3.1
```
## 創建並且下載環境
```bash
conda create -n LLM python==3.10
conda activate LLM
pip install -r requirements.txt
```

## 執行APP
1. 簡單LLM
```python
chainlit run Chapter1_SimpleLocalLLM.py -w
```
2. 記憶LLM
```python
chainlit run Chapter2_MemorableLLM.py -w
```
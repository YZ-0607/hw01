## 任务完成情况
### 任务一：大模型生成文稿
- 标题：AI语音技术科普：从声音克隆到语音识别的全流程解析
- 使用模型：Kimi 月之暗面
- 生成日期：2026-03-26
- 文稿字数：约350字，满足作业要求

### 任务二：剪映声音克隆与语音合成
- 使用剪映专业版（PC）完成文本朗读
- 音频格式：MP3
- 音频存放路径：2_clone_audio/clone_voice.mp3
- 说明：已按要求完成配音导出

### 任务三：开源语音识别（ASR）
- 调研方案：Whisper、FunASR、Vosk 三种开源ASR方案
- 选型方案：OpenAI Whisper small（本地CPU运行）
- 实现功能：读取克隆音频完成语音识别
- 输出结果：识别文本保存至 asr_result.txt

## 运行方式
进入 3_asr 目录执行：
```bash
pip install -r requirements.txt
python main.py
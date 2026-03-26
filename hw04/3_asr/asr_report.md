# 开源语音识别(ASR)方案对比报告
测试环境：Windows 11、Python 3.10、CPU（无GPU）

## 一、对比方案（共3种）
1. OpenAI Whisper（OpenAI/whisper）
2. FunASR（modelscope/FunASR）
3. Vosk（alphacephei/vosk）

---

## 二、多维度对比表
| 对比维度 | OpenAI Whisper | FunASR | Vosk |
|---------|----------------|--------|------|
| 许可协议 | MIT（商用友好） | MIT | Apache 2.0 |
| 语言支持 | 99种语言，中文强 | 中文最优，支持方言 | 多语言，中文一般 |
| 模型体量 | base/small/medium/large | 轻量/工业级 | 超轻量 |
| 推理速度 | CPU：small模型较快 | CPU实时性好 | CPU极快 |
| 流式/实时 | 不支持原生流式 | 支持流式识别 | 支持流式 |
| 部署难度 | 极低（pip一键安装） | 中等 | 低 |
| PC实测感受 | 精度高、使用最简单 | 中文识别最强 | 最轻量、延迟最低 |

---

## 三、选型结论
**最终选择：OpenAI Whisper small 模型**
理由：
1. 部署最简单，一行命令安装
2. 中文识别精度高
3. 支持本地CPU运行，无需GPU
4. 可直接读取音频文件，完美适配任务二的克隆音频
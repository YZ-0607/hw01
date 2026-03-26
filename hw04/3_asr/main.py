import os
import numpy as np
import soundfile as sf
import whisper

# 重写音频加载函数，绕开 ffmpeg
def load_audio_without_ffmpeg(audio_path):
    # 用 soundfile 加载音频（支持 WAV/FLAC 等格式）
    data, sr = sf.read(audio_path)
    # 转成单声道
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    # 重采样到 16kHz（Whisper 要求）
    if sr != 16000:
        import librosa
        data = librosa.resample(data, orig_sr=sr, target_sr=16000)
    return data.astype(np.float32)

# 替换 whisper 的音频加载函数
whisper.audio.load_audio = load_audio_without_ffmpeg

def speech_to_text(audio_path, model_name="small"):
    model = whisper.load_model(model_name)
    print("正在识别音频，请稍候...")
    result = model.transcribe(audio_path, language="Chinese")
    return result["text"]

if __name__ == "__main__":
    AUDIO_FILE = "../2_clone_audio/clone_voice.mp3"
    if not os.path.exists(AUDIO_FILE):
        print("错误：未找到音频文件，请检查路径！")
    else:
        text = speech_to_text(AUDIO_FILE)
        print("\n===== 语音识别结果 =====")
        print(text)
        with open("asr_result.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("\n结果已保存至 asr_result.txt")
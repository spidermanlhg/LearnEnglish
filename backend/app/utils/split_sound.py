from pydub import AudioSegment
from pydub.silence import split_on_silence
import os, sys, re
import shutil
import whisper
import os
import torch
import gc
import logging
import time
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 全局变量，用于存储已加载的模型
_whisper_model = None
_whisper_model_size = None
_whisper_device = None

# 获取当前脚本的完整路径
script_path = os.path.abspath(sys.argv[0])

# 去掉脚本名称，只保留目录路径
cur_dir = os.path.dirname(script_path)



def get_whisper_model(model_size="tiny", device=None):
    """
    获取Whisper模型的单例实例
    
    参数:
        model_size: 模型大小，可选值为 "tiny", "base", "small", "medium", "large"
        device: 运行设备，可以是 "cpu", "cuda", "cuda:0" 等，如果为None则自动选择
    
    返回:
        加载好的Whisper模型实例
    """
    global _whisper_model, _whisper_model_size, _whisper_device
    
    # 自动选择设备
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 如果模型已加载且参数一致，直接返回
    if _whisper_model is not None and _whisper_model_size == model_size and _whisper_device == device:
        logger.info(f"使用已加载的Whisper模型 (大小: {model_size}, 设备: {device})")
        return _whisper_model
    
    # 如果已有模型但参数不一致，先释放资源
    if _whisper_model is not None:
        logger.info(f"释放旧模型资源 (大小: {_whisper_model_size}, 设备: {_whisper_device})")
        del _whisper_model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    # 加载新模型
    start_time = time.time()
    logger.info(f"加载Whisper模型 (大小: {model_size}, 设备: {device})")
    
    try:
        _whisper_model = whisper.load_model(model_size, device=device)
        _whisper_model_size = model_size
        _whisper_device = device
        logger.info(f"模型加载完成，耗时: {time.time() - start_time:.2f}秒")
        return _whisper_model
    except Exception as e:
        logger.error(f"加载模型失败: {e}")
        # 如果加载失败，尝试使用CPU
        if device != "cpu":
            logger.info("尝试使用CPU加载模型")
            return get_whisper_model(model_size, "cpu")
        raise

def split_sound(audiopath, audiotype, output, by_sentence=True, min_segment_length=1.0, max_segment_length=10.0, model_size="base", device=None):
    '''
    audiopath 音频文件路径
    audiotype 音频文件类型
    output 输出路径
    by_sentence 是否按句子分割，默认为True
    min_segment_length 最小分段长度（秒），默认为1.0秒
    max_segment_length 最大分段长度（秒），默认为10.0秒
    model_size Whisper模型大小，可选值为 "tiny", "base", "small", "medium", "large"，默认为"base"
    device 运行设备，可以是 "cpu", "cuda", "cuda:0" 等，如果为None则自动选择

    该函数分隔音频文件后，返回分隔后的音频文件名称。
    '''

    # 函数返回的mp3文件名称list - 初始化在try块外部
    name_list = []

    try:
        # 读入音频
        logger.info(f'读入音频: {audiopath}')
        sound = AudioSegment.from_file(file=audiopath, format=audiotype)
        
        # 创建保存目录
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output, exist_ok=True)
        
        if by_sentence:
            # 使用Whisper获取句子时间戳
            logger.info(f'使用Whisper识别句子 (模型: {model_size})')
            
            # 获取模型实例（使用单例模式）
            model = get_whisper_model(model_size, device)
            
            # 记录内存使用情况
            if torch.cuda.is_available():
                before_mem = torch.cuda.memory_allocated() / (1024 ** 3)  # GB
                logger.info(f'转录前GPU内存使用: {before_mem:.2f} GB')
            
            # 使用更高质量的转录设置
            transcribe_start = time.time()
            result = model.transcribe(
                audiopath, 
                condition_on_previous_text=False, 
                word_timestamps=True,
                verbose=False,
                fp16=(device != "cpu")  # 在GPU上使用半精度加速
            )
            
            logger.info(f'转录完成，耗时: {time.time() - transcribe_start:.2f}秒')
            
            # 记录转录后内存使用
            if torch.cuda.is_available():
                after_mem = torch.cuda.memory_allocated() / (1024 ** 3)  # GB
                logger.info(f'转录后GPU内存使用: {after_mem:.2f} GB, 增加: {after_mem - before_mem:.2f} GB')
            
            # 使用word_timestamps来更精确地识别句子边界
            print('分析语音片段和单词时间戳')
            segments = []
            
            # 定义标点符号列表，用于识别句子结束
            end_punctuations = [".", "?", "!", "。", "？", "！"]
            pause_punctuations = [",", ";", ":", "，", "；", "："]
            
            for segment in result["segments"]:
                # 如果分段时间超过最大分段长度，或者包含单词信息，尝试在自然句子边界处进一步分割
                if (segment["end"] - segment["start"] > max_segment_length and "words" in segment) or "words" in segment:
                    words = segment["words"]
                    start_idx = 0
                    last_pause_idx = 0
                    current_duration = 0
                    
                    for i, word in enumerate(words):
                        word_text = word["word"].strip()
                        current_duration = words[i]["end"] - words[start_idx]["start"]
                        
                        # 检查是否需要在当前单词处分割
                        split_here = False
                        split_reason = ""
                        
                        # 检查是否有句子结束标点
                        has_end_punct = any(word_text.endswith(p) or word_text.startswith(p) for p in end_punctuations)
                        
                        # 检查是否有暂停标点（可能是子句）
                        has_pause_punct = any(word_text.endswith(p) or word_text.startswith(p) for p in pause_punctuations)
                        
                        # 在句号、问号、感叹号等句子结束标点后分割
                        if i > 0 and has_end_punct and current_duration >= min_segment_length:
                            split_here = True
                            split_reason = "句子结束标点"
                        # 如果达到最大时长，尝试在暂停标点处分割
                        elif i > 0 and current_duration >= max_segment_length:
                            if has_pause_punct:
                                split_here = True
                                split_reason = f"达到最大时长({current_duration:.2f}秒)且有暂停标点"
                            # 如果没有找到合适的暂停标点，但已经超过最大时长很多，强制分割
                            elif current_duration >= max_segment_length * 1.5:
                                split_here = True
                                split_reason = f"超过最大时长({current_duration:.2f}秒)，强制分割"
                            # 记录最后一个暂停标点位置，以便在没有更好的分割点时使用
                            elif has_pause_punct:
                                last_pause_idx = i
                        
                        if split_here:
                            # 创建新的分段
                            new_segment = {
                                "start": words[start_idx]["start"],
                                "end": words[i]["end"],
                                "text": " ".join(w["word"] for w in words[start_idx:i+1])
                            }
                            
                            # 只有当分段长度超过最小长度时才添加
                            segment_duration = new_segment["end"] - new_segment["start"]
                            if segment_duration >= min_segment_length:
                                segments.append(new_segment)
                                print(f"分割点: {i}/{len(words)}, 原因: {split_reason}, 长度: {segment_duration:.2f}秒, 文本: {new_segment['text'][:30]}...")
                                start_idx = i + 1
                            else:
                                print(f"跳过过短分段: {segment_duration:.2f}秒 < {min_segment_length}秒, 文本: {new_segment['text']}")
                    
                    # 添加剩余的单词作为最后一个分段
                    if start_idx < len(words):
                        new_segment = {
                            "start": words[start_idx]["start"],
                            "end": words[-1]["end"],
                            "text": " ".join(w["word"] for w in words[start_idx:])
                        }
                        
                        # 检查最后一个分段的长度
                        segment_duration = new_segment["end"] - new_segment["start"]
                        if segment_duration >= min_segment_length:
                            segments.append(new_segment)
                            print(f"添加最后分段, 长度: {segment_duration:.2f}秒, 文本: {new_segment['text'][:30]}...")
                        else:
                            # 如果最后一个分段太短，尝试与前一个分段合并
                            if len(segments) > 0:
                                prev_segment = segments[-1]
                                prev_segment["end"] = new_segment["end"]
                                prev_segment["text"] += " " + new_segment["text"]
                                print(f"最后分段过短({segment_duration:.2f}秒)，已合并到前一个分段")
                            else:
                                # 如果没有前一个分段，只能保留这个短分段
                                segments.append(new_segment)
                                print(f"保留唯一的短分段: {segment_duration:.2f}秒, 文本: {new_segment['text']}")
                else:
                    # 检查分段长度是否符合要求
                    segment_duration = segment["end"] - segment["start"]
                    if segment_duration >= min_segment_length:
                        segments.append(segment)
                        print(f"保留原始分段, 长度: {segment_duration:.2f}秒")
            
            # 根据时间戳分割音频
            print('开始按句子分割')
            for i, segment in enumerate(segments):
                # 获取句子的起止时间（秒），添加缓冲时间确保句子完整播放
                # 起始时间提前50毫秒（如果可能），结束时间延后300毫秒，确保句子不会被截断
                start_time = max(0, int((segment['start'] - 0.05) * 1000))  # 转换为毫秒，并确保不小于0
                end_time = min(len(sound), int((segment['end'] + 0.3) * 1000))  # 转换为毫秒，并确保不超过音频长度
                
                # 提取句子音频
                sentence_audio = sound[start_time:end_time]
                
                # 生成文件名，格式化数字以保证文件名排序正确
                save_name = os.path.join(output, f"{i+1:03d}.{audiotype}")
                sentence_audio.export(save_name, format=audiotype)
                name_list.append({"sn":i+1, "name":f"{i+1:03d}.{audiotype}", "text":segment['text']})
                print(f'{i+1:03d}', len(sentence_audio), f"文本: {segment['text']}")
        else:
            # 使用原来的静默检测方法分割
            print('开始按静默分割')
            chunks = split_on_silence(sound, min_silence_len=200, silence_thresh=-50, keep_silence=200)
            
            # 保存所有分段
            print('开始保存')
            for i, chunk in enumerate(chunks):
                # 生成文件名，格式化数字以保证文件名排序正确
                save_name = os.path.join(output, f"{i+1:03d}.{audiotype}")
                chunk.export(save_name, format=audiotype)
                name_list.append({"sn":i+1, "name":f"{i+1:03d}.{audiotype}"})
                print(f'{i+1:03d}', len(chunk))

        print('保存完毕')

    except Exception as e:
        logger.error(f"处理音频时出错: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # 清理内存
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info(f'内存清理完成，当前GPU内存使用: {torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB')

    return name_list



# 修改示例用法
if __name__ == "__main__":
    audiopath = r"D:\英语 English\麦麦 discovery 2\discover 2级CD MP3版\MP3 units 8-13\41 曲目 41.mp3" # 输入音频文件路径
    audiotype = "mp3"  # 输入音频文件类型
    output = r"C:\Users\kidsland\Desktop\english\jiemi_split" # 输出目录路径
    
    # 按句子分割音频，可以自定义最小和最大分段长度
    split_sound(
        audiopath, 
        audiotype, 
        output, 
        by_sentence=True,
        min_segment_length=1.5,  # 最小分段长度（秒）
        max_segment_length=8.0,  # 最大分段长度（秒）
        model_size="tiny",       # 使用更小的模型以节省资源
        device=None              # 自动选择设备
    )
    
    # 如果需要使用原来的静默检测方法分割
    # split_sound(audiopath, audiotype, output, by_sentence=False)


# spleeter 用法介绍
# 去除声音中的音乐，只留下人的声音。
# spleeter separate -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3 C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3

#分隔
# spleeter separate -i C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3 -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3
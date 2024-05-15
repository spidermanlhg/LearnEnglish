from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import shutil


def split_sound(audiopath, audiotype):
    '''
    audiopath 音频文件路径
    audiotype 音频文件类型

    '''

    # 读入音频
    print('读入音频')
    sound = AudioSegment.from_file(file=audiopath, format=audiotype)

    # 分割
    print('开始分割')
    # min_silence_len: 拆分语句时，静默满0.3秒则拆分。silence_thresh：小于-70dBFS以下的为静默。
    chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-70, keep_silence=600)

    len(chunks)

    # 创建保存目录
    filepath = os.path.split(audiopath)[0]
    chunks_path = filepath+'/chunks/'

    if os.path.exists(chunks_path):
        shutil.rmtree(chunks_path)

    os.mkdir(chunks_path)

    # 保存所有分段
    print('开始保存')
    result = []
    for i in range(len(chunks)):
        new = chunks[i]
        if len(new) > 1000:
            result.append(new)

    for i in range(len(result)):
        new = result[i]
        j = i+1
        save_name = chunks_path+'%03d.%s' % (j, audiotype)
        new.export(      save_name, format=audiotype )
        print('%03d' % j, len(new))

    print('保存完毕')


# spleeter 用法介绍
# spleeter separate -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3 C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3


# spleeter separate -i C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3 -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3

from pydub import AudioSegment
from pydub.silence import split_on_silence
import os, sys
import shutil

# 获取当前脚本的完整路径
script_path = os.path.abspath(sys.argv[0])

# 去掉脚本名称，只保留目录路径
cur_dir = os.path.dirname(script_path)


def split_sound(audiopath, audiotype, output):
    '''
    audiopath 音频文件路径
    audiotype 音频文件类型
    output 输出路径

    该函数分隔音频文件后，返回分隔后的音频文件名称。
    '''

    try:
        # 读入音频
        print('读入音频')
        sound = AudioSegment.from_file(file=audiopath, format=audiotype)

        # 分割
        print('开始分割')
        chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-70, keep_silence=600)

        # 创建保存目录
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs( output, exist_ok=True)

        # 函数返回的mp3文件名称list
        name_list =[]

        # 保存所有分段
        print('开始保存')
        for i, chunk in enumerate(chunks):
            if len(chunk) > 1000:  # 只保存大于1000毫秒的片段
                # 生成文件名，格式化数字以保证文件名排序正确
                save_name = os.path.join(output, f"{i+1:03d}.{audiotype}")
                chunk.export(save_name, format=audiotype)
                name_list.append(  { "sn":i+1 ,  "name":f"{i+1:03d}.{audiotype}" }  )  #把分隔后的mp3文件名放入一个list中，用于函数返回值
                print(f'{i+1:03d}', len(chunk))

        print('保存完毕')

    except Exception as e:
        print(f"Error occurred: {e}")


    return name_list


# 示例用法
if __name__ == "__main__":

    audiopath = r"D:\workspace\LearnEnglish\backend\uploads\1\04 曲目 4.mp3"  # 输入音频文件路径
    audiotype = "mp3"  # 输入音频文件类型
    output = r"D:\workspace\LearnEnglish\backend\data\1\4\\"  # 输出目录路径

    split_sound(audiopath, audiotype, output)



# spleeter 用法介绍
# 去除声音中的音乐，只留下人的声音。
# spleeter separate -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3 C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3

#分隔
# spleeter separate -i C:\Users\kidsland\Desktop\LearnEnglish\public\uploads\3\000.mp3 -p spleeter:2stems -o C:\Users\kidsland\Desktop\LearnEnglish\other\3
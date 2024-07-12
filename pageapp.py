import streamlit as st
import edge_tts
import os
import base64
import json
CONFIG_FILE = 'config.json'

def get_audio_base64(audio_file):
    with open(audio_file, 'rb') as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64
def save_tts(text, rate, volume, pitch):
    rate = f'+{rate}' if rate >= 0 else rate
    volume = f'+{volume}' if volume >= 0 else volume
    pitch = f'+{pitch}' if pitch >= 0 else pitch
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AnaNeural",
        rate=f'{rate}%',
        volume=f'{volume}%',
        pitch=f'{pitch}Hz'
    )

    file_name = ''.join([x for x in text if x.isalnum() or x.isspace()]) + ".mp3"
    communicate.save_sync(file_name)

    return file_name
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {'rate': 0, 'volume': 0, 'pitch': 0, 'save_to_local': False}


# Define the Streamlit app
def app():
    # 加载配置
    config = load_config()
    # 左侧边栏
    st.sidebar.header('控制面板')

    # 三个滑块
    slider1 = st.sidebar.slider('速度', -100, 100, 0)
    slider2 = st.sidebar.slider('音量', -100, 100, 0)
    slider3 = st.sidebar.slider('赫兹', -100, 100, 0)
    # 增加一个勾选框
    save_to_local = st.sidebar.checkbox('直接保存到本地', config['save_to_local'])

    # 保存当前配置
    config = {'rate': slider1, 'volume': slider2, 'pitch': slider3, 'save_to_local': save_to_local}
    save_config(config)
    st.subheader("我是一个语音合成助手，请把要合成的语音发给我")
    user_input = st.text_area('输入你的问题:', height=5)

    # Display the text when the user submits the form
    if st.button('提交'):
        audio_file = save_tts(user_input, slider1, slider2, slider3)
        # 自动播放音频
        audio_base64 = get_audio_base64(audio_file)
        audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    您的浏览器不支持音频播放。
                </audio>
                """
        st.components.v1.html(audio_html)
        # 提供下载链接
        with open(audio_file, 'rb') as f:
            st.download_button(
                label="下载音频",
                data=f,
                file_name=os.path.basename(audio_file),
                mime="audio/mpeg"
            )


# Run the app
if __name__ == "__main__":
    app()

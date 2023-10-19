import streamlit as st
from PIL import Image
from yolov5 import detect
from streamlit_option_menu import option_menu
import os
import tempfile
import shutil
from ffmpy import FFmpeg

weight_path = ".\\weights\\nhanDangTraiCay_model3.pt"
result_path = ".\\yolov5\\runs\\detect\\result\\"

st.set_page_config(
    page_title="Do Minh Trong 21133111 App",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

#lấy đường dẫn
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(suffix="." + uploaded_file.type.rsplit("/", 1)[-1], delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name
def get_absolute_path(file_name):
    return os.path.abspath(file_name)
#convert video
def convert_video(input_path, output_path):
    ff = FFmpeg(executable='C:\\ffmpeg\\bin\\ffmpeg.exe',
                inputs={input_path: None},
                outputs={output_path: '-c:a ac3 -c:v h264'})
    ff.cmd
    ff.run()


s = st.session_state
if not s:
        s.pressed_first_button = False


with st.sidebar:
    selected = option_menu("Main Menu", ["Nhận Dạng Trái Cây", 'Nhận diện khuôn mặt'],
                               icons=['image', 'robot'], menu_icon="cast", default_index=0)


if selected == 'Nhận Dạng Trái Cây':
    if os.path.exists(result_path):
        shutil.rmtree(result_path)

    uploaded_file = st.file_uploader(
        "Upload a JPG, JPEG, PNG, MP4 file",
        type=["jpg", "jpeg", "png", "mp4"],
        help="Scanned file are not supported yet!",
    )
    if not uploaded_file:
        st.stop()
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        absolute_path = get_absolute_path(file_path)
        if "image" in uploaded_file.type:
            image = Image.open(uploaded_file)
            st.image(image, caption='Image you uploaded')

            nhandang = st.button("Nhận dạng", type="primary")
            if nhandang:
                detect.run(weights=weight_path, source=absolute_path, name="result", conf_thres=0.6)
                image = Image.open(result_path + os.path.basename(absolute_path))
                st.image(image)
                shutil.rmtree(result_path)

        if "video" in uploaded_file.type:
            st.video(uploaded_file)
            nhandang = st.button("Nhận dạng", type="primary")
            if nhandang:
                detect.run(weights=weight_path, source=absolute_path, name="result", conf_thres=0.6)
                convert_video(input_path=result_path + os.path.basename(absolute_path),
                              output_path=result_path + 'output.mp4')
                st.video(result_path + 'output.mp4')
                shutil.rmtree(result_path)



if selected == 'Nhận diện khuôn mặt':
        st.text("Nhận diện khuôn mặt")





import tkinter as tk
from tkinter import filedialog
import shutil
import os

def attach_file():
    # 파일 선택 다이얼로그를 열고, 사용자가 선택한 파일의 경로를 얻습니다.
    file_path = filedialog.askopenfilename()
    if not file_path:
        # 사용자가 취소 버튼을 누른 경우
        return

    # 파일을 pre_report 폴더에 복사합니다. 폴더가 없는 경우 생성합니다.
    destination_folder = "pre_report"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, os.path.basename(file_path))
    shutil.copy(file_path, destination_path)
    print(f"File {os.path.basename(file_path)} has been copied to {destination_folder}")

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("File Attachment Example")

# 첨부 버튼 생성 및 배치
attach_button = tk.Button(root, text="Attach File", command=attach_file)
attach_button.pack(pady=20)

# 이벤트 루프 시작
root.mainloop()

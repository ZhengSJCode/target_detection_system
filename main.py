from tkinter import *
import video_class
import Keyboard_class
from tkinter import filedialog

import 虚拟计算器
import 虚拟键盘


class Application(Frame):
    # 视频大小全局设置
    Video_Size = (1024, 768)

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.place(relwidth=1.0, relheight=1.0)
        self.create_Widget()

    def create_Widget(self):
        #
        self.video_Label = Label(self,  text='软工大数据2001班\n\n20102130137\n\n郑帅杰毕业设计',font=(100))
        self.video_Label.place(relx=0, rely=0, relwidth=0.8, relheight=0.9)
        # 右侧选项框架
        Option_Frame = Frame(self, bg='blue')
        Option_Frame.place(relx=0.8, rely=0.05, relwidth=1 - 0.82, relheight=0.9)
        self.create_OptionMenu(Option_Frame)

    def create_OptionMenu(self, master=OptionMenu):
        # Video_Size = (800, 600)
        btn01 = Button(master, text='播放视频', command=self.btn01_play_video)
        btn01.pack(fill="both", expand=True)

        Button(master, text='手势识别', command=self.btn02_figure_camera).pack(fill="both", expand=True)
        Button(master, text='虚拟键盘', command=self.btn03_virtual_keyboard).pack(fill="both", expand=True)
        Button(master, text='虚拟计算器', command=self.test).pack(fill="both", expand=True)
        # Button(master, text='test_btn03', command=self.test).pack(fill="both", expand=True)
        # Button(master, text='test_btn03', command=self.test).pack(fill="both", expand=True)
        Button(master, text='退出', command=self.close_window).pack(fill="both", expand=True)

    def btn01_play_video(self):
        path = filedialog.askopenfilename()
        s = video_class.video(master=self.video_Label, video_Path=path, Video_Size=self.Video_Size)
        s.open()

    def btn02_figure_camera(self):
        s = video_class.Mp_figure(master=self.video_Label, Video_Size=self.Video_Size)
        s.open()

    def btn03_virtual_keyboard(self):
        虚拟键盘.main(master=self.video_Label, Video_Size=self.Video_Size)

    def test(self):
        s=虚拟计算器.Calculator()
        s.open(master=self.video_Label, Video_Size=self.Video_Size)

    def close_window(self):
        self.video_Label.destroy()
        self.master.quit()

    # def test(self):
    #     pass


if __name__ == '__main__':
    root = Tk()
    root.geometry("1920x1680")
    root.minsize(800, 600)
    app = Application(master=root)
    root.mainloop()


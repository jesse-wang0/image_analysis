import tkinter as tk

class Page1(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        self.vid_manager = vid_manager
        self.help_msg = tk.Label(self, text="""Welcome to my Tool. 
                                    \n Please select a video to analyse.""")
        self.help_msg.pack()
        self.content_container = tk.Frame(self, highlightbackground="black", 
                                            highlightthickness=1)

    def get_skip(self):
        return self.spinbox_skip.get()

    def get_input_path(self):
        return self.vid_manager.get_path()
    
    def setup_page(self, path):
        self.vid_manager.set_video(path)
        self.setup_video_preview()
        self.setup_spinbox()
        self.setup_skip_buttons()
        self.help_msg.config(text="Stage 1: Setup")
        self.setup_roi()
        self.setup_scale()
        self.content_container.pack(fill=tk.BOTH)

    def setup_video_preview(self):
        self.image_container = tk.Frame(self.content_container, 
                                        highlightbackground="black", 
                                        highlightthickness=1)
        self.image_label = tk.Label(self.image_container)
        self.image_label.config(image=self.vid_manager.get_next_frame(0))
        self.image_label.pack()
        self.frame_count_label = tk.Label(self.image_container, text=f"Selected frame: {self.vid_manager.get_current_frame_count()} / {self.vid_manager.get_total_frame_count()}")
        self.frame_count_label.pack(side=tk.TOP)
        self.image_container.pack(anchor="nw", side=tk.LEFT)

    def setup_spinbox(self):
        self.spinbox_container = tk.Frame(self.content_container, 
                                        highlightbackground="black", 
                                        highlightthickness=1)
        self.spinbox_text = tk.Label(self.spinbox_container)
        self.spinbox_text.config(text="1. Choose frequency of frames to skip: ")
        self.spinbox_text.pack()
        self.spinbox_skip = tk.Spinbox(self.spinbox_container, from_= 1, 
                                        to = 10, width=10)
        self.spinbox_skip.pack(pady=10)
        self.spinbox_container.pack(fill=tk.BOTH, side=tk.TOP,
                                    anchor="n")

    def setup_skip_buttons(self):
        skip_frames_frame = tk.Frame(self.image_container)
        skip_frames_frame.pack(before=self.frame_count_label, fill=tk.X)
        self.back5_button = tk.Button(skip_frames_frame, text='<<<<<', 
                                command=lambda: self.skip_frame(-5))
        self.back5_button.pack(side=tk.LEFT, anchor="w")
        self.back3_button = tk.Button(skip_frames_frame, text='<<<', 
                                command=lambda: self.skip_frame(-3))
        self.back3_button.pack(side=tk.LEFT, anchor="w")
        self.back1_button = tk.Button(skip_frames_frame, text='<', 
                                command=lambda: self.skip_frame(-1))
        self.back1_button.pack(side=tk.LEFT, anchor="w")

        self.skip5_button = tk.Button(skip_frames_frame, text='>>>>>', 
                                command=lambda: self.skip_frame(5))
        self.skip5_button.pack(side=tk.RIGHT, anchor="e")
        self.skip3_button = tk.Button(skip_frames_frame, text='>>>', 
                                command=lambda: self.skip_frame(3))
        self.skip3_button.pack(side=tk.RIGHT, anchor="e")
        self.skip1_button = tk.Button(skip_frames_frame, text='>', 
                                command=lambda: self.skip_frame(1))
        self.skip1_button.pack(side=tk.RIGHT, anchor="e")
    
    def setup_roi(self):
        self.roi_frame = tk.Frame(self.content_container, 
                                  highlightbackground="black", 
                                  highlightthickness=1)
        title_label = tk.Label(self.roi_frame, text=("2. Select regions containing the object"
                                                     "\n Choose two clear frames to select the object of interest.")
                               )
        title_label.pack(side=tk.TOP)

        self.roi_label_1 = tk.Label(self.roi_frame, text="Region: ( , , , )")
        self.roi_label_1.pack(side=tk.TOP)
        self.roi_button_1 = tk.Button(self.roi_frame, text="Select 1st ROI", 
                                    command=lambda: self.get_roi(1))
        self.roi_button_1.pack(side=tk.TOP, anchor="n", pady=10)
        self.roi_label_2 = tk.Label(self.roi_frame, text="Region: ( , , , )")
        self.roi_label_2.pack(side=tk.TOP)
        self.roi_button_2 = tk.Button(self.roi_frame, text="Select 2nd ROI", 
                                    command=lambda: self.get_roi(2))
        self.roi_button_2.pack(side=tk.TOP, anchor="n", pady=10)
        self.roi_frame.pack(side=tk.TOP, fill=tk.BOTH)


    def setup_scale(self):
        self.scale_frame = tk.Frame(self.content_container, 
                                  highlightbackground="black", 
                                  highlightthickness=1)
        title_label = tk.Label(self.scale_frame, text="3. Select the scale. \n Click the start and end of something of known length.")
        title_label.pack(side=tk.TOP)
        self.scale_button = tk.Button(self.scale_frame, text="Start drawing scale line", 
                                    command=self.draw_scale)
        self.scale_button.pack(side=tk.TOP)
        self.scale_label = tk.Label(self.scale_frame, text="Scale:")
        self.scale_label.pack(side=tk.TOP)
        self.scale_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    
    def skip_frame(self, num):
        self.image_label.config(image=self.vid_manager.get_next_frame(num))
        self.frame_count_label.config(text=f"Selected frame: {self.vid_manager.get_current_frame_count()} / {self.vid_manager.get_total_frame_count()}")

    def get_roi(self, roi_num):
        rect = self.vid_manager.select_roi(roi_num)
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        top_left=(x,y)
        top_right = (x + w, y)
        bottom_left = (x, y + h)
        bottom_right = (x + w, y + h)
        if roi_num == 1:
            self.roi_label_1.config(text=f"Region: ({top_left}, {top_right}, {bottom_left}, {bottom_right})")
        elif roi_num == 2:
            self.roi_label_2.config(text=f"Region: ({bottom_left}, {bottom_right}, {top_left}, {top_right})")

        if self.vid_manager.check_roi_exists() and self.vid_manager.check_scale_exists():
            self.control_btns.on_next()

    def draw_scale(self):
        self.vid_manager.setup_draw()
        scale = self.vid_manager.get_scale()
        if scale is not None:
            self.scale_label.config(text=f"Scale: {scale}")
            if self.vid_manager.check_roi_exists() and self.vid_manager.check_scale_exists():
                self.control_btns.on_next()
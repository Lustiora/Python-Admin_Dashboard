import tkinter
import customtkinter
import sys


# # ==============================================================================
# # [모듈 1] 슬라이더 스크롤 지원 클래스 (ScrollableSliderMixin)
# # 기능: CTkSlider 위젯에 마우스 휠 스크롤 기능을 추가하여 값을 조절할 수 있게 합니다.
# # 사용법:
# #   1. 이 클래스를 메인 앱 클래스에 상속받으세요. (class App(..., ScrollableSliderMixin))
# #   2. 슬라이더 생성 후 self.setup_slider_scroll(슬라이더_변수)를 호출하세요.
# # ==============================================================================
# class ScrollableSliderMixin:
#     def setup_slider_scroll(self, slider, step=0.05):
#         """
#         [설정 함수] 슬라이더에 마우스 진입/이탈 이벤트를 연결합니다.
#         마우스가 슬라이더 위에 있을 때만 휠 기능을 활성화하여, 전체 스크롤과 충돌을 방지합니다.
#         :param slider: 기능을 적용할 CTkSlider 객체
#         :param step: 휠 1칸당 움직일 값 (기본값 0.05, number_of_steps가 있으면 자동 보정됨)
#         """
#         # 마우스가 슬라이더 위에 올라갔을 때(<Enter>) -> 스크롤 제어 함수 연결
#         slider.bind("<Enter>", lambda e: self._bind_scroll(slider, step))
#         # 마우스가 슬라이더 밖으로 나갔을 때(<Leave>) -> 스크롤 제어 해제 (전체 화면 스크롤 복구)
#         slider.bind("<Leave>", lambda e: self._unbind_scroll(slider))
#
#     def _bind_scroll(self, slider, step):
#         """ [내부 함수] 운영체제별 마우스 휠 이벤트를 슬라이더 조작 함수에 연결(Bind)합니다. """
#         # Windows/MacOS 용 휠 이벤트
#         slider.bind("<MouseWheel>", lambda e: self._on_scroll(e, slider, step))
#         # Linux 용 휠 이벤트 (Button-4: 위로, Button-5: 아래로)
#         slider.bind("<Button-4>", lambda e: self._on_scroll(e, slider, step))
#         slider.bind("<Button-5>", lambda e: self._on_scroll(e, slider, step))
#
#     def _unbind_scroll(self, slider):
#         """ [내부 함수] 연결된 마우스 휠 이벤트를 해제(Unbind)합니다. """
#         slider.unbind("<MouseWheel>")
#         slider.unbind("<Button-4>")
#         slider.unbind("<Button-5>")
#
#     def _on_scroll(self, event, slider, step):
#         """ [작동 원리] 휠 이벤트 발생 시, 실제 값을 계산하고 슬라이더에 적용합니다. """
#         current_val = slider.get()
#
#         # 슬라이더의 설정값(최소, 최대, 단계 수)을 안전하게 가져옵니다. (버전 호환성 확보)
#         # getattr를 사용하여 '_from_' 속성이 없으면 '_from'을 찾는 식입니다.
#         min_val = getattr(slider, '_from', getattr(slider, '_from_', 0))
#         max_val = getattr(slider, '_to', getattr(slider, '_to', 1))
#         steps = getattr(slider, '_number_of_steps', None)
#
#         # '단계(Steps)'가 설정된 슬라이더인 경우, 휠 1칸당 이동량을 단계 크기에 맞춥니다.
#         # 예: 0~1 사이 4단계라면 한 칸에 0.25씩 움직여야 자연스럽습니다.
#         if steps is not None and steps > 0:
#             step_size = (max_val - min_val) / steps
#             # 기본 설정된 step(0.05)보다 계산된 step_size가 크면 교체합니다.
#             if step_size > step:
#                 step = step_size
#
#         new_val = current_val
#
#         # 휠 방향 감지 및 값 계산
#         # Windows/Mac: event.delta (양수=위/증가, 음수=아래/감소)
#         # Linux: event.num (4=위, 5=아래)
#         if event.num == 4 or event.delta > 0:
#             new_val = current_val + step
#         elif event.num == 5 or event.delta < 0:
#             new_val = current_val - step
#
#         # 계산된 값이 최소/최대 범위를 벗어나지 않도록 보정(Clamping)
#         new_val = max(min_val, min(max_val, new_val))
#
#         # 값 적용
#         slider.set(new_val)
#
#         # 슬라이더에 연결된 command 함수가 있다면 실행 (예: 프로그레스바 연동 등)
#         if slider._command:
#             slider._command(new_val)
#

# ==============================================================================
# [모듈 2] 메인 어플리케이션 클래스 (App)
# 기능: 전체 UI 레이아웃을 구성하고 각 위젯을 배치합니다.
# 구조: 사이드바(좌측), 메인 콘텐츠(중앙/우측)로 나뉜 그리드 레이아웃을 사용합니다.
# ==============================================================================
# class App(customtkinter.CTk, ScrollableSliderMixin):
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # -- 기본 윈도우 설정 --
        self.title("CustomTkinter complex_example.py")
        self.geometry("1100x580")

        # -- 그리드 레이아웃 설정 (1x4 구조) --
        # column 0: 사이드바 (고정 크기)
        # column 1: 메인 입력/슬라이더 영역 (공간을 차지하며 늘어남 - weight=1)
        # column 2: 탭뷰/스크롤 프레임 영역 (고정)
        # column 3: 라디오버튼/체크박스 영역 (고정)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # ===================================================
        # [구역 1] 사이드바 (Sidebar) - 왼쪽 설정 패널
        # ===================================================
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  # 아래쪽 여백 확보

        # 로고 및 타이틀
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 사이드바 메뉴 버튼들
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # 테마 변경 (Light/Dark/System)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # UI 배율 조절 (Scaling)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # ===================================================
        # [구역 2] 메인 콘텐츠 영역 (Main Area)
        # ===================================================

        # [A] 하단 입력창 (Entry) & 메인 버튼
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # [B] 멀티라인 텍스트 박스 (Textbox) - 상단 중앙
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # [C] 탭 뷰 (Tabview) - 상단 우측
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        # 탭 내부 위젯들 (옵션 메뉴, 콤보박스, 다이얼로그 버튼)
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # [D] 라디오 버튼 그룹 (Radio Button Frame) - 우측 상단
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.radio_var = tkinter.IntVar(value=0)  # 라디오 버튼 그룹 변수
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
                                                           value=2)
        self.radio_button_3.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        # [E] 슬라이더 및 진행바 패널 (Slider & Progressbar) - 중앙
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # 가로 슬라이더 (4단계 스냅)
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # 세로 슬라이더 및 세로 진행바
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")

        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # ===================================================
        # [구역 3] 스크롤 가능한 프레임 (Scrollable Frame)
        # 특징: 스크롤바 영역뿐만 아니라 빈 공간에서도 휠 스크롤이 작동하도록 설정합니다.
        # ===================================================
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.scrollable_frame_switches = []
        for i in range(100):  # 스위치 100개 생성
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

            # [중요] 스위치 위에서도 휠 스크롤이 작동하도록 이벤트 연결(Bind)
            # 기본적으로는 위젯 위에 마우스가 있으면 프레임 스크롤이 멈추는데, 이를 해결합니다.
            switch.bind("<MouseWheel>", self._scroll_frame_event)  # Windows/Mac
            switch.bind("<Button-4>", self._scroll_frame_event)  # Linux Up
            switch.bind("<Button-5>", self._scroll_frame_event)  # Linux Down

        # ------------------------------------------------------------------
        # [핵심 기능] 빈 공간(배경) 및 스크롤바 위에서도 스크롤 가능하게 설정 (분리 적용)
        # CTkScrollableFrame 내부 구조에 직접 이벤트를 연결합니다.
        # try-except를 분리하여 하나의 요소에서 에러가 나도 나머지는 작동하도록 안전장치를 둡니다.
        # ------------------------------------------------------------------

        # 1. 스크롤바(Scrollbar) 자체 바인딩
        try:
            self.scrollable_frame._scrollbar.bind("<MouseWheel>", self._scroll_frame_event)
            self.scrollable_frame._scrollbar.bind("<Button-4>", self._scroll_frame_event)
            self.scrollable_frame._scrollbar.bind("<Button-5>", self._scroll_frame_event)
        except Exception:
            pass

        # 2. 내부 캔버스(배경, Canvas) 바인딩 - 빈 공간 스크롤의 핵심
        try:
            self.scrollable_frame._parent_canvas.bind("<MouseWheel>", self._scroll_frame_event)
            self.scrollable_frame._parent_canvas.bind("<Button-4>", self._scroll_frame_event)
            self.scrollable_frame._parent_canvas.bind("<Button-5>", self._scroll_frame_event)
        except Exception:
            pass

        # 3. 내부 프레임(위젯이 놓이는 공간, Frame) 바인딩
        try:
            self.scrollable_frame._parent_frame.bind("<MouseWheel>", self._scroll_frame_event)
            self.scrollable_frame._parent_frame.bind("<Button-4>", self._scroll_frame_event)
            self.scrollable_frame._parent_frame.bind("<Button-5>", self._scroll_frame_event)
        except Exception:
            pass

        # 4. 메인 프레임 자체 바인딩 (테두리 등)
        try:
            self.scrollable_frame.bind("<MouseWheel>", self._scroll_frame_event)
            self.scrollable_frame.bind("<Button-4>", self._scroll_frame_event)
            self.scrollable_frame.bind("<Button-5>", self._scroll_frame_event)
        except Exception:
            pass
        # ------------------------------------------------------------------

        # [F] 체크박스 프레임 (Checkbox Frame) - 우측 중간
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # # [설정 적용] 슬라이더에 마우스 휠 스크롤 기능 연결
        # # ScrollableSliderMixin의 메서드 호출
        # self.setup_slider_scroll(self.slider_1, step=0.05)
        # self.setup_slider_scroll(self.slider_2, step=0.05)

        # [초기값 설정] 각 위젯의 기본값 및 상태 설정
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")

        # 슬라이더 값 변경 시 프로그레스바도 같이 움직이도록 연결
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)

        self.progressbar_1.configure(mode="indeterming")
        self.progressbar_1.start()

        # 텍스트 박스에 초기 텍스트 삽입
        self.textbox.insert("0.0",
                            "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    # ===================================================
    # [이벤트 핸들러] 각종 버튼 및 입력 이벤트 처리 함수들
    # ===================================================

    def _scroll_frame_event(self, event):
        """
        [스크롤 처리 함수] 스위치나 빈 공간에서 휠을 굴렸을 때 호출됩니다.
        CTkScrollableFrame의 내부 캔버스(_parent_canvas)를 찾아 강제로 스크롤시킵니다.
        """
        try:
            canvas = self.scrollable_frame._parent_canvas

            if sys.platform.startswith("win"):
                # Windows: delta 값에 따라 스크롤 (120 단위)
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif sys.platform == "darwin":
                # MacOS: delta 값 그대로 사용
                canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                # Linux: Button-4(위로), Button-5(아래로)
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        except Exception:
            pass

    def open_input_dialog_event(self):
        """ 다이얼로그(입력창) 열기 """
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """ 테마 변경 (Light / Dark) """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """ UI 크기 배율 변경 """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


# ===================================================
# [메인 실행] 프로그램 시작점
# ===================================================
if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")  # 기본 테마 설정
    customtkinter.set_default_color_theme("blue")  # 기본 색상 테마 설정

    app = App()
    app.mainloop()
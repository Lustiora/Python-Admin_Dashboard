import flet as ft


# ==============================================================================
# [메인 함수] 앱의 UI와 로직이 시작되는 진입점입니다.
# page: 앱의 전체 화면(Canvas)을 담당하는 객체입니다.
# ==============================================================================
def main(page: ft.Page):
    # 1. 페이지 기본 설정
    page.title = "Flet Counter Example"  # 윈도우 타이틀바 제목 설정
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 페이지 내부 내용물을 수직(세로) 중앙 정렬

    # 2. 데이터를 표시할 위젯(Control) 생성
    # TextField: 텍스트를 입력받거나 보여주는 위젯
    # value="0": 초기값 설정
    # text_align=RIGHT: 숫자가 오른쪽 정렬되도록 설정
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # 3. 이벤트 핸들러 함수 정의 (버튼 클릭 시 실행될 로직)

    def minus_click(e):
        """ [-] 버튼 클릭 시 실행 """
        # 현재 입력된 값(문자열)을 정수(int)로 변환해 1 뺌
        txt_number.value = str(int(txt_number.value) - 1)
        # [중요] 데이터가 변경되었음을 페이지에 알리고 화면을 다시 그림 (새로고침)
        page.update()

    def plus_click(e):
        """ [+] 버튼 클릭 시 실행 """
        # 현재 입력된 값(문자열)을 정수(int)로 변환해 1 더함
        txt_number.value = str(int(txt_number.value) + 1)
        # [중요] 변경된 값을 화면에 반영하기 위해 update() 호출 필수
        page.update()

    # 4. 화면에 위젯 배치 (Layout)
    # page.add(): 페이지에 위젯을 추가하는 함수
    page.add(
        # ft.Row: 위젯들을 가로(수평)로 나열하는 컨테이너 (HBox와 유사)
        ft.Row(
            [
                # "remove": 마이너스(-) 모양의 머티리얼 아이콘 이름
                ft.IconButton("remove", on_click=minus_click),

                # 위에서 만든 숫자 표시용 텍스트 필드
                txt_number,

                # "add": 플러스(+) 모양의 머티리얼 아이콘 이름
                ft.IconButton("add", on_click=plus_click),
            ],
            # Row 내부의 위젯들을 가로 중앙에 정렬
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


# ==============================================================================
# [앱 실행]
# target=main: 앱이 시작될 때 실행할 메인 함수를 지정합니다.
# ==============================================================================
ft.app(target=main)
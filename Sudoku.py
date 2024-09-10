import tkinter as tk
import random

# Sudoku 보드의 초기 상태를 저장할 배열
origin_board = [[0 for j in range(9)] for i in range(9)]
# 최종 퍼즐을 저장할 배열
board = [[0 for j in range(9)] for i in range(9)]
# 원래 비어있던 셀의 상태를 저장할 배열
Missing_board = [[0 for j in range(9)] for i in range(9)]
# 각 행, 열, 대각선에서 사용된 숫자를 추적하는 배열
row = [[0 for j in range(10)] for i in range(10)]  # 가로축
col = [[0 for j in range(10)] for i in range(10)]  # 세로축
diag = [[0 for j in range(10)] for i in range(10)]  # 대각선

terminate_flag = False

def board_init():
    """
    초기 Sudoku 보드를 설정합니다.
    각 3x3 서브 그리드에 대해 무작위로 숫자를 배치합니다.
    """
    seq_diag = [0, 4, 8]  # 각 서브 그리드의 대각선 인덱스
    for offset in range(0, 9, 3):  # 3x3 서브 그리드를 순회합니다
        seq = [i for i in range(1, 10)]  # 1부터 9까지의 숫자 리스트
        random.shuffle(seq)  # 숫자를 무작위로 섞습니다
        for idx in range(0, 9):  # 현재 서브 그리드의 9개의 셀을 순회합니다
            i, j = idx // 3, idx % 3  # 셀의 행과 열을 계산합니다
            row[offset + i][seq[idx]] = 1  # 행 배열 업데이트
            col[offset + j][seq[idx]] = 1  # 열 배열 업데이트
            k = seq_diag[offset // 3]  # 현재 서브 그리드의 대각선 인덱스
            diag[k][seq[idx]] = 1  # 대각선 배열 업데이트
            origin_board[offset + i][offset + j] = seq[idx]  # 보드에 숫자를 배치합니다

def make_sudoku(k):
    """
    Sudoku 퍼즐을 생성합니다. 재귀적으로 호출되어 퍼즐을 완성합니다.
    """
    global terminate_flag
    global board

    if terminate_flag:
        return True

    if k > 80:  # 모든 셀을 채운 경우
        for i in range(9):
            for j in range(9):
                board[i][j] = origin_board[i][j]  # 최종 보드를 origin_board로 설정합니다
        terminate_flag = True
        return True

    i, j = k // 9, k % 9  # 현재 위치의 행과 열을 계산합니다
    start_num = random.randint(1, 9)  # 현재 셀에 넣을 숫자를 랜덤으로 선택합니다

    if origin_board[i][j] != 0:  # 현재 셀이 이미 채워져 있는 경우
        return make_sudoku(k + 1)

    for m in range(1, 10):  # 1부터 9까지의 숫자를 시도합니다
        m = 1 + (m + start_num) % 9  # 숫자를 순환하여 시도합니다
        d = (i // 3) * 3 + (j // 3)  # 현재 셀이 위치한 3x3 서브 그리드의 대각선 인덱스 계산
        if row[i][m] == 0 and col[j][m] == 0 and diag[d][m] == 0:  # 숫자가 유효한지 확인합니다
            row[i][m], col[j][m], diag[d][m] = 1, 1, 1  # 사용된 숫자로 표시합니다
            origin_board[i][j] = m  # 보드에 숫자를 배치합니다
            if make_sudoku(k + 1):  # 다음 셀을 채우기 위해 재귀 호출합니다
                return True
            row[i][m], col[j][m], diag[d][m] = 0, 0, 0  # 백트래킹: 숫자를 지우고 다시 시도합니다
            origin_board[i][j] = 0

def Cutnum():
    """
    퍼즐에서 숫자를 제거하여 최소 30개의 숫자를 남깁니다.
    """
    filled_cells = 81
    while filled_cells > 30:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if board[i][j] != " ":
            board[i][j] = " "
            Missing_board[i][j] = board[i][j]  # 원래 보드의 비어있던 상태를 저장
            filled_cells -= 1

board_init()  # 보드 초기화
make_sudoku(0)  # 퍼즐 생성
Cutnum()  # 일부 숫자를 제거하여 퍼즐을 만듦

def create_board():
    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.title("9x9 Sudoku")

    def button_click(row, col):
        """
        버튼을 클릭했을 때 숫자를 입력하는 함수
        """
        if Missing_board[row][col] == " ":  # 원래 비어있던 셀일 때만 수정 가능
            selected_number = spinbox.get()  # Spinbox에서 선택한 숫자 가져오기
            print(f"선택한 숫자: {selected_number}")
            board[row][col] = selected_number
            buttons[row][col].config(text=selected_number)
            # # 입력한 숫자가 행, 열, 서브 그리드 규칙에 맞는지 확인
            # if row_valid(row, selected_number) and col_valid(col, selected_number) and block_valid(row, col, selected_number):
            #     board[row][col] = selected_number
            #     buttons[row][col].config(text=selected_number)  # 버튼의 텍스트 업데이트
            # else:
            #     print("잘못된 입력입니다.")
    '''
    def row_valid(r, num):
        return num not in board[r]

    def col_valid(c, num):
        return num not in [board[i][c] for i in range(9)]

    def block_valid(r, c, num):
        block_row, block_col = r // 3 * 3, c // 3 * 3
        for i in range(3):
            for j in range(3):
                if board[block_row + i][block_col + j] == num:
                    return False
        return True
    '''
    # 보드와 각 버튼을 그릴 프레임 생성
    Chekup_print = ""
    def Checkup():
        if board == origin_board:
            checkup_text.set("완벽합니다.!")
        else:
            checkup_text.set("다시 한번 생각해 보세요.")
    frame = tk.Frame(root)
    frame.pack()

    buttons = [[None for _ in range(9)] for _ in range(9)]

    for r in range(9):
        for c in range(9):
            button_color = 'white'
            if (r // 3 + c // 3) % 2 == 0:
                button_color = 'lightgrey'
            button = tk.Button(frame, text=board[r][c], width=4, height=2, bg=button_color,
                               command=lambda row=r, col=c: button_click(row, col))
            button.grid(row=r, column=c, sticky='nsew')
            buttons[r][c] = button

    # 모든 행과 열의 크기를 동일하게 설정
    for i in range(9):
        frame.grid_rowconfigure(i, weight=1)
        frame.grid_columnconfigure(i, weight=1)

    # Label을 위한 StringVar 생성
    checkup_text = tk.StringVar()
    checkup_text.set("")  # 초기 텍스트는 빈 문자열

    # 중앙 정렬을 위한 프레임 생성
    center_frame = tk.Frame(root)
    center_frame.pack(expand=True)


    # 숫자 선택 Spinbox와 제출 버튼을 수평으로 배치할 프레임 생성
    control_frame = tk.Frame(center_frame)
    control_frame.pack(pady=20)

    spinbox = tk.Spinbox(control_frame, from_=1, to=9, width=10, font=("Helvetica", 20))
    spinbox.pack(side=tk.LEFT, padx=10)

    submit_button = tk.Button(control_frame, text="제출", command=Checkup, font=("Helvetica", 16))
    submit_button.pack(side=tk.LEFT, padx=10)

    # Label 생성 및 변수 연결
    label = tk.Label(center_frame, textvariable=checkup_text, font=("Helvetica", 20))
    label.pack(pady=20)

    # Tkinter 루프 실행
    root.mainloop()

# 보드 생성 함수 호출
create_board()

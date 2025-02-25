import streamlit as st
import matplotlib.pyplot as plt
import random
import time

def draw_columns(n_people):
    """
    인원수에 따라 세로 열만 1200×1200 픽셀 영역에 그립니다.
    (선 두께 7)
    """
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    for i in range(n_people):
        ax.plot([i, i], [0, 12], color='black', lw=7)
    ax.set_xlim(-0.5, n_people - 0.5)
    ax.set_ylim(12, 0)
    ax.axis('off')
    return fig

def generate_ladder(n_people, n_rows):
    """
    인원 수와 층 수에 맞게 사다리의 가로줄(연결선)을 생성합니다.
    연속된 가로선이 생기지 않도록 처리합니다.
    """
    ladder = []
    for _ in range(n_rows):
        row = [False] * (n_people - 1)
        j = 0
        while j < n_people - 1:
            if random.choice([True, False]):
                row[j] = True
                j += 2  # 연속 가로선 방지
            else:
                j += 1
        ladder.append(row)
    return ladder

def simulate_path(ladder, start):
    """
    시작 열(start, 0-indexed)에서 출발하여 사다리를 따라 내려가는 경로를 (x, y) 좌표 리스트로 반환합니다.
    """
    path = []
    current_col = start
    y = 0
    path.append((current_col, y))
    for row in ladder:
        y_mid = y + 0.5
        path.append((current_col, y_mid))
        if current_col > 0 and row[current_col - 1]:
            current_col -= 1
            path.append((current_col, y_mid))
        elif current_col < len(row) and row[current_col]:
            current_col += 1
            path.append((current_col, y_mid))
        y += 1
        path.append((current_col, y))
    return path

def draw_ladder(ladder, n_people, n_rows, markers=None):
    """
    사다리 전체(세로열 + 가로줄)와 진행된 참가자들의 마커(원)를 1200×1200 픽셀 영역에 그립니다.
    선 두께는 7, 마커 크기는 22로 설정합니다.
    markers: (x, y, color) 튜플 리스트
    """
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    for i in range(n_people):
        ax.plot([i, i], [0, n_rows], color='black', lw=7)
    for r, row in enumerate(ladder):
        y = r + 0.5
        for i, has_bar in enumerate(row):
            if has_bar:
                ax.plot([i, i+1], [y, y], color='black', lw=7)
    if markers:
        for (x, y, col) in markers:
            ax.plot(x, y, 'o', markersize=22, color=col)
    ax.set_xlim(-0.5, n_people - 0.5)
    ax.set_ylim(n_rows, 0)
    ax.axis('off')
    return fig

def main():
    # 중앙 정렬된 제목 (h2 태그)
    st.markdown("<h2 style='text-align: center;'>비주얼 사다리 게임</h2>", unsafe_allow_html=True)
    
    # 좌측: 참가자 정보 입력, 우측: 사다리 게임 영역
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        n_people = st.number_input("인원수를 입력하세요:", min_value=2, value=5, step=1)
        st.subheader("참가자 정보 입력")
        cols = st.columns(n_people)
        names = []
        bets = []
        base_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        colors = [base_colors[i % len(base_colors)] for i in range(n_people)]
        for i in range(n_people):
            with cols[i]:
                st.markdown(f"<div style='text-align:center; color:{colors[i]}; font-weight:bold;'>{i+1}번 참가자</div>", unsafe_allow_html=True)
                name = st.text_input("이름", value=f"사람{i+1}", key=f"name_{i}")
                bet = st.text_input("내기명", value=f"내기{i+1}", key=f"bet_{i}")
                names.append(name)
                bets.append(bet)
        start_game = st.button("게임 시작", key="start_button")
    
    with right_col:
        # 상단 여백 확보 후, 1200×1200 픽셀 사다리 영역 표시
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        ladder_placeholder = st.empty()
        fig = draw_columns(n_people)
        ladder_placeholder.pyplot(fig)
        plt.close('all')
    
    if start_game:
        n_rows = random.randint(10, 20)
        ladder = generate_ladder(n_people, n_rows)
        paths = [simulate_path(ladder, i) for i in range(n_people)]
        finished_markers = []
        # 각 참가자의 경로를 순차적으로 애니메이션 (원 이동 속도: 기존 0.05초 대신 0.05/3초 간격)
        for i in range(n_people):
            current_path = paths[i]
            for pos in current_path:
                markers = finished_markers.copy()
                markers.append((pos[0], pos[1], colors[i]))
                fig = draw_ladder(ladder, n_people, n_rows, markers=markers)
                ladder_placeholder.pyplot(fig)
                plt.close('all')
                time.sleep(0.05/3)  # 지연 시간을 0.05초의 1/3로 줄임 (약 0.0167초)
            finished_markers.append((current_path[-1][0], current_path[-1][1], colors[i]))
        results = []
        for i, path in enumerate(paths):
            final_col = path[-1][0] + 1
            results.append(f"{names[i]}({bets[i]}): {final_col}번")
        with left_col:
            st.success("게임 결과: " + ", ".join(results))

if __name__ == '__main__':
    main()

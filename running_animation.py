import sys
import time
import os
import glob

# 윈도우에서 ANSI 코드 사용 활성화
if sys.platform.startswith('win'):
    import colorama
    colorama.init()

def read_frames(directory):
    """ 디렉토리에서 ASCII 아트 프레임 파일을 읽고 정렬하여 반환 """
    frame_files = glob.glob(os.path.join(directory, 'ascii-art*.txt'))

    def get_frame_number(filename):
        """ 파일명에서 숫자 추출하여 정렬 """
        base = os.path.basename(filename)
        if base == 'ascii-art.txt':
            return 0
        try:
            return int(base.split('(')[1].split(')')[0])
        except:
            return float('inf')

    # 파일 정렬
    frame_files.sort(key=get_frame_number)

    frames = []
    for file_path in frame_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[:23]  # 마지막 빈 줄 제외
            frame = ''.join(lines)
            frames.append(frame)

    return frames

def clear_previous_frame(height):
    """이전 프레임을 완전히 지우는 함수"""
    # 커서를 프레임의 시작 위치로 이동
    sys.stdout.write("\033[F" * height)
    # 각 라인을 지움
    for _ in range(height):
        sys.stdout.write("\033[2K")  # 현재 라인을 완전히 지움
        sys.stdout.write("\033[1B")  # 한 라인 아래로 이동
    # 다시 프레임의 시작 위치로 이동
    sys.stdout.write("\033[F" * height)

def main():
    frames = read_frames('running_man_frame')  # 프레임 파일 경로 설정
    frame_count = len(frames)
    frame_height = 24  # 프레임 높이 24로 수정 (인덱스 표시줄 포함)

    # 커서 숨기기
    print("\033[?25l", end="")

    try:
        first_run = True
        while True:
            for idx, frame in enumerate(frames):
                # 프레임에 인덱스 정보 추가
                frame_with_index = frame + f"\n현재 프레임 인덱스: {idx}"
                
                if first_run and idx == 0:
                    # 최초 실행시 첫 프레임만 바로 출력
                    sys.stdout.write(frame_with_index)
                    first_run = False
                else:
                    # 나머지 모든 경우에는 이전 프레임을 지우고 새 프레임 출력
                    clear_previous_frame(frame_height)
                    sys.stdout.write(frame_with_index)

                sys.stdout.flush()  # 출력 버퍼 비우기
                time.sleep(0.1)  # 0.1초 딜레이

    except KeyboardInterrupt:
        pass  # Ctrl+C 입력 시 루프 종료

    finally:
        # 커서 다시 표시
        print("\033[?25h", end="")

if __name__ == "__main__":
    main()

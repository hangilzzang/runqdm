import threading
import sys
import time
import glob
import os
import pkg_resources


class runqdm:
    FRAME_HEIGHT = 24  # 프레임 높이를 24로 수정 (고정 텍스트 줄 포함)
    ANIMATION_DELAY = 0.03

    
    def __init__(self, iterable):
        self.iterable = iterable  # range(10), list 등 반복 가능한 객체 저장
        self.iterator = iter(iterable)  # 내부적으로 iterator 생성
        self.total = len(iterable) if hasattr(iterable, '__len__') else None
        self.current = 0  # 현재 진행 상태
        self.run_animation = True        
        
        # 애니메이션 실행 준비        
        if sys.platform.startswith('win'):
            import colorama
            colorama.init()
            
        self.frames = self.read_frames('running_man_frame')

        # 애니메이션 스레드 시작
        self.animation_thread = threading.Thread(target=self.start_animation)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    

    def __iter__(self):
        return self  # self를 반환하여 이터레이터로 사용 가능하게 함

    def __next__(self):
        try:
            item = next(self.iterator)  # 내부 이터레이터에서 다음 값 가져오기
            self.current += 1  # 진행 상태 증가
            return item  # 실제 값 반환
        except StopIteration:
            self.run_animation = False
            self.animation_thread.join()
            raise StopIteration  # 반복 종료

    def start_animation(self):
        
        print("\033[?25l", end="") # 커서 숨기기
        
        while self.run_animation:
            self.play_animation_cycle(self.frames)

        print("\033[?25h", end="") # 커서 보이기
    
    def play_animation_cycle(self, frames):
        for frame in frames:
            if not self.run_animation:  # 각 프레임 시작 전에 체크
                break
            next_frame = frame + "\n고정된 텍스트 라인"
            sys.stdout.write(f"\033[{self.FRAME_HEIGHT}F")
            sys.stdout.write(next_frame)
            sys.stdout.flush()
            time.sleep(self.ANIMATION_DELAY)
        
    def read_frames(self, directory):
        """ 디렉토리에서 ASCII 아트 프레임 파일을 읽고 정렬하여 반환 """
        frame_path = pkg_resources.resource_filename('runqdm', directory)

        frame_files = glob.glob(os.path.join(frame_path, 'ascii-art*.txt'))
        
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

    def clear_previous_frame(self, height):
        """이전 프레임을 완전히 지우는 함수"""
        # 커서를 프레임의 시작 위치로 이동
        sys.stdout.write("\033[F" * height)
        # 각 라인을 지움
        for _ in range(height):
            sys.stdout.write("\033[2K")  # 현재 라인을 완전히 지움
            sys.stdout.write("\033[1B")  # 한 라인 아래로 이동
        # 다시 프레임의 시작 위치로 이동
        sys.stdout.write("\033[F" * height)
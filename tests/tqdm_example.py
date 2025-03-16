from tqdm import tqdm
import time
# import numpy as np

def basic_example():
    """기본적인 tqdm 사용 예제"""
    for i in tqdm(range(10), desc="🏃 running"):
        time.sleep(0.5)  # 각 단계마다 0.5초 대기


if __name__ == "__main__":
    basic_example()
    


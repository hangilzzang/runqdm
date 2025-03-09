from tqdm import tqdm
import time
# import numpy as np

def basic_example():
    """기본적인 tqdm 사용 예제"""
    for i in tqdm(range(10), desc="진행 중"):
        time.sleep(0.5)  # 각 단계마다 0.5초 대기

def list_processing():
    """리스트 처리 예제"""
    numbers = list(range(1000))
    squares = []
    
    for num in tqdm(numbers, desc="제곱 계산 중"):
        squares.append(num ** 2)
        time.sleep(0.01)

# def numpy_example():
#     """NumPy 배열 처리 예제"""
#     data = np.random.rand(1000, 1000)
#     result = []
    
    # for row in tqdm(data, desc="행렬 처리 중"):
    #     result.append(np.mean(row))
    #     time.sleep(0.01)

if __name__ == "__main__":
    basic_example()
    
#     print("\n2. 리스트 처리 예제 실행")
#     list_processing()
    
#     print("\n3. NumPy 배열 처리 예제 실행")
#     numpy_example()

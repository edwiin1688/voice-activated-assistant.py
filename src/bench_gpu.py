import torch
import time

def benchmark_gpu():
    if not torch.cuda.is_available():
        print("CUDA not available")
        return
    
    device = "cuda"
    print(f"Testing GPU: {torch.cuda.get_device_name(0)}")
    
    # 建立大矩陣
    size = 4096
    a = torch.randn(size, size, device=device, dtype=torch.float16)
    b = torch.randn(size, size, device=device, dtype=torch.float16)
    
    # 預熱
    for _ in range(10):
        torch.matmul(a, b)
    torch.cuda.synchronize()
    
    # 計時
    start = time.time()
    iters = 100
    for _ in range(iters):
        torch.matmul(a, b)
    torch.cuda.synchronize()
    end = time.time()
    
    avg_time = (end - start) / iters * 1000
    print(f"Average 4096x4096 matrix mult time: {avg_time:.2f} ms")
    print(f"TFLOPS: { (2 * size**3) / (avg_time / 1000) / 1e12 :.2f}")

if __name__ == "__main__":
    benchmark_gpu()

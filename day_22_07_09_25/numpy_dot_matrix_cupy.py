import torch
import time
import random
import numpy as np
from typing import Tuple

# Wybór urządzenia: GPU jeśli dostępne, inaczej CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Używane urządzenie: {device}")

# Funkcja generująca losową macierz 2D jako tensor
def generate_random_tensor(shape: Tuple[int, int]) -> torch.Tensor:
    cpu_data = [
        [random.random() for _ in range(shape[1])]
        for _ in range(shape[0])
    ]
    return torch.tensor(cpu_data, dtype=torch.float32).to(device)

# Tworzenie dwóch macierzy na wybranym urządzeniu
TORCH_ARRAY_A = generate_random_tensor((500, 500))
TORCH_ARRAY_B = generate_random_tensor((500, 500))

# Mnożenie macierzy na GPU lub CPU (zależnie od dostępności)
print("=" * 30)
start_time = time.time()
gpu_result = torch.matmul(TORCH_ARRAY_A, TORCH_ARRAY_B)
gpu_exec_time = time.time() - start_time
print(f"Czas wykonania na {device}: {gpu_exec_time:.6f} s")

# Konwersja tensorów do NumPy (CPU) i porównanie
CPU_ARRAY_A = TORCH_ARRAY_A.cpu().numpy()
CPU_ARRAY_B = TORCH_ARRAY_B.cpu().numpy()

start_time = time.time()
numpy_result = np.dot(CPU_ARRAY_A, CPU_ARRAY_B)
cpu_exec_time = time.time() - start_time
print(f"Czas wykonania na CPU (NumPy): {cpu_exec_time:.6f} s")

# Porównanie wyników
diff = torch.sum(torch.abs(gpu_result.cpu() - torch.tensor(numpy_result)))
print(f"Różnica między GPU a CPU: {diff.item():.10f}")
print(f"Zgodność wyników: {diff.item() < 1e-5}")


# Używane urządzenie: cpu
# ==============================
# Czas wykonania na cpu: 0.002916 s
# Czas wykonania na CPU (NumPy): 0.005245 s
# Różnica między GPU a CPU: 3.9742736816
# Zgodność wyników: False
#
# Process finished with exit code 0
# Używane urządzenie: cpu
# ==============================
# Czas wykonania na cpu: 0.006327 s
# Czas wykonania na CPU (NumPy): 0.000375 s
# Różnica między GPU a CPU: 0.0000000000
# Zgodność wyników: True
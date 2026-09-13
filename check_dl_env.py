import sys
import platform
import subprocess

print("=" * 70)
print("        Deep Learning Environment Check")
print("=" * 70)

# ==============================
# Python信息
# ==============================
print("\n[Python]")
print("Python Version:")
print(sys.version)
print("Platform:")
print(platform.platform())

# ==============================
# pip版本
# ==============================
print("\n[Pip]")
try:
    import pip
    print("pip version:")
    print(pip.__version__)
except Exception:
    print("pip not found")

# ==============================
# PyTorch
# ==============================
print("\n[PyTorch]")
try:
    import torch
    print("torch:")
    print(torch.__version__)
    print("torch CUDA:")
    print(torch.version.cuda)
    print("CUDA Available:")
    print(torch.cuda.is_available())
    if torch.cuda.is_available():
        print("\nGPU Information:")
        device = torch.cuda.current_device()
        print("GPU ID:")
        print(device)

        print("GPU Name:")
        print(torch.cuda.get_device_name(device))

        prop = torch.cuda.get_device_properties(device)

        print("Compute Capability:")
        print(
            f"{prop.major}.{prop.minor}"
        )

        print("GPU Memory Total:")
        print(
            f"{prop.total_memory / 1024**3:.2f} GB"
        )

        allocated = (
            torch.cuda.memory_allocated(device)
            /1024**3
        )

        reserved = (
            torch.cuda.memory_reserved(device)
            /1024**3
        )

        print("Memory Allocated:")
        print(
            f"{allocated:.3f} GB"
        )

        print("Memory Reserved:")
        print(
            f"{reserved:.3f} GB"
        )

except Exception as e:

    print("PyTorch Error:")
    print(e)
# ==============================
# torchvision
# ==============================
print("\n[TorchVision]")
try:
    import torchvision
    print(
        "torchvision:"
    )
    print(
        torchvision.__version__
    )
except Exception as e:
    print(e)
# ==============================
# torchaudio
# ==============================
print("\n[TorchAudio]")
try:
    import torchaudio
    print(
        "torchaudio:"
    )

    print(
        torchaudio.__version__
    )
except Exception as e:
    print(e)
# ==============================
# D2L
# ==============================
print("\n[D2L]")

try:
    import d2l
    print(
        "d2l:"
    )
    print(
        d2l.__version__
    )
except Exception as e:
    print(e)

# ==============================
# AI常用库
# ==============================
packages = [
    "numpy",
    "matplotlib",
    "pandas",
    "sklearn",
    "jupyter",
    "notebook"

]

print("\n[Python AI Packages]")
for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(
            module,
            "__version__",
            "unknown"
        )

        print(
            f"{pkg:<15}: {version}"
        )

    except Exception:
        print(
            f"{pkg:<15}: Not Installed"
        )
# ==============================
# NVIDIA驱动
# ==============================
print("\n[NVIDIA Driver]")
try:
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total",
            "--format=csv"
        ],
        capture_output=True,
        text=True
    )

    print(
        result.stdout
    )
except Exception:
    print(
        "nvidia-smi unavailable"
    )

print("=" * 70)
print(
    "Environment Check Finished"
)
print("=" * 70)
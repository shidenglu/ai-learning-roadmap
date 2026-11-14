import os
import sys
import subprocess
from pathlib import Path


# ============================================================
# Wan2.2-Animate 环境检查脚本
# ============================================================

ROOT = Path.cwd()

print("=" * 70)
print("Wan2.2-Animate Environment Check")
print("=" * 70)


# ------------------------------------------------------------
# 1. Python
# ------------------------------------------------------------
print("\n[1] Python")

print("Python      :", sys.version.replace("\n", " "))
print("Executable  :", sys.executable)


# ------------------------------------------------------------
# 2. Conda
# ------------------------------------------------------------
print("\n[2] Conda")

print("CONDA_PREFIX:", os.environ.get("CONDA_PREFIX", "N/A"))
print("CONDA_DEFAULT_ENV:",
      os.environ.get("CONDA_DEFAULT_ENV", "N/A"))


# ------------------------------------------------------------
# 3. PyTorch
# ------------------------------------------------------------
print("\n[3] PyTorch")

try:
    import torch

    print("Torch       :", torch.__version__)
    print("Torch CUDA  :", torch.version.cuda)
    print("CUDA avail  :", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU         :", torch.cuda.get_device_name(0))
        print("GPU count   :", torch.cuda.device_count())

        props = torch.cuda.get_device_properties(0)

        print(
            "VRAM        : %.2f GB"
            % (props.total_memory / 1024 ** 3)
        )

        print("Compute Cap :", f"{props.major}.{props.minor}")

        print(
            "Allocated   : %.2f GB"
            % (torch.cuda.memory_allocated(0) / 1024 ** 3)
        )

        print(
            "Reserved    : %.2f GB"
            % (torch.cuda.memory_reserved(0) / 1024 ** 3)
        )

except Exception as e:
    print("PyTorch ERROR:", repr(e))


# ------------------------------------------------------------
# 4. CUDA Toolkit
# ------------------------------------------------------------
print("\n[4] CUDA Toolkit")

print("CUDA_PATH   :", os.environ.get("CUDA_PATH", "N/A"))

try:
    result = subprocess.run(
        ["nvcc", "--version"],
        capture_output=True,
        text=True
    )

    print(result.stdout.strip())

    if result.stderr.strip():
        print("nvcc stderr :", result.stderr.strip())

except Exception as e:
    print("nvcc ERROR  :", repr(e))


# ------------------------------------------------------------
# 5. NVIDIA Driver
# ------------------------------------------------------------
print("\n[5] NVIDIA Driver")

try:
    result = subprocess.run(
        ["nvidia-smi"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

except Exception as e:
    print("nvidia-smi ERROR:", repr(e))


# ------------------------------------------------------------
# 6. Python Packages
# ------------------------------------------------------------
print("\n[6] Python Packages")

packages = [
    "torch",
    "torchvision",
    "torchaudio",
    "transformers",
    "huggingface_hub",
    "tokenizers",
    "safetensors",
    "einops",
    "moviepy",
    "opencv-python",
    "Pillow",
    "numpy",
    "scipy",
]

try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show"] + packages,
        capture_output=True,
        text=True
    )

    print(result.stdout)

except Exception as e:
    print("pip ERROR:", repr(e))


# ------------------------------------------------------------
# 7. SAM2
# ------------------------------------------------------------
print("\n[7] SAM2")

SAM2_PATH = ROOT.parent.parent / "sam2-0e78a118995e66bb27d78518c4bd9a3e95b4e266"

print("Expected path:")
print(SAM2_PATH)

if SAM2_PATH.exists():
    print("SAM2 path  : OK")

    try:
        import sam2

        print("SAM2 import: OK")
        print("SAM2 file  :", sam2.__file__)

    except Exception as e:
        print("SAM2 import ERROR:", repr(e))

else:
    print("SAM2 path  : NOT FOUND")


# ------------------------------------------------------------
# 8. Wan
# ------------------------------------------------------------
print("\n[8] Wan")

try:
    import wan

    print("Wan import : OK")
    print("Wan file   :", wan.__file__)

except Exception as e:
    print("Wan import ERROR:", repr(e))


# ------------------------------------------------------------
# 9. Project Structure
# ------------------------------------------------------------
print("\n[9] Project Structure")

paths = {
    "generate.py":
        ROOT / "generate.py",

    "wan":
        ROOT / "wan",

    "model":
        ROOT / "Wan2.2-Animate-14B",

    "process_checkpoint":
        ROOT / "Wan2.2-Animate-14B" / "process_checkpoint",

    "input":
        ROOT / "input",

    "video":
        ROOT / "input" / "video.mp4",

    "video_50":
        ROOT / "input" / "video_50.mp4",

    "person":
        ROOT / "input" / "person.JPG",

    "person_832":
        ROOT / "input" / "person_832.jpg",

    "output_50":
        ROOT / "output_50",

    "output_832_50":
        ROOT / "output_832_50",
}

for name, path in paths.items():

    if path.exists():

        if path.is_dir():
            print(f"{name:20s}: OK  {path}")

        else:
            size_mb = path.stat().st_size / 1024 / 1024
            print(
                f"{name:20s}: OK  "
                f"{path}  ({size_mb:.2f} MB)"
            )

    else:
        print(f"{name:20s}: NOT FOUND  {path}")


# ------------------------------------------------------------
# 10. process_checkpoint
# ------------------------------------------------------------
print("\n[10] process_checkpoint")

checkpoint = (
    ROOT
    / "Wan2.2-Animate-14B"
    / "process_checkpoint"
)

if checkpoint.exists():

    for item in checkpoint.iterdir():

        if item.is_dir():
            print("[DIR ]", item.name)

        else:
            print("[FILE]", item.name)

else:

    print("process_checkpoint NOT FOUND")


# ------------------------------------------------------------
# 11. GPU Memory Test
# ------------------------------------------------------------
print("\n[11] GPU Memory")

try:

    import torch

    if torch.cuda.is_available():

        torch.cuda.empty_cache()

        free, total = torch.cuda.mem_get_info()

        print(
            "Free VRAM   : %.2f GB"
            % (free / 1024 ** 3)
        )

        print(
            "Total VRAM  : %.2f GB"
            % (total / 1024 ** 3)
        )

        print(
            "Used VRAM   : %.2f GB"
            % ((total - free) / 1024 ** 3)
        )

    else:

        print("CUDA unavailable")

except Exception as e:

    print("GPU memory ERROR:", repr(e))


# ------------------------------------------------------------
# 12. Key Configuration
# ------------------------------------------------------------
print("\n[12] Environment Variables")

for key in [
    "CUDA_PATH",
    "CUDA_HOME",
    "PATH",
]:

    value = os.environ.get(key)

    if key == "PATH" and value:

        print("PATH:")
        for p in value.split(os.pathsep):

            if "CUDA" in p.upper():
                print("  ", p)

    else:

        print(f"{key:12s}: {value}")


# ------------------------------------------------------------
# 13. Final Summary
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("CHECK FINISHED")
print("=" * 70)

print("\n当前工作目录:")
print(ROOT)

print("\n建议重点关注:")
print("1. CUDA avail")
print("2. GPU")
print("3. VRAM")
print("4. Torch CUDA")
print("5. CUDA_PATH")
print("6. nvcc version")
print("7. SAM2 import")
print("8. Wan import")
print("9. process_checkpoint")
print("10. input / output 文件")

import torch
from diffusers import WanPipeline
from diffusers.utils import export_to_video


# =========================
# 1. 加载模型
# =========================

model_id = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

pipe = WanPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16
)

pipe = pipe.to("cuda")


# =========================
# 2. 设置提示词
# =========================

prompt = """
A cute orange cat sitting inside a futuristic spaceship,
looking through the window at the galaxy,
stars moving slowly outside,
cinematic lighting,
smooth camera movement,
high quality
"""


# =========================
# 3. 生成视频
# =========================

output = pipe(
    prompt=prompt,
    num_frames=81,
    height=480,
    width=832,
    guidance_scale=5.0
).frames[0]


# =========================
# 4. 保存 MP4
# =========================

export_to_video(
    output,
    "output.mp4",
    fps=16
)

print("视频生成完成：output.mp4")
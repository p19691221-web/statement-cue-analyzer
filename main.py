"""
陳述線索分析器 - 研究用原型
NOT a lie detector. 僅輸出可觀測線索。
"""
import cv2
import mediapipe as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LEFT = [33, 160, 158, 133, 153, 144]
RIGHT = [362, 385, 387, 263, 373, 380]
EAR_THRESHOLD = 0.21
MIN_CLOSED_FRAMES = 2  # 連續低於門檻的幀數，過濾單幀雜訊


def _dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def _ear(pts, idx):
    p = [pts[i] for i in idx]
    return (_dist(p[1], p[5]) + _dist(p[2], p[4])) / (2 * _dist(p[0], p[3]) + 1e-6)


def analyze_video(video_path):
    if not video_path:
        raise ValueError("未收到影片")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"無法開啟影片：{video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    times, ears = [], []
    blinks, closed_run, n = 0, 0, 0
    with mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            n += 1
            res = mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if not res.multi_face_landmarks:
                closed_run = 0
                continue
            h, w = frame.shape[:2]
            lm = res.multi_face_landmarks[0].landmark
            pts = [(l.x * w, l.y * h) for l in lm]
            e = (_ear(pts, LEFT) + _ear(pts, RIGHT)) / 2
            times.append(n / fps)
            ears.append(e)
            if e < EAR_THRESHOLD:
                closed_run += 1
            else:
                if closed_run >= MIN_CLOSED_FRAMES:
                    blinks += 1
                closed_run = 0
    cap.release()

    if n == 0:
        raise ValueError("影片沒有可讀取的畫面")
    if not ears:
        raise ValueError("整段影片都沒有偵測到臉部")

    duration = n / fps
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(times, ears, linewidth=1)
    ax.axhline(EAR_THRESHOLD, color="red", linestyle="--",
               label=f"blink threshold {EAR_THRESHOLD}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("EAR")
    ax.legend(loc="upper right")
    fig.tight_layout()

    return {
        "ear_plot": fig,
        "blink_count": blinks,
        "mean_ear": float(np.mean(ears)),
        "duration_s": duration,
        "blinks_per_min": blinks / duration * 60,
        "face_coverage": len(ears) / n,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法：python main.py video.mp4")
    else:
        r = analyze_video(sys.argv[1])
        print(f"時長：{r['duration_s']:.1f}s，眨眼：{r['blink_count']}"
              f"（{r['blinks_per_min']:.1f} 次/分鐘）")
        print(f"平均 EAR：{r['mean_ear']:.3f}，臉部偵測覆蓋率：{r['face_coverage']:.0%}")
        print("僅為行為線索，無法判斷是否說謊。")

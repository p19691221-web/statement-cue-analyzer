"""
陳述線索分析器 - 研究用原型
NOT a lie detector. 僅輸出可觀測線索。
"""
import cv2
import mediapipe as mp
import numpy as np

mp_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True)

LEFT = [33,160,158,133,153,144]
RIGHT = [362,385,387,263,373,380]

def dist(a,b): return np.linalg.norm(np.array(a)-np.array(b))

def ear(pts, idx):
    p = [pts[i] for i in idx]
    return (dist(p[1],p[5])+dist(p[2],p[4]))/(2*dist(p[0],p[3])+1e-6)

def analyze(video):
    cap = cv2.VideoCapture(video)
    blinks = 0
    ears = []
    n = 0
    was_closed = False

    while True:
        ret, frame = cap.read()
        if not ret: break
        n+=1
        if n%10!=0: continue
        h,w,_=frame.shape
        res = mp_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not res.multi_face_landmarks: continue
        lm = res.multi_face_landmarks[0].landmark
        pts = [(int(l.x*w), int(l.y*h)) for l in lm]
        e = (ear(pts, LEFT)+ear(pts, RIGHT))/2
        ears.append(e)
        if e<0.21:
            if not was_closed:
                blinks+=1
                was_closed=True
        else:
            was_closed=False

    cap.release()
    print(f"影片: {video}")
    print(f"分析幀: {n}, 觀察眨眼: {blinks}")
    print(f"平均EAR: {np.mean(ears):.3f}" if ears else "無臉部資料")
    print("結論: 僅為行為線索，無法判斷是否說謊。")
    print("免責: 禁止用於指控特定人物。")

if __name__=="__main__":
    import sys
    if len(sys.argv)<2:
        print("用法: python main.py video.mp4")
    else:
        analyze(sys.argv[1])

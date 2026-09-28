# Statement Cue Analyzer · 陳述線索分析器

A browser-based behavioral cue analyzer for research and education. **It is not a lie detector.**

**Live demo:** https://p19691221-web.github.io/statement-cue-analyzer/

## What it measures

From a face video, it reports only what can be observed:

- Blink count and blinks per minute
- Mean eye aspect ratio (EAR)
- Long eye closures (> 0.5 s), reported separately from blinks
- Face coverage (share of frames where a face was detected)
- EAR curve over time, with the threshold used for that video

## What it does not do

- **No deception judgment.** Stress ≠ lying. Fatigue, lighting, eyewear and camera angle all change these numbers.
- **No emotion or intent inference.**
- **No face identification.**
- **Not for** hiring, legal review, or accusations against a specific person.

## Privacy

The web version runs entirely in your browser. Your video is never uploaded. The only network requests are for the MediaPipe library and the face detection model, downloaded from public CDNs.

## Method

- MediaPipe Face Landmarker; EAR computed from 6 landmarks per eye, averaged across both eyes
- Sampled at 30 fps
- Adaptive threshold per video: 75% of the open-eye baseline (80th-percentile EAR)
- A blink is a closure lasting 2 samples up to 0.5 s; longer closures (looking down, squinting) are counted separately
- Invalid input fails with an error. The tool never substitutes placeholder data.

## Limitations

- Short clips give unstable rates. One extra blink in an 11-second clip changes the result by about 5 per minute. Use 30–60 s.
- Segments where EAR hovers near the threshold can be classified either way.
- Glasses, low-angle cameras and poor lighting reduce landmark accuracy.
- There is no population baseline. Numbers are not comparable across people or recording conditions.

## Files

| File | Purpose |
|---|---|
| `index.html` | Web version (reference implementation), served by GitHub Pages |
| `main.py` | Python command-line version |
| `app.py` | Gradio UI for the Python version |
| `requirements.txt` | Python dependencies |

## Running the Python version

```bash
pip install -r requirements.txt
python main.py your_video.mp4   # command line
python app.py                   # Gradio UI at http://127.0.0.1:7860
```

The Python version uses MediaPipe's legacy `mp.solutions` API. MediaPipe 1.0+ no longer includes it, so install a 0.10.x release, for example `pip install "mediapipe==0.10.21"`. The Python version still uses a fixed threshold (0.21). The web version's adaptive method is the reference.

## 中文摘要

本工具僅輸出可觀測的行為線索（眨眼次數、眨眼率、眼睛長寬比），**不是測謊儀，無法判斷一個人是否說謊**。緊張不等於說謊。網頁版完全在瀏覽器內處理，影片不會上傳。禁止用於求職面試、法律審查、針對特定人物的指控。僅供研究與教育用途。

## License

MIT. See `LICENSE`.

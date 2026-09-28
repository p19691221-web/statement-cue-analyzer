import gradio as gr
from main import analyze_video # 你原本的函數

def ui_analyze(video_path):
    result = analyze_video(video_path)
    # 只回傳線索，不回傳說謊判斷
    return result["ear_plot"], f"Blink: {result['blink_count']} | Mean EAR: {result['mean_ear']:.2f}\n\n[Compliance] Behavioral cue only, NOT lie detection. Stress!= Lying."

with gr.Blocks(title="Statement Cue Analyzer") as demo:
    gr.Markdown("# Statement Cue Analyzer | Behavioral Cue Only - NOT a Lie Detector")
    gr.Markdown("Local-only. No face ID. No deception judgment.")
    with gr.Row():
        video_in = gr.Video(label="1. Upload Video")
        with gr.Column():
            plot_out = gr.Plot(label="2. EAR Curve")
            text_out = gr.Textbox(label="Results")
    btn = gr.Button("Analyze", variant="primary")
    btn.click(ui_analyze, inputs=video_in, outputs=[plot_out, text_out])

demo.launch()

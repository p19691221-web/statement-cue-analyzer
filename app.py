import gradio as gr
from main import analyze_video # 你原本的函數

def ui_analyze(video_path):
    try:
        r = analyze_video(video_path)
    except ValueError as e:
        raise gr.Error(str(e))
    text = (f"Blink: {r['blink_count']} ({r['blinks_per_min']:.1f}/min) | "
            f"Mean EAR: {r['mean_ear']:.2f} | Face coverage: {r['face_coverage']:.0%}\n\n"
            "[Compliance] Behavioral cue only, NOT lie detection. Stress != Lying.")
    return r["ear_plot"], text
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

"""Disable Gradio server launch during headless CI notebook execution."""

try:
    import gradio as gr
except Exception:
    gr = None


def _launch_noop(self, *args, **kwargs):
    print("[stub] gradio launch skipped for headless CI execution")
    return self


if gr is not None:
    if hasattr(gr, "Blocks"):
        gr.Blocks.launch = _launch_noop
    if hasattr(gr, "Interface"):
        gr.Interface.launch = _launch_noop

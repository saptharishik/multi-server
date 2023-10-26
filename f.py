import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.Pipeline()

# Create elements
src = Gst.ElementFactory.make("videotestsrc", "source")
sink = Gst.ElementFactory.make("autovideosink", "sink")

# Add elements to the pipeline
pipeline.add(src)
pipeline.add(sink)

# Link elements
src.link(sink)

# Set the pipeline to "playing" state
pipeline.set_state(Gst.State.PLAYING)

# Wait until error or EOS
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Parse message
if msg:
    if msg.type == Gst.MessageType.ERROR:
        err, debug_info = msg.parse_error()
        print(f"Error received from element {msg.src.get_name()}: {err} - {debug_info}")
    elif msg.type == Gst.MessageType.EOS:
        print("End-Of-Stream reached")

# Set the pipeline to "null" state
pipeline.set_state(Gst.State.NULL)

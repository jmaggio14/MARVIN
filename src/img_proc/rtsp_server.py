import cv2
import numpy as np
import marvin


class RtspStreamer(object):
    def __init__(self,
                    fps=30.0,
                    ip_address="127.0.0.1",
                    port=9999,
                    encoder="x264enc",
                    noise_reduction="10000",
                    byte_stream="true",
                    threads=4,
                    ):
        self.fps = fps
        gstreamer_kwargs = {"encoder":encoder,
                            "noise_reduction":noise_reduction,
                            "byte_stream":byte_stream,
                            "threads":threads,
                            "ip_address":ip_address,
                            "port":port,
                            }
        self.gstreamer_string = \
        """
        appsrc ! videoconvert ! {encoder} noise-reduction={noise_reduction}\
        tune=zerolatency byte-stream={byte_stream} threads = {threads} !\
        mpegtsmux ! udpsink host={ip_address} port={port}
        """.format(**gstreamer_kwargs)
        print(self.gstreamer_string)

        self.__is_initialized = False

    def __init(self,size):
        """
        opens and initializes the videowriter
        """
        self._h,self._w = size
        marvin.Status.info("initializing the RtspStreamer...")
        self.kwargs = {"filename":self.gstreamer_string,
                        "fourcc":0,
                        "fps":self.fps,
                        "frameSize":(self._w,self._h)}
        self.writer = cv2.VideoWriter( **self.kwargs )

        self.__is_initialized = True

    def write(self,frame):
        """
        writes a frame to the video stream.
        automatically opens a video writer set to the input frame size
            frame: input frame to save to file
        return::
            None
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        if not self.writer.isOpened():
            self.writer.open( **self.kwargs )

        self.writer.write(frame)

    def release(self):
        """
        closes the video writer, ironically creates opens the videowriter
        if it's not already open
        input::
            None
        return::
            None
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        self.writer.release()

    def reopen(self):
        """
        closes and reopens the VideoWriter. ironically creating it if it doesn't
        exist
        """
        if not self.__is_initialized:
            size = marvin.frameSize(frame)
            self.__init(size)

        if self.writer.isOpened():
            self.writer.release()
        self.writer.open( **self.kwargs )


if __name__ == "__main__":
    marvin.init(10)
    marvin.Status.warning("""testing rtsp video streamer, relies on a camera being on /dev/video0""")

    cap = marvin.CameraCapture(0)
    timer = marvin.Timer()
    timer.countdown = 30
    streamer = RtspStreamer()
    viewer = marvin.Cv2ImageViewer("rtsp streamer test")

    while timer.countdown:
        frame = cap.read()
        viewer.view(frame)
        streamer.write(frame)
        print(timer.countdown)















# import gi
# gi.require_version("Gst","1.0")
# from gi.repository import Gst,GObject,GstVideo
# from gi.repository import GdkX11,GstVideo
#
# class GTK_main(object):
#
# import os
# import gi
# gi.require_version("Gst","1.0")
# from gi.respository import Gst,GObject,Gtk
#
#
# class GTK_Main(object):
#     def __init__(self):
#         window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
#         window.set_title("Mpeg2-Player")
#         window.set_default_size(500,400)
#         window.connect("destroy",Gtk.main_quit,"WM destroy")
#         vbox = Gtk.VBox()
#         window.add(vbox)
#         hbox = Gtk.HBox()
#         vbox.pack_start(hbox,False,False,0)
#         self.entry = Gtk.Entry()
#         hbox.add(self.entry)
#         self.button = Gtk.Button("Start")
#         hbox.pack_start(self.button,False,False,0)
#         self.button.connect("clicked",self.start_stop)
#         self.novie_window = Gtk.DrawingArea()
#         vbox.add(self.movie_window)
#         window.show_all()
#
#
#         self.player = Gst.Pipeline.new("player")
#         source = Gst.ElementFactory.make("filesrc","file-source")
#         demuxer = Gst.ElementFactory.make("mpegpsdemux","demuxer")
#

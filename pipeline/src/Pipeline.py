#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#


class Pipeline(object):
    def __init__(cls,pipeline_name,data_ip,out_ip,**kwargs):
        self.pipeline_name = pipeline_name
        self.data_ip = data_ip
        self.out_ip = out_ip
        self.kwargs = kwargs
        self._is_closed = False


    def get_payload_data(self,**kwargs):
        pass

    def process_payload_data(self,**kwargs):
        pass

    def communicate_with_control_loop(self,**kwargs):
        pass

    def mainloop(self,**kwargs):
        # get data
        self.get_payload_data(**kwargs)
        # process data
        self.process_payload_data(**kwargs)
        # send actions to control loop
        self.communicate_with_control_loop(**kwargs)

    def close(self):
        self._is_closed = True

    def is_closed(self):
        return self._is_closed

    def get_pipeline_name(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out_str = "Marvin Pipeline Object -- '{name}'"
                                            .format(name=self.pipeline_name)
        return out_str

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.close()
        return False

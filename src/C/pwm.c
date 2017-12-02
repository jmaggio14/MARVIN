#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>


int pulseWidthModulation(int pin_number, uint32_t on_time,uint32_t off_time){
    /*
    INCOMPLETE!

    There is currently no way to change, kill or modify this function after it is called
    We'll have to figure out a way to communicate with it over a pipe or some other method
    from Python
    */
    //creating file path
    char value_path[80];
    char break_path[80];
    sprintf(value_path,"/sys/class/gpio/gpio%d/value",pin_number);
    sprintf(break_path,"gpio%d_break_pipe",pin_number);
    printf("value_path:%s\n",value_path );
    printf("break_path:%s\n",break_path );
    char on_signal = '1';
    char off_signal = '0';

    //creating file pointers that
    FILE* fp;
    fp = fopen(value_path,"w");
    int fd = open(break_path,O_RDONLY | O_NONBLOCK);
    ssize_t break_read_size;
    int break_value = 0;
    while(1){
      break_read_size = read(fd,&break_value,4);
      if ( break_value == 1){
        break;
      }
      fwrite(&on_signal,1,1,fp);
      usleep(on_time);
      fwrite(&off_signal,1,1,fp);
      usleep(on_time);
    }
    return 0;
}

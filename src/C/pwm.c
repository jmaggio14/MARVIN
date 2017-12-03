#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>


int pulseWidthModulation(int pin_number, char* break_path_p, uint32_t on_time,uint32_t off_time){
    /*
    INCOMPLETE!

    There is currently no way to change, kill or modify this function after it is called
    We'll have to figure out a way to communicate with it over a pipe or some other method
    from Python
    */
    //creating file path
    char value_path[80];
    sprintf(value_path,"/sys/class/gpio/gpio%d/value",pin_number);
    char on_signal = '1';
    char off_signal = '0';

    //creating file pointers for the gpio value file
    FILE* value_fp = fopen(value_path,"w");
    //creating file ids for the break_path_p pipe
    int fd = open(*break_path_p, O_RDONLY | O_NONBLOCK);
    char break_value = '0';
    ssize_t break_value_size;

    while(1){
      break_read_size = read(fd,&break_value,sizeof(char));
      if (break_value == '1'){
        break;
      }
      fwrite(&on_signal,1,1,value_fp);
      usleep(on_time);
      fwrite(&off_signal,1,1,value_fp);
      usleep(off_time);
    }
    return 0;
}

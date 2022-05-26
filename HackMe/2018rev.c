#include <sys/time.h>
#include <unistd.h>
#include <sys/types.h>
#include<stdio.h>

int main(int argc, char* argv[], char* envp[])
{
  int rc = 0;
  struct timeval now;

  now.tv_sec=1514764800;
  now.tv_usec=0;
  rc=settimeofday(&now, NULL);

  if(rc==0)
  {
    char str[20] = "123";
    str[0] = 1;
    argv[0] = str;
    envp[0] = str;
    execve("./2018.rev" , argv, envp);
  }
  else
  {
    printf("fail to set time\n");
  }
  return 0;
}
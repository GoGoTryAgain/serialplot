# serialplot
A python application that plots serial data in real time. Useful for visualizing data from microcontrollers. Originally written for Windows, others have used on linux. See it in action here: https://www.youtube.com/watch?v=FdZKBGY49SI

![alt tag](https://raw.githubusercontent.com/crxguy52/serialplot/master/screenshot.png)

#Requirements
Python - serialplot is written so that it can be run with py2 or py3. However, there are some issues with matplotlib and py3 on windows. See the wiki for more details.

Pyserial - Obviously

matplotlib - I used matplotlib's animate function to draw the graphs. It would definitely be faster to draw the plots using a tk canvas, but I'm also lazy.


how to use? 
(i'm for china,and is not good at english,if somewhere is wrong ,please help me correct )
the software accepts the string data from serialtool. Use the string mode to send the data that you want to show.  If you just need one line,you can send one data every time,such as "-1\r\n" "-2\r\n" (windows). If you want show 2 line at the same time, you can send two line data with a ','.For example,"-1,-3\r\n","-3,-2",so the first line data is '-1' and '-3',the second line data is '-3'and '-2'. You will see the two line picture at the same time.

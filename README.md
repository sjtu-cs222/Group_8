Implementation of Comstant Distribution Matching
==

This is a project about distribution matching.

Files 
--

dm.py is the class file, and main.py is an demo. Put both of them in the same folder, compile and run main.py. The demo will output the imformation of default distribution matcher and started initialization. And it will print randonly generated 1/0 input and corresponding output, as well as the result of decoding (which is the same with input bits of course).  
To modify the demo, just edit main.py. In line 11 the attributes of matcher is determined. The meaning of these parameter is proposed in dm.py. If you want to change the input length, remember to modify the input generation function (line 4 to line 8). And make sure the output symbols should include more information than input bits (an fundamental of information theory), which means more intervals in this algorithm.


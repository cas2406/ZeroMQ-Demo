ZeroMQ Demo

This is just a small demo to show how you could use zeromq to communicate between multiple process. 

For some more info on zeromq, and why it is not just tcp sockets see: http://zeromq.org/topics:omq-is-just-sockets

To run the demo run main.py and robot.py in two different consoles

---------------------------------------------------------------------
[WORK IN PROGRESS]
[ANY FEEDBACK IS WELCOME]

Below i will explain why i chose for creating two different programs that run separately and communicate over ZeroMQ.
The explanation will go a bit deeper in to how python executes code, which can be a bit hard to understand however it only
just touches the surface.

programming languages generally fall into two programming categories; compiled and interpreted languages.
the differences between interpreted and compiled languages boils down to the following. 
When you run a compiled language ( C++ for example ) it first needs to be compiled before you can execute it.
During compilation your code will be converted to machine-specific instructions ( not every pc is the same, think of diffrent cpu brands for example). 
Where as an interpreted language ( like python ) is converted to machine code at runtime by an interpreter 
for that specific machine.

Now you might wonder why not every language is an interpreted language. 
Well that is because converting the code to machine code at runtime takes a while, which makes the program a bit slower.
Where as the compiled code from an compiled language can be immediately executed by the cpu.

So why is it faster to use two different python programs that communicate over ZeroMQ.
Take the example code as in this repository.
Displaying a webcam stream using opencv uses some functions that take a while to complete (order of milliseconds).
Controlling the UR10 arm however uses some functions that take a lot longer to finish ( order of seconds, because the function 
completes when the UR10 has reached it's position ).
When you would try to display the webcam stream and move the arm at the same time in a single threaded program 
you will see that the webcam stream will hang when the robot arm is moving.
This is because the program can only do one task at a time. 

[the part below assumes the cpython interpreter is used, which is the most common interpreter]
[this is the interpreter you download when, downloading from https://www.python.org/]

Now some might say, well why won't you use multi-threading? 
multi-threading means that the computer executes multiple tasks in parallel (at the same time).
well now the robot arm and webcam stream wil move and display at the same time but not quite as fast as you would might expect.
This is because python can't really multi-thread. This is because threads in python use the same memory heap for every thread.
The problem that arises with this shared memory, is that every thread can read or write to the same memory location at the same time.
To overcome this problem python uses the so called Global intpreter lock (GIL). This GIL makes sure that only one thread at a time can
access the heap. The GIL does this by locking access, this prevents the other threads from operating.
This basically means that only work on one thread at a time.
But how does python execute two threads at the same time then? well it doesn't, what it actually does is switch very fast
between the different threads. Which makes it seem like the two threads run in parallel.

ok but what about the multiprocessing library?
when using the multiprocessing library, python creates a subprocess for each "thread".
Each subprocess has it's own memory space and runs on a separate core of the cpu. This bypass the GIL limitations.
So the threads run truely in parallel.

So why use ZeroMQ then?
by using the architecture as described in this repository you are actually doing the same as the multiprocessing library.
As there are two separate process with each their own memory space. 
What ZeroMQ does in this architecture is provide an easy way to communicate between these processes. 
Using ZeroMQ you can easily send all types of variables or when combining with google's protobuf entire class objects.
You are also able to run processes on different computers as you can send data easily over the network.
For example you can have an low power computer like an raspberry pi aquire data which it can then send to 
an more powerfull device which wil process the data.
It is also allows you to create all kinds of network topologies.

sources:
https://wiki.python.org/moin/GlobalInterpreterLock
https://realpython.com/python-gil/
https://www.vanguardsw.com/dphelp4/dph00296.htm
https://en.wikipedia.org/wiki/Global_interpreter_lock
https://indianpythonista.wordpress.com/2018/01/04/how-python-runs/
https://stackoverflow.com/questions/3265357/compiled-vs-interpreted-languages
https://blog.usejournal.com/multithreading-vs-multiprocessing-in-python-c7dc88b50b5b

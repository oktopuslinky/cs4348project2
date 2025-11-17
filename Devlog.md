# 11/16/2025 6:02 PM

I need to write a program that simulates a bank with 3 tellers and 50 customers. The bank opens when all 3 tellers are ready, and customers are able to make a withdrawal or deposit throughout the day. Only two tellers are able to go into the safe, which means that some process synchronization will be necessary. The bank will close (program termination) when all 50 customers have been served. Because there are quite a few moving parts, a precise level of coordination will be mecessary. This project seems like a large synchronization puzzle, which I will use threads in Python to solve. I am using Python because it is the language that I am most comfortable with. I will have to use semaphores for enforcing the limits on interacting with the bank door, safe, and manager. I will need a few functions for this program, which will be:
    - The thread for the teller
    - The thread for the customer
    - The main function which will control the thread management.
My first code commit will be creating the file and declaring the functions necessary to build.

# ll/16/2025 6:24 PM

SESSION START
During this session, I will be creating the file and declaring the functions. I will not write any of the logic inside of the functions yet, as that will be for future sessions. I will make sure to write what each function does as a docstring inside of it, that way I can easily come back and write the code in future sessions. This will help save time, as having a proper framework in advance eliminates issues with having to debug messy code due to poor planning. This will give me more time to clean up the code and make it more readable.

# 11/16/2025 7:06 PM

SESSION END
I was able to declare and describe the functions that I initially wanted to, in addition to adding some extra ones that will be useful for finishing the project. Those functions were print_line and monitor_customer_teller_completion. The first function was created as a helper function to easily display the log messages to the console. The other function was created to ensure the prevention of the deadlock situation of a teller being blocked on a semaphore despite the bank processing all customers. I will next work on developing the print_line function, as it is the easiest to implement and will get the project started.

# 11/16/2025 7:15 PM

SESSION START
For this session, I plan to write the print_line function. This should be simple, as I already have written the parameters and just need to output them in the correct format. One thing I will have to be careful about is that in the bracket, the bracket can either be empty if there is no interaction, or have the person that the thread interacted with, along with their id.

# 11/16/2025 7:29 PM
SESSION END
I was able to implement the print_line function, which will be responsible for printing the logs. I will be creating the global variables next, which will have the semaphores, synchronization structures, and necessary flags. I will decide which specific variables I want at the beginning of the next session.

# 11/16/2025 7:30 PM
SESSION START
I will be creating the global variables for this session. I will be making semaphores for the door, safe, manager, teller's customers, and the customer's state. I will also be declaring constants for the number of tellers and customers in order to minimize error. I will declare other variables as well that I deem necessary for the completion for the project.

# 11/16/2025 7:52 PM
SESSION END
I was able to add in all of the variables that I personally believe will be necessary as of right now. This may or may not change throughout the course of writing the program. There are some additional variables that I added as well. I made the line of customers a queue, as it is the perfect data structure for that. Also, I made the ready sellers a set, as it does not have any specific order. I wish to next work on developing the teller thread.

# 11/16/2025 7:54 PM
SESSION START
For this session, I will be implementing the logic written in the docstrings of the teller_thread. I will have to make sure that I am keeping correct track of the semaphores and all of the internal data within the function at all times, as this will ensure that the program continues to function correctly.

# 11/16/2025 8:38 PM
SESSION END
I was able to implement the logic for the teller_thread function. One issue that I ran into was ensuring that I am making the teller do all of the correct actions in the correct order, while making sure that the teller correctly waits on the right customer action. While I do not know at this moment if the logic that I programmed was completely correct (due to the customer_thread function not being programmed yet), I have a good starting point as of right now that I can build on if need be. In order to test the teller_thread function that I just made, I will next build the customer_thread function.

# 11/16/2025 9:00 PM
SESSION START
I aim to implement the customer_thread function according to the docstring planning that I already did. I will also make sure that the customer_thread function works with the teller_thread function without any issues. 

# 11/16/2025 9:16 PM
SESSION END
I have started working on the customer_thread function. I was not able to finish the entirety of the function during this session, but I was able to complete steps 1-4 from the customer sequence outlined on the project document. I will finish the rest of the steps of the sequence in the next session. So far, there have not been any challenges in implementing this function. However, it is possible that the rest of this function may be more difficult to write due to greater customer-teller process considerations.

# 11/16/2025 9:19 PM
SESSION START
In this session, my goal is to finish the customer_thread function and test it in the main function. I will need to use my understanding of threads and semaphores to be able to build this out.

# 11/16/2025 9:45 PM
SESSION END
I started the session by finishing up the rest of the steps for the customer_thread function. The logic for implementing the function itself was a little similar to that of the teller_thread function, since it directly works with it. Due to this, the customer_thread function was easier to implement than the previous one. However, while testing the functions, I stumbled upon an issue. I noticed that all of the tellers were not leaving the bank at the end of the day. I realized that the reason why this was happening was because some of the tellers were still blocked, meaning that they were not able to leave. In order to fix this, I wrote some code in the main function to wake any of the tellers that are still blocked, that way they can leave. This was a very important learning point for me during this project, because this reinforced the idea of frequent testing. Due to the testing, I was able to catch this error that I would have not seen if I had not done so. After I ran the tests, I realized that the code worked perfectly as it should for the output, and did not need the auxiliary thread I had suggested before. The error checking I implemented throughout the functions already took care of this deadlock situation. This means that I am now finished with the project. I learned a lot from this project, such as how to implement a solution for a deadlock situation and how to synchronize threads on this scale. It was very interesting to see how I was able to use the knowledge I learned in class to write a program that can simulate such a large amount of moving parts.

# 11/16/2025 10:16 PM
SESSION START
I forgot to add the readme file for the project, so I will add that during this session.

# 11/16/2025 10:22 PM
SESSION END
I have added the readme file for the project according to the instructions.
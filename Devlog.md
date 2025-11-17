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
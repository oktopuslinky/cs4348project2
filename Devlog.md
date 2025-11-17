# 11/16/2025 6:02 PM

I need to write a program that simulates a bank with 3 tellers and 50 customers. The bank opens when all 3 tellers are ready, and customers are able to make a withdrawal or deposit throughout the day. Only two tellers are able to go into the safe, which means that some process synchronization will be necessary. The bank will close (program termination) when all 50 customers have been served. Because there are quite a few moving parts, a precise level of coordination will be mecessary. This project seems like a large synchronization puzzle, which I will use threads in Python to solve. I am using Python because it is the language that I am most comfortable with. I will have to use semaphores for enforcing the limits on interacting with the bank door, safe, and manager. I will need a few functions for this program, which will be:
    - The thread for the teller
    - The thread for the customer
    - The main function which will control the thread management.
My first code commit will be creating the file and declaring the functions necessary to build.
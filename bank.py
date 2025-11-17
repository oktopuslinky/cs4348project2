import threading, random, time
from collections import deque

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

door_sem = threading.Semaphore(2)
safe_sem = threading.Semaphore(2)
manager_sem = threading.Semaphore(1)

lock = threading.Lock()

ready_tellers = set()
waiting_customers = deque()

teller_customer_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
waiting_flags = [False for _ in range(NUM_TELLERS)]

teller_selected_customer = [None for _ in range(NUM_TELLERS)]

# customer semaphores
customer_asked_sem = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
customer_done_sem = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
customer_left_sem = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]

teller_got_transaction_sem = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customer_ready_sem = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]

customer_transaction = [None for _ in range(NUM_CUSTOMERS)]

served_count = 0
served_count_lock = threading.Lock()
all_done_event = threading.Event()

def print_line(thread_type, tid_or_cid, bracket_type, bracket_id, msg):
    """
    Prints a formatted log line with the format:
    THREAD_TYPE ID [THREAD_TYPE ID]: MESSAGE
    """

    if bracket_type is None:
        bracket = "[]"
    else:
        bracket = f"[{bracket_type} {bracket_id}]"

    print(f"{thread_type} {tid_or_cid} {bracket}: {msg}")

def teller_thread(tid):
    """
    Simulates the behavior of a bank teller. Until all customers are served, the teller will repeatedly:
        - announce readiness to serve.
        - announce that the teller is waiting for a customer.
        - wait for an introduction handshake for the sake of synchronization.
        - ask for the transaction type (withdrawal or deposit) and wait for the response.
        - handles the deposit or withdrawal transaction
        - enter the safe
        - complete the transaction and wait for the customer to leave
    """
    global served_count
    while True:
        print_line("Teller", tid, None, None, "ready to serve")
        print_line("Teller", tid, None, None, "waiting for a customer")

        customer_to_serve = None
        with lock:
            # if waiting queue has customers, take one
            if waiting_customers:
                cust_id, cust_event = waiting_customers.popleft()
                teller_selected_customer[tid] = cust_id
                customer_to_serve = cust_id
                cust_event.set()
            else: # if no waiting customers, mark self as ready
                ready_tellers.add(tid)

        if customer_to_serve is None:
            with lock:
                waiting_flags[tid] = True
            teller_customer_sem[tid].acquire()
            with lock:
                waiting_flags[tid] = False
                customer_to_serve = teller_selected_customer[tid]

        # if all customers are served, break
        if customer_to_serve is None:
            if all_done_event.is_set():
                break
            else:
                continue

        cid = customer_to_serve
        customer_ready_sem[cid].acquire()

        print_line("Teller", tid, "Customer", cid, "serving a customer")
        print_line("Teller", tid, "Customer", cid, "asks for transaction")
        # signal customer to give transaction
        customer_asked_sem[cid].release()

        # wait until customer gives transaction
        teller_got_transaction_sem[tid].acquire()
        trans = customer_transaction[cid]

        if trans == "withdrawal":
            print_line("Teller", tid, "Customer", cid, "handling withdrawal transaction")
            print_line("Teller", tid, "Customer", cid, "going to the manager")
            print_line("Teller", tid, "Customer", cid, "getting manager's permission")

            # one teller for manager
            manager_sem.acquire()
            # simulate manager interaction, 5-30 ms
            ms = random.randint(5, 30)
            time.sleep(ms / 1000.0)
            manager_sem.release()

            print_line("Teller", tid, "Customer", cid, "got manager's permission")
        else:
            print_line("Teller", tid, "Customer", cid, "handling deposit transaction")

        print_line("Teller", tid, "Customer", cid, "going to safe")
        safe_sem.acquire()
        print_line("Teller", tid, "Customer", cid, "enter safe")

        # perform transaction, 10-50 ms
        ms = random.randint(10, 50)
        time.sleep(ms / 1000.0)

        print_line("Teller", tid, "Customer", cid, "leaving safe")
        # done with safe
        safe_sem.release()

        if trans == "withdrawal":
            print_line("Teller", tid, "Customer", cid, "finishes withdrawal transaction.")
        else:
            print_line("Teller", tid, "Customer", cid, "finishes deposit transaction.")

        # signal customer that transaction is done
        customer_done_sem[cid].release()

        print_line("Teller", tid, "Customer", cid, "wait for customer to leave.")

        customer_left_sem[cid].acquire()

        with lock:
            teller_selected_customer[tid] = None

        with served_count_lock:
            served_count += 1
            if served_count >= NUM_CUSTOMERS:
                all_done_event.set()

        # if all done, break
        if all_done_event.is_set():
            break

    print_line("Teller", tid, None, None, "leaving for the day")

def customer_thread(cid):
    """
    Simulates the behavior of a bank customer. Each customer will:
        - randomly choose to make a withdrawal or deposit.
        - wait for a short random time until arriving at the bank.
        - enter bank door, 2 at a time.
        - if there is a ready teller, select it. Otherwise, wait in line.
        - do a handshake with the teller
        - wait for teller to finish transaction
        - leave teller, go to door, and leave the bank.
    """
    pass

def monitor_customer_teller_completion():
    """
    Auxiliary thread that prevents a deadlock situation where the teller stays blocked on a semaphore even after
    all customers have been served.
    """
    pass

def main():
    random.seed()  # system time seed

    # Start teller threads
    tellers = []
    for t in range(NUM_TELLERS):
        th = threading.Thread(target=teller_thread, args=(t,), daemon=False)
        th.start()
        tellers.append(th)

if __name__ == "__main__":
    main()
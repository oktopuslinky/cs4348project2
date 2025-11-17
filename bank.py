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

    trans = random.choice(["deposit", "withdrawal"])
    customer_transaction[cid] = trans

    # wait between 0-100 ms
    ms = random.randint(0, 100)
    time.sleep(ms / 1000.0)

    # enter bank
    door_sem.acquire()
    print_line("Customer", cid, None, None, "going to bank.")
    print_line("Customer", cid, None, None, "entering bank.")
    print_line("Customer", cid, None, None, "getting in line.")

    assigned_teller = None
    assigned_event = threading.Event()

    with lock:
        # check if any ready teller exists
        if ready_tellers:
            # pick a random teller
            tid = ready_tellers.pop()
            teller_selected_customer[tid] = cid
            assigned_teller = tid
        else:
            # if no ready teller, put customer in waiting line
            waiting_customers.append((cid, assigned_event))

    if assigned_teller is None:
        assigned_event.wait()
        with lock:
            for t in range(NUM_TELLERS):
                if teller_selected_customer[t] == cid:
                    assigned_teller = t
                    # ensure it's not in ready_tellers set
                    ready_tellers.discard(t)
                    break

    print_line("Customer", cid, f"Teller", assigned_teller, "selecting a teller.")
    print_line("Customer", cid, f"Teller", assigned_teller, "selects teller")
    print_line("Customer", cid, f"Teller", assigned_teller, "introduces itself")

    # signal the teller that the customer is ready
    customer_ready_sem[cid].release()

    with lock:
        if waiting_flags[assigned_teller]:
            teller_customer_sem[assigned_teller].release()

    # wait for teller to ask for the transaction
    customer_asked_sem[cid].acquire()

    # tell the teller the transaction
    if trans == "withdrawal":
        print_line("Customer", cid, f"Teller", assigned_teller, "asks for withdrawal transaction")
    else:
        print_line("Customer", cid, f"Teller", assigned_teller, "asks for deposit transaction")

    customer_transaction[cid] = trans
    teller_got_transaction_sem[assigned_teller].release()

    # wait for teller to complete the transaction
    customer_done_sem[cid].acquire()

    # customer leaves the bank through the door
    print_line("Customer", cid, f"Teller", assigned_teller, "leaves teller")
    print_line("Customer", cid, None, None, "goes to door")
    print_line("Customer", cid, None, None, "leaves the bank")

    customer_left_sem[cid].release()
    door_sem.release()

def main():
    random.seed()  # system time seed

    # Start teller threads
    tellers = []
    for t in range(NUM_TELLERS):
        th = threading.Thread(target=teller_thread, args=(t,), daemon=False)
        th.start()
        tellers.append(th)

    customers = []
    for c in range(NUM_CUSTOMERS):
        th = threading.Thread(target=customer_thread, args=(c,), daemon=False)
        th.start()
        customers.append(th)

    for th in customers:
        th.join()

    all_done_event.set()

    # fix: wake any tellers still blocked
    for tid in range(NUM_TELLERS):
        try:
            teller_customer_sem[tid].release()
        except Exception:
            pass
    
    for th in tellers:
        th.join()

    print("The bank closes for the day.")

if __name__ == "__main__":
    main()
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
    pass

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
    pass

if __name__ == "__main__":
    main()
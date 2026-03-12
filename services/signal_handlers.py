import signal

running_flag = {"running": True}

def shutdown_handler(signum, frame):
    print(f"Signal {signum} reçu, arrêt du bot...", flush=True)
    running_flag["running"] = False

def register_shutdown_signals():
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
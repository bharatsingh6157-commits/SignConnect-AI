import psutil
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = p.info['cmdline']
        if cmd and 'streamlit_app.py' in ' '.join(cmd):
            print(f"Killing PID {p.info['pid']}")
            p.terminate()
    except:
        pass

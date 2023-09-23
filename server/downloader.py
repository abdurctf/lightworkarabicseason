import subprocess

def run_instaloader():
    cmd = ["python", "-m", "instaloader", "--login=lwas_2023", ":saved"]
    subprocess.run(cmd)

if __name__ == "__main__":
    run_instaloader()

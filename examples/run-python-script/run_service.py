"""Run a Python script using script name sent from client."""

import subprocess
import zampy


def callback(ch, method, properties, body):
    script = body.decode().strip()
    print(f"[*] Run python script {script}")
    subprocess.run(["python", script])
    print("[x] Done\n")


def main():
    """Run Python script."""
    service = zampy.Service()
    service.run_python_script(callback)


if __name__ == "__main__":
    main()

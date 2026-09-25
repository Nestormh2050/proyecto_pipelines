import subprocess
import sys

LIST_COMMAND = "dir" if sys.platform == "win32" else "ls -la"


def run(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred while running the command: {e}"


def main():
    print("Command output:\n", run(LIST_COMMAND))
    print("Output:", run("echo Hello, World!").strip())


if __name__ == "__main__":
    main()

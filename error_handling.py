import sys


# Fonction pure
def error_print(*args, exception: Exception = None, stop_script: bool = True, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print_help()  # Help is not printed in stderr by design. We don't want to pollute the error log

    if exception is not None:
        print("Oups! There was an unexpected error... Here's the traceback:", file=sys.stderr)
        raise exception

    if stop_script:
        sys.exit(1)


# Fonction pure
def print_help():
    print("----------------------------------------------")
    print("Usage examples:")
    print("main.py url https://spacejam.com")
    print("main.py url https://spacejam.com crawling false")
    print("main.py file ./tests/spacejam.html")
    print("main.py stdin html|filelist|urllist:")
    print("   echo [\\\"https://spacejam.com\\\"] | python main.py stdin urllist")
    print("   echo [\\\"./tests/spacejam.html\\\"] | python main.py stdin filelist")
    print("   python main.py stdin html < ./tests/spacejam.html")
    print("----------------------------------------------")
    print("Parameter details:")
    print("help -> shows this message")
    print("url -> string url")
    print("file -> string path to a file")
    print("stdin -> accepted values are:")
    print("   html -> will tell the program to expect html in the stdin")
    print("   filelist -> will tell the program expect a JSON array of file paths in the stdin")
    print("   urllist -> will tell the program expect a JSON array of urls in the stdin")
    print("!!!! NOTE: url, file, and stdin are mutually exclusive. You must only use one of them.")
    print(
        "crawling -> true (default) or false. (can be capitalized) To be used whenever the program reads URLs. It will be ignored otherwise.")
    print("----------------------------------------------")

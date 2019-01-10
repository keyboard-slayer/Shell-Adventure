import os
import sys


def launch(file: str):
    os.system(
            "/bin/bash -c 'chmod +x venv/bin/* && source venv/bin/activate && cd game/ && PYTHONPATH=\"{}\"" \
            " python -O {}'" .format(os.path.abspath("./"), os.path.abspath(f"./test/{file}")))


if __name__ == "__main__":
    header = "\n".join([files for files in os.listdir("./test/") \
                        if files != "__init__.py"])

    if sys.argv[1] == "--dev":
        print(f"""
*******************
*Fichier de tests *
*******************
{header}""")
        filename = input("Tappez le nom du fichier: ")
        launch(filename)

import pandas as pd

def compare_csv_files(file1 , file2):
    # Compare DataFrames
    if file1.equals(file2):
        return True
    else:
        # comp = file1.compare(file2)
        # print(f"-----------------Compare-------------------")
        # print(comp)
        return False
import numpy as np
import pandas as pd
import sys

#python read_file.py csv_file_path


def main():
	file_path = sys.argv[1]
	binary_vector = pd.read_csv(file_path,header=None,nrows=1).values.tolist()[0]
	df = pd.read_csv(file_path,skiprows=1,header=None)
	for i in range(len(binary_vector)):
		val = binary_vector[i]
		if val == 0:
			df = df.drop(i,axis=1)
	print(df)

if __name__ == "__main__":
	main()

import subprocess
import numpy as np
from os import listdir 

INPUT_PATH = './test_LPs/input/'
OUTPUT_PATH = './test_LPs/output/'

def evaluate_output(output, filename):

  with open('{}{}'.format(OUTPUT_PATH, filename)) as f:
    true_output = [line.split() for line in f.readlines()]
    true_status = true_output[0]

    lines = [line.split() for line in output.split('\n')[:-1]]
    predicted_status = lines[0]

    classification = predicted_status == true_status
    print("  Classification: ", classification)

    if len(true_output) > 1 and classification:
      true_values = [list(map(float, x)) for x in true_output[1:]]
      predicted_values = [list(map(float, x)) for x in lines[1:]]

      if len(lines) == 1:
        value, assigned = False, False
      else:
        value = np.isclose(predicted_values[0], true_values[0])[0]
        assigned = np.all(np.isclose(predicted_values[1], true_values[1]))

      print("  Optimal Value: ", value)
      print("  Assigned Values: ", assigned)

    else:
      value, assigned = True, True

    verdict = np.all([classification, value, assigned])
    print("%s Verdict: %s\n" % (("#", "Correct") if verdict else ("!", "Invalid")))

    return verdict

def main():
  input_files = listdir(INPUT_PATH)
  verdicts = []

  for file in input_files:
    print("File: ", file)
    try:
      output = subprocess.check_output(["python3", "main.py", "--file={}{}".format(INPUT_PATH, file)]).decode("utf-8")
      verdict = evaluate_output(output, file)
    except:
      print("--ERRORED OUT\n")
      verdict = False

    verdicts.append((verdict, file))

  total_fails = [file for verdict, file in verdicts if not verdict]

  print("Solver failed on these files:")
  print(total_fails)

  return -1

if __name__=="__main__":
  main()
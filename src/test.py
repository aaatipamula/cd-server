import subprocess as sp

run = sp.run(['docker', 'ps'], capture_output=True)

print(run.stderr.decode())
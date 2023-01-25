import re

def getTime(line: str) -> int:
    match = re.search(r'\d+(?:s \d+ms|ms)', line)

    if not match:
        return 0
    
    time = match.group()
    if 's ' in time:
        seconds, miliseconds = time.split('s ')
    else:
        seconds, miliseconds = 0, time
    
    seconds = int(seconds)
    miliseconds = int(miliseconds[:-2])

    return float(seconds * 1000 + miliseconds)

def getEnergy(line: str):
    total = line[line.find(':') + 1 : line.find('(')].strip()
    pairs = re.findall(r'(\w+)=(\d+\.\d+)', line)
    pairs = [*pairs, ('total', total)]

    return [(label, float(value)) for label, value in pairs]

def getCharge(line: str):
    start = line.find('charge=') + len('charge=')
    end = line[start:].find(' ')
    return float(line[start:start+end]) * 0.001
    

def getAppData(filename: str, id: str, log=True) -> dict:
    data = {}

    try:
        with open(filename, "r") as file:
            searchTime, searchCharge = False, True

            for line in file:

                if searchTime and "Total running:" in line:
                    data['time'] = getTime(line)
                    searchTime = False
                elif searchCharge and 'charge=' in line:
                    data['charge'] = getCharge(line)
                    searchCharge = False

                if id not in line:
                    continue
                
                # line contains the id
                line = line.strip()

                # if the id is at the start -> look for execution time
                if line.startswith(id):
                    searchTime = True
                # 
                elif line.startswith(f'Uid {id}'):
                    pairs = getEnergy(line)
                    data['energy'] = {label: value for label, value in pairs}
                    
                
    except IOError:
        if (log): print(f'Error: {filename} is missing')
    
    return data

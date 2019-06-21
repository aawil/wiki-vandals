import pandas as pd
import numpy as np
import requests
import sys

def get_damage_batch(session, rev_ids):
    rev_ids = [str(rev_id) for rev_id in rev_ids]
    rev_id_list = "|".join(rev_ids)
    
    url = "https://ores.wikimedia.org/v3/scores/enwiki/"
    model = "damaging"
    request = session.get(url+"?models="+model+"&revids="+rev_id_list)
    data = request.json()
    
    probs = []
    
    for rev_id in rev_ids:
        try:
            probs.append(data['enwiki']['scores'][rev_id][model]['score']['probability']['true'])
        except:
            probs.append(np.nan)
    
    return probs

changes = pd.read_csv('anon_changes_jun04.tsv', sep='\t')
changes = changes.query("rc_actor != 0.0")
revid_chunks = np.array_split(changes['rc_this_oldid'], len(changes)//50)

if __name__ == "__main__":
    session = requests.Session()
    for i in range(int(sys.argv[1]), int(sys.argv[2])):
        # if i % 100 == 0:
        print(f"getting chunk {i}...")
        damage_chunk = get_damage_batch(session, revid_chunks[i])
        pd.Series(damage_chunk).to_csv(f"./damage_chunks/damage_chunk_{i}.csv", header=False)
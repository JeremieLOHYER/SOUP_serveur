
import jellyfish

def compare(a: str, b: str):
    return jellyfish.jaro_similarity(a,b)

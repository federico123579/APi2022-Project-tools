#!/usr/bin/env python3

import sys
import math
import argparse
import random as rand

def clamp(a, b, c):
    return max(a, min(b, c))

def fold_clamp(a, b, c):
    if a <= b and b <= c:
        return b
    q = abs(b - a) // (c - a)
    r = abs(b - a) % (c - a)
    if q % 2 == 0:
        return r + a
    return c - r

def sign(a):
    return -1 if a < 0 else 1

levenshtein_memo = dict()

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if (s1, s2) in levenshtein_memo:
        return levenshtein_memo[(s1, s2)]
    
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    levenshtein_memo[(s1, s2)] = previous_row[-1]
    return previous_row[-1]


def random_word(args):
    return ''.join([args.alphabet[rand.randrange(0, len(args.alphabet))] for i in range(0, args.word_size)])

def random_word_not_in_dict(args, dict):
    w = random_word(args)
    while w in dict:
        w = random_word(args)
    return w


def word_generator(args):
    seed = random_word(args)
    yield seed
    while True:
        mode = rand.random()
        if mode > 0.2:
            chars_to_change = list(range(0, args.word_size))
            rand.shuffle(chars_to_change)
            f = rand.gauss(args.word_size*args.dict_rand, math.sqrt(args.word_size/4))
            char_count = fold_clamp(1, int(f), args.word_size-1)
            for i in chars_to_change[0:char_count]:
                a = seed[0:i]
                b = args.alphabet[rand.randrange(0, len(args.alphabet))]
                c = seed[i + 1:]
                seed = a + b + c
        else:
            ls = list(seed)
            rand.shuffle(ls)
            ''.join(ls)
        yield seed


def gen_insert(dict: set, args):
    num_words = rand.randrange(args.insert_min, args.insert_max)
    total = len(dict) + num_words
    gen = word_generator(args)
    print('+inserisci_inizio')
    new_words = []
    while len(dict) < total:
        w = next(gen)
        if w not in dict:
            new_words += [w]
            dict.add(w)
    rand.shuffle(new_words)
    for w in new_words:
        print(w)
    print('+inserisci_fine')


def gen_dict(args) -> set:
    print('Generazione dizionario...', end='', file=sys.stderr)
    sys.stderr.flush()

    gen = word_generator(args)
    res = {next(gen)}
    while len(res) != args.dict_size:
        res.add(next(gen))
        if len(res) % (args.dict_size // 100 + 1) == 0:
            print('\rGenerazione del dizionario...', len(res)*100//args.dict_size, '%', end='', file=sys.stderr)
            sys.stderr.flush()
    print('\rGenerazione del dizionario completa', file=sys.stderr)
    return res


def gen_game(dict: set, args):
    print('+nuova_partita')

    stupidity = args.stupidity
    if stupidity is None:
        stupidity = rand.random()
    p_error = 0.1
    c = rand.randrange(args.game_len_min, args.game_len_max)

    ldict = sorted(dict)
    ref = ldict[rand.randrange(0, len(ldict))]
    print(ref)
    print(c)

    ldict.sort(key=lambda v: levenshtein(ref, v))

    i = 0
    guesspos = rand.randrange(1, len(ldict))
    tried_words = set()
    while i < c:
        insertroll = rand.random()
        if insertroll < args.p_insert:
            prevg = ldict[int(guesspos)]
            gen_insert(dict, args)
            ldict = sorted(sorted(dict), key=lambda v: levenshtein(ref, v))
            guesspos = ldict.index(prevg)

        mode = rand.random()
        if mode < p_error:
            print(random_word_not_in_dict(args, dict))
            continue
        if mode - p_error < args.game_p_filter:
            print('+stampa_filtrate')
        
        g = ldict[int(guesspos)]
        if g not in tried_words:
            print(g)
            tried_words.add(g)
            if g == ref:
                break
            i += 1
        
        newpos = guesspos // 2
        stppos = rand.randint(0, len(ldict))
        guesspos = int(newpos * (1-stupidity) + stppos * stupidity)
        guesspos = clamp(0, guesspos, len(ldict)-1)


def main():
    default_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    ap = argparse.ArgumentParser(description='Generatore di soluzioni Prova Finale API 2022')
    ap.add_argument('-s', '--seed', dest='seed', type=int,
                    help="Seme da cui ricavare la partita")
    ap.add_argument('-a', '--alphabet', dest='alphabet', type=str, default=default_alphabet,
                    help="L'alfabeto da utilizzare (deve essere un sottoinsieme di quello di base)")
    ap.add_argument('-n', '--dict-size', dest='dict_size', type=int, default=50,
                    help='Numero di parole nel dizionario')
    ap.add_argument('-k', '--word-size', dest='word_size', type=int, default=5,
                    help='Lunghezza delle parole')
    ap.add_argument('-r', '--dict-rand', dest='dict_rand', type=float, default=0.2,
                    help='Frazione di caratteri cambiati a ogni passo durante la generazione del dizionario')
    ap.add_argument('-g', '--n-games', dest='games', type=int, default=5,
                    help='Numero di partite')
    ap.add_argument('-i', '--p-insert', dest='p_insert', type=float, default=0.1,
                    help='Probabilità di inserire comandi di inserimento')
    ap.add_argument('-j', '--insert-min', dest='insert_min', type=float, default=5,
                    help='Minimo numero di parole inseribili in un comando di inserimento')
    ap.add_argument('-J', '--insert-max', dest='insert_max', type=float, default=10,
                    help='Massimo numero di parole inseribili in un comando di inserimento')
    ap.add_argument('-e', '--game-p-inv', dest='game_p_inv', type=float, default=0.1,
                    help='Probabilità di inserire una parola invalida in una partita')
    ap.add_argument('-f', '--game-p-filter', dest='game_p_filter', type=float, default=0.1,
                    help='Probabilità di inserire una richiesta di stampa parole filtrate in una partita')
    ap.add_argument('-m', '--game-len-min', dest='game_len_min', type=int, default=7,
                    help='Lunghezza minima di una partita')
    ap.add_argument('-M', '--game-len-max', dest='game_len_max', type=int, default=20,
                    help='Lunghezza massima di una partita')
    ap.add_argument('-z', '--stupidity', dest='stupidity', type=float,
                    help='Livello di stupidità del giocatore simulato. Tende ad allungare le partite.')
    args = ap.parse_args()

    if any([c not in default_alphabet for c in args.alphabet]):
        print("errore: Caratteri non validi nell'alfabeto ridotto")
        exit(1)
    if len(args.alphabet)**args.word_size < args.dict_size:
        print('errore: Le parole sono troppo corte.')
        exit(1)
    if not (0 <= args.dict_rand and args.dict_rand <= 1):
        print('errore: Fattore aleatorio dizionario non tra 0 e 1')
        exit(1)
    if not (0 <= args.p_insert and args.p_insert <= 1):
        print('errore: Probabilità aggiunta inserimenti in partita non tra 0 e 1')
        exit(1)
    if not (0 <= args.game_p_inv and args.game_p_inv <= 1):
        print('errore: Probabilità inserimento parole invalide non tra 0 e 1')
        exit(1)
    if not (0 <= args.game_p_inv and args.game_p_filter <= 1):
        print('errore: Probabilità inserimento richiesta filtraggio non tra 0 e 1')
        exit(1)
    if args.game_p_inv + args.game_p_filter > 1:
        print('errore: La probabilità di evento eccezionale in partita è maggiore di 1')
        print('(Evento eccezionale: stampa filtrate o parola invalida)')
        exit(1)
    if args.stupidity is not None and not (0 <= args.stupidity and args.stupidity <= 1):
        print('errore: Fattore stupidità non tra 0 e 1')
        exit(1)

    if args.seed is None:
        seed = rand.randrange(2**32-1)
        rand.seed(seed)
        print('Seme =', seed, file=sys.stderr)
    else:
        rand.seed(int(args.seed))

    d = gen_dict(args)
    print(args.word_size)
    d_det = sorted(d)
    rand.shuffle(d_det)
    for w in d_det:
        print(w)
    for i in range(0, args.games):
        insertroll = rand.random()
        if insertroll < args.p_insert:
            gen_insert(d, args)
        print('\rGenerazione partite...', i+1, '/', args.games, end='', file=sys.stderr)
        sys.stderr.flush()
        gen_game(d, args)
    print('\rGenerazione partite completata', file=sys.stderr)


if __name__ == '__main__':
    main()

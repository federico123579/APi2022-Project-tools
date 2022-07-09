# Contenuti
- [installazione](#Installazione)
- [script & tools presenti](#Script)

# Installazione

## Requisiti:

- `Python` >= 3.6
- [Poetry](https://python-poetry.org/) (consigliato)
    - altrimenti `virtualenv`

## Virtualenv
Basterà trovarsi nella repository ed eseguire il comando di installazione, questo genererà un ambiente virtuale con virtualenv `.env` e poi attivarlo.

```
./install.sh
```

l'installazione è necessaria solo la prima volta o quando si scarica una nuova versione. L'attivazione invece è necessaria ad ogni avvio di shell.

```
. .env/bin/activate
```

## Poetry

Con `poetry` è semplicissimo, basterà installare i tool con il seguente (basta farlo solo la prima volta):

```
cd ./tools
poetry install
```

e poi attivare la shell all'interno dell'ambiente virtuale per avere a portata i comandi (questo si ripete ogni volta che avviate una shell per avere a portata i vostri comandi senza esplicitarne la posizione): 

```
poetry shell
```

# Script

Ci sono 4 script utili che possono aiutare durante la fase di testing dell'eseguibile:

- **gentest**: generazione casuale di test.
- **testall**: per testare l'eseguibile su ogni file di test presente in una directory e in tutte le sue sottodirectory.
- **testsingle**: per testare e visualizzare le differenze tra l'output generato dall'eseguibile e l'output corretto.
- **runtest**: test runner per salvare su file l'output dell'eseguibile per ogni file di test presente in un directory (*serve più a chi vuole caricare le proprie versioni di output corretto*).

## Gentest

Script solito già noto per la generazione dei test in modo casuale con scelta dei parametri.
Per avere informazioni sui suoi parametri:

```
gentest -h
```

## Testall

```
testall PATH_EXECUTABLE TEST_DIRECTORY_PATH 
```

Dove `PATH_EXECUTABLE` è il percorso dell'eseguibile e `TEST_DIRECTORY_PATH` è il percorso verso la directory contenente tutti i test, generalmente la cartella `tests` presente in questa repo.
Questo script controlla l'output dell'eseguibile e lo confronta con ogni output corretto (se presente) fornendone in sintesi la corrispondenza.

## Testsingle

```
testsingle PATH_EXECUTABLE TEST_INPUT_FILE TEST_CORRECT_OUTPUT_FILE
```
Dove `PATH_EXECUTABLE` è il percorso dell'eseguibile, `TEST_INPUT_FILE` è il file di ingresso su cui si vuole testare l'output (*generalmente li si trova nella cartella `tests` in questa repo*) e `TEST_CORRECT_OUTPUT_FILE` è il file contenente l'output corrett (*sempre presente nella cartella `tests`*).
Questo script si comporta similmente a diff, per ora, permette unicamente, come opzione extra, `-y` per un controllo side-by-side.

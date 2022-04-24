from pathlib import Path
import math
import heapq

class node:		# struttura che conterrà i nodi dell'albero di huffman
	def __init__(self, freq, car):
		self.left = None
		self.right = None
		self.freq = freq
		self.car=car
		self.cod=''

def shannonEntropy(occorrenze):		# calcolo l'entropia di shannon
	entr = 0
	
	for item in occorrenze:
		entr+=((occorrenze[item]/len(testo))*math.log(1/(occorrenze[item]/len(testo)), 2))
	
	print('L\'entropia di Shannon e\':', round(entr, 2))

def huffmanTree(occorrenze):
	nodes = []
	for item in occorrenze:
		nodes.append(node(occorrenze[item], item))		# creo un heap contenente un nodo per ogni carattere

	while len(nodes)>1:		# finchè nell'heap non rimane un solo nodo
		nodes = sorted(nodes, key=lambda elem: elem.freq)		# riordino l'heap
		left = nodes[0]
		right = nodes[1]		# prendo i primi due nodi con prob minore
		left.cod = 0 			# a quello di sinistra assegno codifica 0
		right.cod = 1 			# a quello di destra assegno codifica 1
		father = node(left.freq+right.freq, '$')			# creo il nodo padre che avrà come probabilità la somma delle probabilità dei figli
		father.left = left
		father.right = right		# gli assegno i figli
		del nodes[0]
		del nodes[0]		# elimino i nodi appena fusi
		nodes.append(father)		# aggiungo il nodo appena creato all'heap
	
	return nodes[0]		# ritorno l'unico elemento della lista che sara' la radice dell'albero di Huffman

def rewriteFile(root):
	f = open("Lorem ipsum.txt", "r")		# apro il file sorgente in lettura
	w = open("output.txt", "w")		# apro il file destinazione in scrittura

	for line in f:
		for ch in line:		# per ogni carattere del file sorgnete
			findCod(root, ch, w)		# cerco la sua codifica e la stampo nel file destinazione
	
	f.close()
	w.close()		# chiudo i file aperto

def findCod(node, ch, w, val=''):		# cerco la codifica del carattere e la stampo
	newVal = val + str(node.cod)		# ogni volta che scendo di un livello alla codifica viene aggiunto uno 0 o un 1
	if(node.left):
		findCod(node.left, ch, w, newVal)
	if(node.right):
		findCod(node.right, ch, w, newVal)
	# ho raggiunto una foglia dell'albero (solo le foglie ontengono delle codifiche)
	if(node.left==None and node.right==None and node.car == ch):		# se è la codifica del carattere che stavo cercando
		w.write(newVal)		# la stampo nel file destinazione
		codifica[node.car] = len(newVal)		# aggiungo al dizionario per ogni carattere la lunghezza della sua codifica

def lunghezzaAttesa():
	lungh=0
	for item in occorrenze:
		lungh+=occorrenze[item]/len(testo)*codifica[item]		# la lunghezza attesa calcolata come la sommatoria delle probabilità di ogni carattere * lunghezza della codifica
	return lungh

testo = Path('Lorem ipsum.txt').read_text()		# leggo il testo sotoforma di stringa
occorrenze = {}		# creo un dizionario

for x in range(0, 127):		# conto quante volte compare una lettera nel file
	if testo.count(chr(x)) != 0:
		occorrenze[chr(x)] = testo.count(chr(x))		# inserisco nel dizionario le lettere con il loro numero di occorrenze

occorrenze[' '] = testo.count(' ')		# inserisco anche lo spazio
occorrenze =dict(sorted(occorrenze.items(), key=lambda item: item[1], reverse=True))		# ordino il dizionario in base alle occorrenze

for item in occorrenze:
	print('Il carattere', item, 'compare', occorrenze[item], 'volte con una probabilita\' del:', round(occorrenze[item]/len(testo)*100, 2), '%')		# stampo quante volte comapre un carattere

codifica = {}		# dizionario che per ogni carattere contiene la lunghezza della sua codifica

shannonEntropy(occorrenze)
rewriteFile(huffmanTree(occorrenze))
risultato = Path('output.txt').read_text()		# leggo il testo in output sotoforma di stringa
print('La lunghezza attesa della codifica e\':', round(lunghezzaAttesa(), 2))
print('La lunghezza del file in input e\'', len(testo), 'byte, mentre la lunghezza del file compresso e\'', len(risultato)/8, 'byte')
print('La percentuale di compressione e\'', (len(risultato)/8)/len(testo)*100, '%')
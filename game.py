from copy import copy, deepcopy
import random
import pygame
import time
# Creo un tablero de 9x9. x cada casillero igual a 0, es decir, vacio, le asigno el menor numero del 1 al 9 que no 
# esté ni en su cuadricula de 3x3 ni en su fila ni columna. Y sigo x toda la fila. 
# Si en algun momento llego a un punto donde no puedo avanzar más, retrocedo.
# Como retrocedo? todos los valores que agregué tambien los almaceno en un struct donde pongo su fila y su columna en una pila.


white = (255,255,255)
black = (0,0,0)
green = (40,255,40)
red = (255,0,0)

(width, height) = (600, 470)
screen = pygame.display.set_mode((width, height))
background_colour = (25,25,55)
screen.fill(background_colour)

cell_size = 40

top_margin_board = 20
left_margin_board = 20

selected_cell = [-1,-1]

A = []
completed_board = []
row = 0
column = 0
filled_positions = []
#En filled positions va: las posiciones fila-columna YYY todos los valores que ya puse previamente ahí
#[Fila,Columna,[numeros ya usados]]

####PARTE DE DIBUJO
def set_board():
	pygame.draw.rect(screen,white,(left_margin_board,top_margin_board,360,360))



def set_board_lines():
	for row in range(0, 10):
		for column in range(0, 10):
			if(column in [0,3,6,9]):
				margin = 4
			else:
				margin = 1
			pygame.draw.line(screen, black, (left_margin_board + cell_size*column,top_margin_board), (left_margin_board + cell_size*column,top_margin_board + cell_size*9), margin)

			if(row in [0,3,6,9]):
				margin = 4
			else:
				margin = 1
			pygame.draw.line(screen, black, (left_margin_board,top_margin_board+ cell_size*row), (left_margin_board + cell_size*9,top_margin_board+ cell_size*row), margin)				


def set_play_button(width, height,text):
	x_position = left_margin_board + cell_size*4.5 - width/2
	y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,black,(x_position,y_position,width,height))

	width = 230
	height = 75
	small_x_position = left_margin_board + cell_size*4.5 - width/2
	small_y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,white,(small_x_position,small_y_position,width,height))

	pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
	myfont = pygame.font.SysFont('Comic Sans MS', 90)
	textsurface = myfont.render(text, False, (0, 0, 0))
	screen.blit(textsurface,(x_position*1.05,y_position*1.1))

	return x_position,y_position

def set_solve_button(width, height):
	x_position = left_margin_board + cell_size*9.5
	y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,black,(x_position,y_position,width,height))

	width = 150	
	height = 75
	small_x_position = left_margin_board + cell_size*9.75
	small_y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,white,(small_x_position,small_y_position,width,height))

	myfont = pygame.font.SysFont('Comic Sans MS', 60)
	textsurface = myfont.render('  SOLVE', False, (0, 0, 0))
	screen.blit(textsurface,(x_position,y_position*1.15))

	return x_position,y_position



def start_game():

	pygame.font.init()
	set_board();
	set_board_lines();
	width_play_button = 250
	height_play_button = 90
	button_x_position,button_y_position = set_play_button(width_play_button, height_play_button,'  PLAY');
	pygame.display.flip()
		


	running = True
	initialized_game = False
	while running:
	  for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	    	running = False
	    elif event.type == pygame.MOUSEBUTTONUP:
	    	pos = pygame.mouse.get_pos()
	    	if(button_x_position<pos[0]<button_x_position+width_play_button and button_y_position<pos[1]<button_y_position+height_play_button):
	    		running = False
	    		initialized_game = True

	return initialized_game


def set_dificulty_options(width, height):
	x_position = left_margin_board + cell_size*4.5 - width/2
	y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,black,(x_position,y_position,width,height))

	width = 230
	height = 75
	small_x_position = left_margin_board + cell_size*4.5 - width/2

	###########################################

	easy_y_position = top_margin_board + cell_size*2.5 - height/2
	pygame.draw.rect(screen,white,(small_x_position,easy_y_position,width,height))

	myfont = pygame.font.SysFont('Comic Sans MS', 90)
	textsurface = myfont.render('EASY', False, (0, 0, 0))
	screen.blit(textsurface,(small_x_position*1.05,easy_y_position*1.1))

	###########################################

	medium_y_position = top_margin_board + cell_size*4.5 - height/2
	pygame.draw.rect(screen,white,(small_x_position,medium_y_position,width,height))
	
	myfont = pygame.font.SysFont('Comic Sans MS', 80)
	textsurface = myfont.render('MEDIUM', False, (0, 0, 0))
	screen.blit(textsurface,(small_x_position*1.05,medium_y_position*1.05))

	###########################################

	hard_y_position = top_margin_board + cell_size*6.5 - height/2
	pygame.draw.rect(screen,white,(small_x_position,hard_y_position,width,height))

	myfont = pygame.font.SysFont('Comic Sans MS', 90)
	textsurface = myfont.render('  HARD', False, (0, 0, 0))
	screen.blit(textsurface,(small_x_position*1.05,hard_y_position*1.05))


	return x_position,easy_y_position, medium_y_position, hard_y_position


def select_dificulty():

	set_board();
	set_board_lines();
	width_options = 250
	height_options = 300
	button_x_position,easy_y_position, medium_y_position, hard_y_position = set_dificulty_options(width_options, height_options);
	pygame.display.flip()
	height_options = 90


	running = True
	dificulty = 0
	while running:
	  for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	    	running = False
	    elif event.type == pygame.MOUSEBUTTONUP:
	    	pos = pygame.mouse.get_pos()
	    	if(button_x_position<pos[0]<button_x_position+width_options):
	    		if(easy_y_position<pos[1]<easy_y_position+height_options):
	    			dificulty = 1
	    			running = False
	    		if(medium_y_position<pos[1]<medium_y_position+height_options):
	    			dificulty = 2
	    			running = False
	    		if(hard_y_position<pos[1]<hard_y_position+height_options):
	    			dificulty = 3
	    			running = False

	return dificulty

def show_number(row, column, number):
	text = str(number)
	myfont = pygame.font.SysFont('Comic Sans MS', 60)
	textsurface = myfont.render(text, False, (0, 0, 0))
	screen.blit(textsurface,(left_margin_board + cell_size*column + 8,top_margin_board + cell_size*row + 4))

def clear_cell(row,column):
	pygame.draw.rect(screen,white,(left_margin_board + 40*column + 4,top_margin_board + 40*row + 4,32,34))



def show_board(board):
	set_board();
	set_board_lines();
	for row in range(0,9):
		print(board[row])
		for column in range(0,9):
			if(board[row][column]!=0):
				show_number(row,column,board[row][column])
	pygame.display.flip()


def select_cell(column, row):
	global selected_cell

	if(selected_cell[0]!=-1): #Limpio la que selecciné previamente
		pygame.draw.rect(screen,white,(left_margin_board + cell_size*selected_cell[1]+1,top_margin_board + cell_size*selected_cell[0]+1,cell_size-1,cell_size-1))
		if(A[selected_cell[0]][selected_cell[1]]!=0):
			show_number(selected_cell[0],selected_cell[1], A[selected_cell[0]][selected_cell[1]])
		set_board_lines()
		pygame.display.flip()	

	row = int(row)
	column = int(column)
	selected_cell = [row,column]
	pygame.draw.rect(screen,green,(left_margin_board + cell_size*column+1,top_margin_board + cell_size*row+1,cell_size-1,cell_size-1))
	pygame.draw.rect(screen,white,(left_margin_board + cell_size*column+3,top_margin_board + cell_size*row+3,cell_size-5,cell_size-5))
	if(A[row][column]!=0):
		show_number(row, column, A[row][column])
	pygame.display.flip()

### SOLUCION GRAFICA


def write_number_on_board(number):
	clicked_row = selected_cell[0]
	clicked_column = selected_cell[1]
	if(A[clicked_row][clicked_column]==0):
		if(completed_board[clicked_row][clicked_column]==number):
			A[clicked_row][clicked_column] = number
			update_remaining_numbers(number)
			pygame.draw.rect(screen,green,(left_margin_board + cell_size*clicked_column+1,top_margin_board + cell_size*clicked_row+1,cell_size-1,cell_size-1))
			pygame.draw.rect(screen,white,(left_margin_board + cell_size*clicked_column+3,top_margin_board + cell_size*clicked_row+3,cell_size-5,cell_size-5))			
			show_number(clicked_row,clicked_column,number)
		else:
			pygame.draw.rect(screen,red,(left_margin_board + cell_size*clicked_column+1,top_margin_board + cell_size*clicked_row+1,cell_size-1,cell_size-1))
			pygame.draw.rect(screen,white,(left_margin_board + cell_size*clicked_column+3,top_margin_board + cell_size*clicked_row+3,cell_size-5,cell_size-5))			
			if(A[clicked_row][clicked_column]!=0):
				show_number(clicked_row, clicked_column, A[clicked_row][clicked_column])
	pygame.display.flip()
	

def fill_position(blocked_numbers,board):
	correctly_filled = False;
	if(board[row][column]!=0):
		correctly_filled = True
	else:
		posible_numbers = [1,2,3,4,5,6,7,8,9]
		numbers_already_in_use = []
		#Agrego los numeros que ya use en la fila
		for i in board[row]:
			if(i!=0 and i not in numbers_already_in_use):
				numbers_already_in_use.append(i)
		#Agrego los numeros que ya use en la columna
		for j in range(0,9):
			if(board[j][column]!=0 and board[j][column] not in numbers_already_in_use):
				numbers_already_in_use.append(board[j][column])
		#Agrego los numeros que ya use en la cuadricula de 3x3
		cell_row = (row//3)*3
		cell_column = (column//3)*3
		for i in range(cell_row,cell_row+3):
			for j in range(cell_column,cell_column+3):
				if(board[i][j]!=0 and board[i][j] not in numbers_already_in_use):
					numbers_already_in_use.append(board[i][j])

		# Remuevo de los posibles números a los que ya aparecieron en el bloque 3x3 o fila o columna
		for element in numbers_already_in_use:
		    if element in posible_numbers:
		        posible_numbers.remove(element)
 
		position_selected_number = 0
		#print("Mis numeros posibles son: ",posible_numbers, "correctly_filled: ",correctly_filled)
		while len(posible_numbers)>position_selected_number and not correctly_filled:
			#print("Entré, comparo: ",posible_numbers[position_selected_number], blocked_numbers)
			if(posible_numbers[position_selected_number]not in blocked_numbers):
				selected_number = posible_numbers[position_selected_number]
				blocked_numbers.append(selected_number)
				filled_positions.append([row,column,blocked_numbers])
				board[row][column] = posible_numbers[position_selected_number]
				correctly_filled = True
			position_selected_number+=1

	#print("correctly_filled: ",correctly_filled)
	return correctly_filled

#### PARTE DE SOLUCION
def backtrack():
	#print("backtrack")
	global row
	global column
	position_correctly_filled = False
	#print("filled_positions: ",filled_positions)
	while not position_correctly_filled:
		if(len(filled_positions)>0):
			last_position_added = filled_positions.pop()
			#print(last_position_added)
			row = last_position_added[0]
			column = last_position_added[1]
			last_tried_numbers = last_position_added[2]
			A[row][column]=0
			position_correctly_filled = fill_position(last_tried_numbers)
			#if position_correctly_filled:
			#	print("Si lo pude cambiar")
			#else:
			#	print("no lo pude cambiar")
		else:
			raise Exception("No puedo backtreackear mas") #No hay solucion
	

def fill_position(blocked_numbers):
	correctly_filled = False;
	if(A[row][column]!=0):
		correctly_filled = True
	else:
		posible_numbers = [1,2,3,4,5,6,7,8,9]
		numbers_already_in_use = []
		#Agrego los numeros que ya use en la fila
		for i in A[row]:
			if(i!=0 and i not in numbers_already_in_use):
				numbers_already_in_use.append(i)
		#Agrego los numeros que ya use en la columna
		for j in range(0,9):
			if(A[j][column]!=0 and A[j][column] not in numbers_already_in_use):
				numbers_already_in_use.append(A[j][column])
		#Agrego los numeros que ya use en la cuadricula de 3x3
		cell_row = (row//3)*3
		cell_column = (column//3)*3
		for i in range(cell_row,cell_row+3):
			for j in range(cell_column,cell_column+3):
				if(A[i][j]!=0 and A[i][j] not in numbers_already_in_use):
					numbers_already_in_use.append(A[i][j])

		# Remuevo de los posibles números a los que ya aparecieron en el bloque 3x3 o fila o columna
		for element in numbers_already_in_use:
		    if element in posible_numbers:
		        posible_numbers.remove(element)
 
		position_selected_number = 0
		#print("Mis numeros posibles son: ",posible_numbers, "correctly_filled: ",correctly_filled)
		while len(posible_numbers)>position_selected_number and not correctly_filled:
			#print("Entré, comparo: ",posible_numbers[position_selected_number], blocked_numbers)
			if(posible_numbers[position_selected_number]not in blocked_numbers):
				selected_number = posible_numbers[position_selected_number]
				blocked_numbers.append(selected_number)
				filled_positions.append([row,column,blocked_numbers])
				A[row][column] = posible_numbers[position_selected_number]
				correctly_filled = True
			position_selected_number+=1

	#print("correctly_filled: ",correctly_filled)
	return correctly_filled



def complete_sudoku():
	global row
	global column
	row = 0
	column = 0
	while row < 9:
		while column < 9:
			#input("Press Enter to continue...")
			#print(row,column,A[row][column])
			if(A[row][column]==0):
				position_correctly_filled = fill_position([])
				if(position_correctly_filled):
					#print("llené correctamente la posicion")
					column+=1
				else:
					backtrack()
			else:
				#print("La posicion ya estaba ocupada")
				column+=1

		row+=1
		column = 0


def init_empty_board():
	global A
	A = [[0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0,0],
		]

def create_board():
	try:
		cant_generated_numbers = 0
		for row in [0,1,2,3,8]:
			added_numbers = 0
			while(added_numbers<9):
				cant_generated_numbers +=1
				if(cant_generated_numbers>300):
					raise Exception("Estoy tratando de crear un tablero imposible")
				number_already_in_use = False
				new_number = random.randint(1,9)
				cell_row = (row//3)*3
				cell_column = (added_numbers//3)*3
				for i in range(cell_row,cell_row+3):
					for j in range(cell_column,cell_column+3):
						if(A[i][j]==new_number):
							number_already_in_use = True

				for i in range(0,9):
					if(new_number == A[i][added_numbers]):
						number_already_in_use = True


				if(new_number in A[row]):
					number_already_in_use = True

				if(not number_already_in_use):
					A[row][added_numbers] = new_number
					added_numbers+=1
	except:
		init_empty_board()
		create_board()
'''
Selected dificulty:
1:remuevo el 38% de los casilleros
2:remuevo el 54% de los casilleros
3:remuevo el 63% de los casilleros
'''
def adjust_board_to_dificulty(selected_dificulty): 
	#B = A #Copia de la matriz original
	global A
	global filled_positions
	#print("Mi tablero COMPLETO ES:")
	#print_board()
	B = deepcopy(A)
	chance_of_empty_cell = 0
	if selected_dificulty=="1":
		chance_of_empty_cell = 38
	elif selected_dificulty=="2":
		chance_of_empty_cell = 54
	else:
		chance_of_empty_cell = 63
	try:
		for i in range(0,9):
			for j in range(0,9):
				if(random.randint(1,100)<chance_of_empty_cell):
					A[i][j]=0
		playable_board = deepcopy(A)
		complete_sudoku() #completo la matriz
		global completed_board
		completed_board = deepcopy(A)
		backtrack() # Hago backtrack

		complete_sudoku() #Intento completarla devuelta con otra solucion, si tira error, hay solucion unica
		#Si estoy acá, NO hay solucion unica asique me armo otra.
		A = deepcopy(B) #Restauro A a la matriz completa y pruebo devuelta
		filled_positions = []
		adjust_board_to_dificulty(selected_dificulty)
		#print_board()
		#Ahora que la tengo, me aseguro de que se puede resolver solo una vez
	except:
		# Estoy acá xq la matriz tiene solucion unica.
		filled_positions = []
		A = deepcopy(playable_board)
		#print("Ya tengo una matriz de solucion unica! Es:")
		#print_board()
		#print("\n")

def pressed_number(text_number):
	pressed_number = False
	if(text_number == "1"):
		pressed_number = True
		write_number_on_board(1)
	elif(text_number == "2"):
		pressed_number = True
		write_number_on_board(2)
	elif(text_number == "3"):
		pressed_number = True
		write_number_on_board(3)
	elif(text_number == "4"):
		pressed_number = True
		write_number_on_board(4)
	elif(text_number == "5"):
		pressed_number = True
		write_number_on_board(5)
	elif(text_number == "6"):
		pressed_number = True
		write_number_on_board(6)
	elif(text_number == "7"):
		pressed_number = True
		write_number_on_board(7)
	elif(text_number == "8"):
		pressed_number = True
		write_number_on_board(8)
	elif(text_number == "9"):
		pressed_number = True
		write_number_on_board(9)
	return pressed_number

def pressed_arrow_key(pressed_key):
	global selected_cell
	row = selected_cell[0]
	column = selected_cell[1]
	if(selected_cell[0]!=-1): #Es decir, ya clickee alguna celda
		if pressed_key[pygame.K_UP]:
			if(row>0):
				row=row-1
		elif pressed_key[pygame.K_DOWN]:
			if(row<8):
				row=row+1
		elif pressed_key[pygame.K_RIGHT]:
			if(column<8):
				column=column+1
		elif pressed_key[pygame.K_LEFT]:
			if(column>0):
				column=column-1

	select_cell(column,row)


def show_backtrack():
	global row
	global column
	global A
	position_correctly_filled = False
	#print("filled_positions: ",filled_positions)
	while not position_correctly_filled:
		if(len(filled_positions)>0):
			last_position_added = filled_positions.pop()
			#print(last_position_added)
			row = last_position_added[0]
			column = last_position_added[1]
			clear_cell(row,column)
			time.sleep(0.01)
			pygame.display.flip()
			last_tried_numbers = last_position_added[2]
			A[row][column]=0
			position_correctly_filled = fill_position(last_tried_numbers)
		else:
			raise Exception("No puedo backtreackear mas") #No hay solucion
	show_number(row,column, A[row][column])

def show_resolution():
	global row
	global column
	global A
	row = 0
	column = 0
	while row < 9:
		while column < 9:
			#input("Press Enter to continue...")
			#print(row,column,A[row][column])
			time.sleep(0.01)
			if(A[row][column]==0):
				position_correctly_filled = fill_position([])
				pygame.display.flip()
				if(position_correctly_filled):
					#print("llené correctamente la posicion")
					show_number(row,column,A[row][column])
					column+=1
				else:
					show_backtrack()
			else:
				#print("La posicion ya estaba ocupada")
				column+=1

		row+=1
		column = 0
	pygame.display.flip()

def play():
	width_solve_button = 170
	height_solve_button = 90
	button_x_position,button_y_position =set_solve_button(width_solve_button,height_solve_button)
	pygame.display.flip()


	running = True
	solved = False
	while running:
	  for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	    	running = False
	    elif event.type == pygame.MOUSEBUTTONUP:
	    	pos = pygame.mouse.get_pos()
	    	if(button_x_position<pos[0]<button_x_position+width_solve_button and button_y_position<pos[1]<button_y_position+height_solve_button):
	    		show_resolution()
	    		running = False
	    		solved = True
	    	if(left_margin_board<pos[0]<left_margin_board + 9*cell_size and top_margin_board<pos[1]<top_margin_board + 9*cell_size):
	    		select_cell((pos[0]-left_margin_board)/cell_size ,(pos[1]-top_margin_board)/cell_size)
	    #elif event.type == pygame.KEYDOWN:
	    #	write_number_on_board(pygame.key.name(event.key))
	    elif event.type == pygame.KEYDOWN:
	    	if(not pressed_number(pygame.key.name(event.key))):
	    		pressed_arrow_key(pygame.key.get_pressed())

	if(solved): #Es decir, me sali del otro loop xq terminé, y no xq clickee para salirme
		width_replay_button = 250
		height_replay_button = 90
		button_x_position,button_y_position = set_play_button(width_replay_button, height_replay_button,'REPLAY');
		pygame.display.flip()
		running = True
		replay = False
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if(button_x_position<pos[0]<button_x_position+width_replay_button and button_y_position<pos[1]<button_y_position+height_replay_button):
						running = False
						replay = True

		if(replay):
			game_admin()


remaining_numbers ={}

def update_remaining_numbers(number):
	global remaining_numbers
	remaining_numbers[number] = remaining_numbers[number] - 1

	pygame.draw.rect(screen,black,(left_margin_board-5,cell_size*10.5-5,cell_size*9+10,cell_size+10))
	pygame.draw.rect(screen,white,(left_margin_board,cell_size*10.5,cell_size*9,cell_size))

	for i in range(1,10):
		if(remaining_numbers[i]>0):
			show_number(10, i-1, i)


def init_remaining_numbers():
	global remaining_numbers
	for i in range(1,10):
		remaining_numbers[i]=9

	for row in A:
		for number in row:
			if(number!=0):
				update_remaining_numbers(number)	

def game_admin():
	init_empty_board()
	create_board()
	complete_sudoku()
	selected_dificulty = select_dificulty() #0: me salí, 1: easy, 2: medium, 3: hard
	if(selected_dificulty!=0):
		adjust_board_to_dificulty(selected_dificulty)
		init_remaining_numbers();
		show_board(A)
		play()

if(start_game() == True):
	game_admin()
import curses
import numpy as np

def shift_row_left(row):
    ans = np.zeros(4)
    trimmed_row = np.delete(row,np.argwhere(row==0))
    ans[:trimmed_row.size] = trimmed_row
    return ans
    
def combine_row_left(row):
    ans = np.zeros(4)
    shifted_row = shift_row_left(row)
    for i in range(3): 
        if shifted_row[i] == 0:
            break
        if shifted_row[i] == shifted_row[i+1]:
            shifted_row[i] = shifted_row[i] + 1
            shifted_row = np.delete(shifted_row, i+1)
            break
    ans[:shifted_row.size] = shifted_row
    return ans

def combine_matrix_left(matrix):
    return np.apply_along_axis(combine_row_left, 1, matrix)

def combine_matrix_up(matrix):
    ans = np.rot90(matrix)
    ans = combine_matrix_left(ans)
    ans = np.rot90(ans)
    ans = np.rot90(ans)
    ans = np.rot90(ans)
    return ans

def combine_matrix_right(matrix):
    ans = np.rot90(matrix)
    ans = np.rot90(ans)
    ans = combine_matrix_left(ans)
    ans = np.rot90(ans)
    ans = np.rot90(ans)
    return ans

def combine_matrix_down(matrix):
    ans = np.rot90(matrix)
    ans = np.rot90(ans)
    ans = np.rot90(ans)
    ans = combine_matrix_left(ans)
    ans = np.rot90(ans)
    return ans

def check_lose(matrix):
    if matrix[matrix>0].size == 0:
        return True
    return False

def check_win(matrix):
    if matrix[matrix>10].size > 0:
        return True
    return False

def insert_number(matrix):
    indices = np.where(matrix == 0)
    ans = matrix
    if(indices[0].size > 0):
        choice = np.random.randint(indices[0].size)
        ans[indices[0][choice]][indices[1][choice]] =  np.random.choice([1,2],1,p=[0.8, 0.2])
    return ans


def draw_menu(stdscr):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK,curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK,curses.COLOR_YELLOW )
    curses.init_pair(4, curses.COLOR_BLACK,curses.COLOR_MAGENTA )
    curses.init_pair(5, curses.COLOR_BLACK,curses.COLOR_CYAN )
    curses.init_pair(6, curses.COLOR_BLACK,curses.COLOR_RED )
    curses.init_pair(7, curses.COLOR_MAGENTA,curses.COLOR_CYAN )
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_MAGENTA)
    curses.init_pair(9, curses.COLOR_GREEN,curses.COLOR_YELLOW )
    curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_RED)
    curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

    player_array = np.zeros((4,4))
    player_array = insert_number(player_array)
    player_array = insert_number(player_array)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()

        temp_mat = player_array
        if k == curses.KEY_DOWN:
            temp_mat = combine_matrix_down(player_array)
        elif k == curses.KEY_UP:
            temp_mat = combine_matrix_up(player_array)
        elif k == curses.KEY_RIGHT:
            temp_mat = combine_matrix_right(player_array)
        elif k == curses.KEY_LEFT:
            temp_mat = combine_matrix_left(player_array)

        if (not np.array_equal(temp_mat, player_array)):
            player_array = insert_number(temp_mat)

        for i in range(4):
            for j in range(4):
                stdscr.attron(curses.color_pair(1+int(player_array[i][j])))
                stdscr.addch(int(i+1), int(j+1), chr(int(64+player_array[i][j])))
                stdscr.attroff(curses.color_pair(1+int(player_array[i][j])))

        if(check_win(player_array) or check_lose(player_array)):
            break

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
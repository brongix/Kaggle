def my_agent_test(obs, config):
    
    ################################
    # Imports and helper functions #
    ################################
    
    import numpy as np
    import random

    # Gets board at next step if agent drops piece in selected column
    def drop_piece(grid, col, piece, config):
        next_grid = grid.copy()
        for row in range(config.rows-1, -1, -1):
            if next_grid[row][col] == 0:
                break
        next_grid[row][col] = piece
        return next_grid

    # Returns True if dropping piece in column results in game win
    def check_winning_move(obs, config, col, piece):
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        next_grid = drop_piece(grid, col, piece, config)
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[row,col:col+config.inarow])
                if window.count(piece) == config.inarow:
                    return True
        # vertical
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns):
                window = list(next_grid[row:row+config.inarow,col])
                if window.count(piece) == config.inarow:
                    return True
        # positive diagonal
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        # negative diagonal
        for row in range(config.inarow-1, config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        return False
    
    def check_winning_move_on_grid(grid, config, col, piece):
        
        next_grid = drop_piece(grid, col, piece, config)
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[row,col:col+config.inarow])
                if window.count(piece) == config.inarow:
                    return True
        # vertical
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns):
                window = list(next_grid[row:row+config.inarow,col])
                if window.count(piece) == config.inarow:
                    return True
        # positive diagonal
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        # negative diagonal
        for row in range(config.inarow-1, config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        return False
    
    
    # Returns True if dropping piece in column results in opportunity
    def check_opportunity_move(obs, config, col, piece):
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        next_grid = drop_piece(grid, col, piece, config)
        
        valid_moves = [col for col in range(config.columns) if next_grid[0][col] == 0]
        
        #check how many winning moves
        opp = 0
        for move in valid_moves:
            if check_winning_move_on_grid(next_grid, config, move, piece):
                opp += 1
            if opp >= 2:
                return True
        
        return False
    
    #########################
    # Agent makes selection #
    #########################
    
    
    #Level 0 - valid moves
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    
    #Level 1A - winning move
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark):
            return col
    
    #Level 1D - blocking winning move
    opp = obs.mark % 2 + 1
    for move in valid_moves:
        if check_winning_move(obs, config, move, opp):
            return move
        
    #Level 2A - opportunity move    
    for move in valid_moves:
        if check_opportunity_move(obs, config, move, obs.mark):
            return move
        
    #Level 2D - blocking opportunity move
    for move in valid_moves:
        if check_opportunity_move(obs, config, move, opp):
            return move
        
    return random.choice(valid_moves)

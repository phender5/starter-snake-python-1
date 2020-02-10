import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return '''
    This is worm yes!
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    #data['headType'] = 'bwc-earmuffs'
    #data['tailType'] = 'bwc-ice-skate'
    #data['color'] = '#add8e6'
    color = "#add8e6"
    return start_response(color)



@bottle.post('/move')
def move():
    data = bottle.request.json
    print(json.dumps(data))

    directions = ['up', 'down', 'left', 'right']
    value = data['turn'] % 12
    health = data['you']['health']
    food = data['board']['food'][0]
    height = data['board']['height']
    width = data['board']['width']
    head = data['you']['body'][0]
    avoid = []
    num_snakes = len(data['board']['snakes'])

    # appends the coordinates of the snakes to an array of coordinates to avoid
    for i in range(num_snakes):
        for j in range(len(data['board']['snakes'][i]['body'])):
            string = '(' + str(data['board']['snakes'][i]['body'][j]['x']) + "," + str(data['board']['snakes'][i]['body'][j]['y']) + ")"
            avoid.append(string)
        

    # appends the coordinates of the borders to the array of coordinates to avoid
    for i in range(height):
        string = "(" + '-1' + ',' + str(i) + ")"
        avoid.append(string)
        string = "(" + str(width) + ',' + str(i) + ")"
        avoid.append(string)
    for i in range(width):
        string = "(" + str(i) + ',' + '-1' + ")"
        avoid.append(string)
        string = "(" + str(i) + ',' + str(height) + ")"
        avoid.append(string)
    
    direction = random.choice(directions)
    # Finds food based on the first element in "food"
    # Goes left/right until the x matches, then goes up/down
    if health < 50:
        if food['x'] < head['x']:
            direction = 'left'
            print("err: 1")
        elif food['x'] > head['x']:
            direction = 'right'
            print("err: 2")
        elif food['x'] == head['x']:
            if food['y'] < head['y']:
                direction = "up"
                print("err: 3")
            elif food['y'] > head['y']:
                direction = 'down'
                print("err: 4")
    elif value == 0 or value == 1 or value == 2:
        direction = 'up'
        print("err: 6")
    elif value == 4 or value == 5 or value == 3:
        direction = 'right'
        print("err: 7")
    elif value == 7 or value == 8 or value == 6:
        direction = 'down'
        print("err: 8")
    elif value == 10 or value == 11 or value == 9:
        direction = 'left' 
        print("err: 9")


    if direction == 'left':
        coord = "(" + str(head['x']-1) + ',' + str(head['y']) + ")"
    elif direction == 'right':
        coord = "(" + str(head['x']+1) + ',' + str(head['y']) + ")"
    elif direction == 'up':
        coord = "(" + str(head['x']) + ',' + str(head['y']-1) + ")"
    else:
        coord = "(" + str(head['x']) + ',' + str(head['y']+1) + ")"

    if coord in avoid:
        print("err: 10")
        direction = 'up'
        coord = "(" + str(head['x']) + ',' + str(head['y']-1) + ")"
        if coord in avoid:
            print("err: 11")
            direction = 'down'
            coord = "(" + str(head['x']) + ',' + str(head['y']+1) + ")"
            if coord in avoid:
                print("err: 12")
                direction = 'right'
                coord = "(" + str(head['x']+1) + ',' + str(head['y']) + ")"
                if coord in avoid:
                    print("err: 13")
                    direction = 'left'
                    

    print(avoid)
    print(coord)
    print(direction)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )

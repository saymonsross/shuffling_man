init python:
    from copy import deepcopy
    
    class pipe_handler:
        def __init__(self, map, wh):
            self.init_map = deepcopy(map)
            self.map = deepcopy(self.init_map)
            self.wh = wh
            self.shuffle()
        def shuffle(self):
            for ii in self.map:
                for i in ii:
                    i[1] = (renpy.random.randint(1,4))

        def rotate(self, ii, i):
            if self.map[ii][i][1] < 4:
                self.map[ii][i][1] += 1
            else:
                self.map[ii][i][1] = 1
        def sum(self, m):
            r = ""
            for ii in m:
                for i in ii:
                    if i[0] in [0,4]:
                        pass
                    elif i[0] == 1:
                        if i[1] in [1,3]:
                            r = r + "1"
                        if i[1] in [2,4]:
                            r = r + "2"
                    else:
                        r = r + str(i[1])
            return r

    def pipe_reset(trans, st, at):
        if trans.rotate == 360:
            trans.rotate = 0
            return None

    class pipe_maker_handler: # --------------------------- Pipe maker
        def __init__(self, map, wh):
            self.map = map
            self.wh = wh

        def rotate(self, ii, i):
            if self.map[ii][i][0] < 7:
                self.map[ii][i][0] += 1
            else:
                self.map[ii][i][0] = 0
        def change(self, ii, i):
            if self.map[ii][i][1] < 4:
                self.map[ii][i][1] += 1
            else:
                self.map[ii][i][1] = 1
        def add_row(self):
            r = []
            for i in self.map[0]:
                r.append([0,4])
            self.map.append(r)
        def add_column(self):
            for ii,i in enumerate(self.map):
                self.map[ii].append([0,4])
        def copy(self):
            t = "    [\n"
            for nn, ii in enumerate(self.map):
                if nn:
                    t = t + "\n"
                t = t + ("        [ ")
                for n, i in enumerate(ii):
                    if n:
                        t = t + ", "
                    t = t + ("[{},{}]".format(i[0], i[1]))
                t = t + (" ],")
            t = t + "\n    ],"
            clip_put(t)
            # return t

screen pipes(g = pipes_map_1):
    modal True

    vbox:
        spacing 0
        for nn,ii in enumerate(g.map):
            hbox:
                spacing 0
                for n,i in enumerate(ii):
                    button:
                        padding 0,0 xsize g.wh ysize g.wh
                        add pipes_list[i[0]]
                        action Function(g.rotate, nn, n)
                        at pipes_rotate(i[1]*90)
    # frame:
    #     xalign .0
    #     has vbox
    #     text g.sum(g.init_map)
    #     text g.sum(g.map)
    default remains = 5
    if g.sum(g.init_map) == g.sum(g.map):
        timer 1 repeat True action SetScreenVariable("remains", remains - 1)
        if remains < 1:
            timer .1 action Return()
        frame:
            text "The water is flowing, let's proceed to the next place... in {}".format(remains)


default pipes_map_create = pipe_maker_handler(
    [
        [ [0,4], [0,4] ],
    ],
    256,
)
screen pipes_maker(g = pipes_map_create):
    modal True
    vbox:
        spacing 0
        for nn,ii in enumerate(g.map):
            hbox:
                spacing 0
                for n,i in enumerate(ii):
                    button:
                        padding 0,0 xsize g.wh ysize g.wh
                        button:
                            align 1.0,1.0
                            text "change"
                            action Function(g.rotate, nn, n)
                        add pipes_list[i[0]]
                        action Function(g.change, nn, n)
                        at pipes_rotate(i[1]*90)

    button:
        xalign 0.0
        text "Add row"
        action Function(g.add_row)
    button:
        yalign 0.0
        text "Add column"
        action Function(g.add_column)
    button:
        align 0.0,0.0
        text "Copy"
        action Function(g.copy)
        # text g.copy()

transform pipes_rotate(r):
    rotate_pad False
    ease .2 rotate r
    function pipe_reset



# -------------------- pipes image list
default pipes_list = [None,
    "pipes/straight.png",
    "pipes/bend.png",
    "pipes/t.png",
    "pipes/cross.png",
    "pipes/cap.png",
    "pipes/ground.png",
    "pipes/sink.png",
]

# -------------------- levels
default pipes_map_1 = pipe_handler(
    [
        [ [6,4], [1,4], [7,4] ],
    ],
    256
)
default pipes_map_2 = pipe_handler(
    [
        [ [0,4], [5,1], [7,3] ],
        [ [6,4], [3,4], [2,1] ],
    ],
    256
)
default pipes_map_3 = pipe_handler(
    [
        [ [7,2], [2,4], [7,3] ],
        [ [7,2], [4,4], [2,1] ],
        [ [6,4], [3,4], [6,2] ],
    ],
    256
)
default pipes_map_4 = pipe_handler(
    [
        [ [2,3], [1,4], [2,4] ],
        [ [2,2], [7,4], [1,1] ],
        [ [0,4], [6,4], [2,1] ],
    ],
    256
)
default pipes_map_5 = pipe_handler(
    [
        [ [7,3], [5,4], [2,4], [0,4] ],
        [ [2,2], [3,2], [4,1], [2,4] ],
        [ [0,4], [6,3], [5,3], [7,1] ],
    ],
    256
)
default pipes_map_6 = pipe_handler(
    [
        [ [7,3], [5,4], [3,2], [1,2], [3,2], [3,2], [7,4] ],
        [ [3,1], [3,2], [4,1], [6,2], [6,3], [2,2], [7,4] ],
        [ [5,3], [6,3], [3,1], [3,2], [3,2], [2,4], [0,4] ],
        [ [7,2], [6,2], [6,3], [5,3], [6,3], [6,3], [0,4] ],
    ],
    256
)


label pipes_game_chain:
    window hide
    show screen pipes(pipes_map_1)
    pause
    hide screen pipes
    show screen pipes(pipes_map_2)
    pause
    hide screen pipes
    show screen pipes(pipes_map_3)
    pause
    hide screen pipes
    show screen pipes(pipes_map_4)
    pause
    hide screen pipes
    show screen pipes(pipes_map_5)
    pause
    hide screen pipes
    show screen pipes(pipes_map_6)
    pause
    hide screen pipes


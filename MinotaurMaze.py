import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import math
import binascii
import pickle
import threading
import random


# Constants:
TILE_SIZE = 64
TILE_NAMES = [
    "images/Tiles/Tile00.ppm",
    "images/Tiles/Tile01.ppm",
    "images/Tiles/Tile02.ppm",
    "images/Tiles/Tile03.ppm",
    "images/Tiles/Tile04.ppm",
    "images/Tiles/Tile05.ppm",
    "images/Tiles/Tile06.ppm",
    "images/Tiles/Tile07.ppm",
    "images/Tiles/Tile08.ppm",
    "images/Tiles/Tile09.ppm",
    "images/Tiles/Tile10.ppm",
    "images/Tiles/Tile11.ppm",
    "images/Tiles/Tile12.ppm",
    "images/Tiles/Tile13.ppm",
    "images/Tiles/Tile14.ppm",
    "images/Tiles/Tile15.ppm",
    "images/Tiles/Tile16.ppm",
    "images/Tiles/Tile17.ppm",
    "images/Tiles/Tile18.ppm",
    "images/Tiles/Tile19.ppm",
    "images/Tiles/Tile20.ppm",
    "images/Tiles/Tile21.ppm",
    "images/Tiles/Tile22.ppm",
    "images/Tiles/Tile23.ppm",
    "images/Tiles/Tile24.ppm",
    "images/Tiles/Tile25.ppm",
    "images/Tiles/Tile26.ppm",
    "images/Tiles/Tile27.ppm",
    "images/Tiles/Tile28.ppm",
    "images/Tiles/Tile29.ppm"
]
PLAYER_SPRITES = [
    "images/Player.png"
]
MINOTAUR_SPRITES = [
    "images/Minotaur.png"
]
OVERLAY_IMAGE = "images/Visibility.png"
BOSS_IMAGES = [
    "images/BossKeys/BossKey0.ppm",
    "images/BossKeys/BossKey1.ppm",
    "images/BossKeys/BossKey2.ppm",
    "images/BossKeys/BossKey3.ppm",
    "images/BossKeys/BossKey4.ppm",
    "images/BossKeys/BossKey5.ppm",
    "images/BossKeys/BossKey6.ppm",
    "images/BossKeys/BossKey7.ppm",
    "images/BossKeys/BossKey8.ppm",
    "images/BossKeys/BossKey9.ppm"
]
QUIT = "images/Quit.png"
SAVE_AND_QUIT = "images/SaveAndQuit.png"
CONGRATULATIONS = "images/Congratulations.png"
MIN_DOCS_PER_LEVEL = 3
MAX_DOCS_PER_LEVEL = 5

# Global variables:
state = 0
progress = 0


# External functions:
def PythagoreanTheorem(a, b):
    """Returns the square root of a^2 + b^2.

    :param a: numerical
    :param b: numerical
    :return: float
    """
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))


def GetSeed(length=8):
    """Returns a seed of length 'length'.

    :param length: int
    :return: int
    """
    return random.randint(0, int(math.pow(10, length)))


def To_b32(integer):
    to_b32 = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
        16: "G",
        17: "H",
        18: "I",
        19: "J",
        20: "K",
        21: "L",
        22: "M",
        23: "N",
        24: "O",
        25: "P",
        26: "Q",
        27: "R",
        28: "S",
        29: "T",
        30: "U",
        31: "V"
    }
    return to_b32[integer]


def From_b32(b32):
    from_b32 = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "O": 24,
        "P": 25,
        "Q": 26,
        "R": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31
    }
    return from_b32[str(b32)]


def BinaryString(number, length):
    return ("{0:0" + str(length) + "b}").format(number)


def SaveMapInstance(map_data, filename, data_to_save):
    SaveTileMap(map_data, filename)

    with open(filename, "wb") as f:
        pickle.dump(data_to_save, f)


def LoadMapInstance(filename):
    map_data = LoadTileMap(filename)
    with open(filename, "rb") as f:
        loaded_data = pickle.load(f)

    return map_data, loaded_data


def SaveTileMap(map_data, filename):
    levels = map_data.levels
    width = map_data.width
    height = map_data.height
    maps = map_data.maps
    ladders = map_data.ladders
    map_graph = map_data.map_graph
    documents = map_data.documents
    start = map_data.start
    end = map_data.end

    decoded = ""

    for level in range(levels):
        for y in range(height):
            for x in range(width):
                decoded += To_b32(maps[level][y][x])
        decoded += To_b32(31)

    encoded = RunLengthEncode(decoded)

    components = int(math.ceil(len(encoded) / 16))
    desired_length = components * 16

    while len(encoded) < desired_length:
        encoded += To_b32(31)  # 31 means a new level, so will be removed when read from a file.

    binary_string = ""
    for value in encoded:
        binary_string += BinaryString(From_b32(value), 5)

    n = int("0b" + binary_string, 2)
    map_data = binascii.unhexlify('%x' % n)

    graphs = map_graph.AsArray()

    with open(filename + ".tilemap", "wb") as f:
        pickle.dump(levels, f)
        pickle.dump(width, f)
        pickle.dump(height, f)
        pickle.dump(ladders, f)
        pickle.dump(map_data, f)
        pickle.dump(graphs, f)  # Didn't have enough time to encrypt this. Could have also gotten it from map_data
        pickle.dump(documents, f)  # on load, but would take too long at this point. Will probably do it in version 2.
        pickle.dump(start, f)
        pickle.dump(end, f)


def LoadTileMap(filename):
    with open(filename + ".tilemap", "rb") as f:
        levels = pickle.load(f)
        width = pickle.load(f)
        height = pickle.load(f)
        ladders = pickle.load(f)
        data = pickle.load(f)
        graphs = pickle.load(f)
        documents = pickle.load(f)
        start = pickle.load(f)
        end = pickle.load(f)

    map_graph = MapGraph()
    map_graph.CreateGraphs(graphs)

    binary_string = bin(int(binascii.hexlify(data), 16))[2:]

    encoded = ""

    for i in range(len(binary_string) // 5):
        encoded += To_b32(int(binary_string[i * 5: (i + 1) * 5], 2))

    while encoded[-1] == 31:
        encoded = encoded[:-1]

    maps = []

    data = RunLengthDecode(encoded).split(To_b32(31))

    for level in range(levels):
        maps.append([])

        for y in range(height):
            maps[level].append([])

            for x in range(width):
                maps[level][y].append(From_b32(data[level][y * width + x]))

    return MapData(levels, width, height, maps, map_graph, ladders, documents, start, end)


def CreateFromLoadedTileMap(filename):
    global current_map_data
    global save_data

    filename = filename.replace(".tilemap", "")

    if ".savefile" in filename:
        current_map_data, save_data = LoadMapInstance(filename)

    else:
        current_map_data = LoadTileMap(filename)

def RunLengthEncode(decoded):
    encoded = ""
    pointer = 0

    while len(decoded) > pointer:
        rep_times = 0
        repeats = False

        while len(decoded) - pointer >= 4\
                and rep_times < 32\
                and all(decoded[pointer + point] == decoded[pointer] for point in range(rep_times + 3)):

            rep_times += 1
            repeats = True

        else:
            if repeats:
                encoded += To_b32(30) + To_b32(rep_times - 1) + decoded[pointer]
                pointer += rep_times + 2

            else:
                encoded += decoded[pointer]
                pointer += 1

    return encoded


def RunLengthDecode(encoded):
    decoded = ""

    pointer = 0

    while len(encoded) > pointer:
        if encoded[pointer] == To_b32(30):
            decoded += encoded[pointer + 2] * (From_b32(encoded[pointer + 1]) + 3)
            pointer += 3

        else:
            decoded += encoded[pointer]
            pointer += 1

    return decoded


def GetLeaderboard():
    leaderboard = []
    with open("Leaderboard.txt", "rb") as f:
        for i in range(10):
            leaderboard.append(pickle.load(f))
    return leaderboard


def GetBeautifiedLeaderboard():
    leaderboard = GetLeaderboard()
    text = [str(i + 1) + "." + leaderboard[i][0] + " - " + leaderboard[i][1] for i in range(10)]
    meta = [(leaderboard[i][2], leaderboard[i][3], leaderboard[i][4], leaderboard[i][5]) for i in range(10)]
    return text, meta


def SaveLeaderboard(leaderboard_data):
    top_score_count = len(leaderboard_data)

    with open("Leaderboard.txt", "wb") as f:
        for i in range(top_score_count):
            pickle.dump([leaderboard_data[i][0],
                        leaderboard_data[i][1],
                        leaderboard_data[i][2],
                        leaderboard_data[i][3],
                        leaderboard_data[i][4],
                        leaderboard_data[i][5]], f)

        for i in range(10 - top_score_count):
            pickle.dump(["", "", "", "", "", ""], f)


def ScorePlayer(player_name, score, seed, levels, width, height):
    leaderboard_filled = GetLeaderboard()
    leaderboard = []
    pointer = 0

    for player in leaderboard_filled:
        if player != ["", "", "", "", "", ""]:
            leaderboard.append(player)

    if len(leaderboard) < 10:
        leaderboard.append([player_name, ScoreString(score), seed, levels, width, height])

    else:
        while pointer < 10:
            if int(leaderboard[pointer][1]) < score:
                leaderboard.insert(pointer, [player_name, ScoreString(score), seed, levels, width, height])
                pointer += 10
            pointer += 1

    SaveLeaderboard(leaderboard)


def ScoreString(integer):
    score = str(integer)
    while len(score) < 4:
        score = "0" + score
    return score


def CreateMap(levels, width, height, seed):
    global current_map_data

    map_creator = MapCreator(levels, width, height, seed)
    map_creator.CreateMaps()

    current_map_data = MapData(
        levels,
        width,
        height,
        map_creator.maps,
        map_creator.map_graph,
        map_creator.ladders,
        map_creator.documents,
        map_creator.start,
        map_creator.end)


# External classes:
class PerlinNoise2D:
    def __init__(self, seed, octaves=2):
        self.random = LinearCongruentialGenerator(seed)
        self.octaves = octaves
        self.scaleFactor = 1
        self.gradient = {}

    @staticmethod
    def GenerateGradient():
        random_point = [random.gauss(0, 1), random.gauss(0, 1)]  # Needs updating

        scale = math.pow(math.pow(random_point[0], 2) + math.pow(random_point[1], 2), -0.5)

        return scale * random_point[0], scale * random_point[1]

    def getPlainNoise(self, x, y):
        min_x = math.floor(x)
        max_x = min_x + 1
        min_y = math.floor(y)
        max_y = min_y + 1

        dots = []

        for point in [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]:
            if point not in self.gradient:
                self.gradient[point] = self.GenerateGradient()
            gradient = self.gradient[point]

            dots.append(gradient[0] * (x - point[0]) +
                        gradient[1] * (y - point[1]))

        s = self.smoothstep(y - min_y)

        return self.lerp(
            self.smoothstep(x - min_x),
            self.lerp(s, dots[0], dots[1]),
            self.lerp(s, dots[2], dots[3])
            ) * self.scaleFactor

    @staticmethod
    def smoothstep(t):
        return t * t * (3. - 2. * t)

    @staticmethod
    def lerp(t, a, b):
        return a + t * (b - a)

    def ValueAt(self, x, y):
        ret = 0
        for octave in range(1, self.octaves + 1):
            ret += self.getPlainNoise(x * octave, y * octave) / octave

        ret /= 2 - math.pow(2, 1 - self.octaves)

        return ret


class LinearCongruentialGenerator:
    def __init__(self, seed, multiplier=1103515245, increment=12345, modulus=2147483648):
        self._seed = seed
        self._multiplier = multiplier
        self._increment = increment
        self._modulus = modulus
        self._current_value = int(seed)

    def GetNext(self, maximum=-1, minimum=-1):
        self._current_value = (self._multiplier * self._current_value + self._increment) % self._modulus

        if minimum == -1:
            if maximum == -1:
                return self._current_value
            return self._GetNextMax(maximum)
        return self._GetNextMinMax(minimum, maximum)

    def _GetNextMax(self, maximum):
        return self._current_value % maximum

    def _GetNextMinMax(self, minimum, maximum):
        return self._GetNextMax(maximum - minimum) + minimum

    def Modulus(self):
        return self._modulus


class MiddleSquareAlgorithm:
    def __init__(self):
        self._seed = None
        self._middle_size = None
        self._output_size = None
        self._output = None

    def _Limit(self):
        return self._output[:self._output_size]

    def _MiddleSquare(self):
        square = str(self._seed * self._seed)

        left = (len(square) - self._middle_size) // 2
        right = left + self._middle_size

        middle = square[left:right]

        self._output += middle
        self._seed = int(middle)

    def _MiddleSquareAlgorithm(self):
        while len(self._output) < self._output_size:
            self._MiddleSquare()

        return self._Limit()

    def __call__(self, seed, digits):
        self._seed = seed
        self._middle_size = len(str(seed))
        self._output_size = digits
        self._output = ""

        return self._MiddleSquareAlgorithm()


# Start Game:
def BeginGame():
    """Creates a tkinter window and passes it to the game class.
    """
    root = tk.Tk()
    Game(root)
    root.mainloop()


# Main classes:
class Game(tk.Frame):
    def __init__(self, master):  # Initialize the game class.
        tk.Frame.__init__(self, master)
        self.master = master

        self.WIDTH = 1280
        self.HEIGHT = 720

        self.boss_canvas = tk.Canvas(self.master)
        self.boss_image = None

        self.frame = None

        self.display = None
        self.controls = Controls()

        self.data = {}

        self.boss_canvas.config(width=self.WIDTH, height=self.HEIGHT, bg="red")

        self.master.bind("<KeyRelease>", self.KeyUp)
        self.master.bind("<KeyPress>", self.KeyDown)

        self.master.geometry("1280x720")
        self.master.title("Minotaur's Maze")

        self.master.minsize(self.WIDTH, self.HEIGHT)
        self.master.maxsize(self.WIDTH, self.HEIGHT)

        self.master.protocol('WM_DELETE_WINDOW', self.Exit)

        self.ShowMenu()

    def Restart(self):
        global current_map_data
        global save_data

        current_map_data = MapData()
        save_data = None

        self.ShowMenu()

    def KeyDown(self, e):
        result = self.controls.KeyDown(e.keysym)
        if result[0] == -1:
            if result[1] == -1:
                self.Exit()
            elif result[1] == 0:
                self.BOSS_KEY_PRESS()
            elif result[1] == 1:
                self.TogglePausePlay()
        elif result[0] == 0:
            self.display.CanvasWaitNextMove(result[1])
        elif result[0] == 1:
            if result[1] == 0:
                self.display.SpecialTileEvent()

            elif result[1] == 1:
                self.SaveOrQuit()

            elif result[1] == 2:
                self.Restart()

    def SaveOrQuit(self):
        self.display.PauseEnter()

    def KeyUp(self, e):
        result = self.controls.KeyRelease(e.keysym)
        if result[0] == 0:
            if self.controls.IsPaused():
                self.display.ChangePause()
            else:
                self.display.NextMove(result[1])

    def MakeFrame(self):
        self.frame = tk.Frame(self.master)
        self.frame.config(width=self.WIDTH, height=self.HEIGHT)
        self.frame.grid_propagate(False)
        self.frame.pack()

    def DestroyFrame(self):
        if self.frame is not None:
            self.frame.destroy()

    def ResetFrame(self):
        self.DestroyFrame()
        self.MakeFrame()

    def BOSS_KEY_PRESS(self):
        if self.controls.boss_mode:
            self.controls.boss_mode = False
            self.frame.pack()
            self.boss_canvas.pack_forget()
            self.master.title("Minotaur's Maze")
            self.controls.Play()

        else:
            self.controls.boss_mode = True
            self.frame.pack_forget()
            self.boss_canvas.pack()
            self.boss_image = tk.PhotoImage(file=random.choice(BOSS_IMAGES))
            self.boss_canvas.create_image(640, 360, image=self.boss_image)
            self.master.title("Inspirational Images?")
            if not self.controls.IsPaused():
                self.controls.Pause()

    def TogglePausePlay(self):
        if self.controls.paused and not self.controls.boss_mode:
            self.controls.Play()
            self.display.PauseHide()

        elif not self.controls.paused and not self.controls.boss_mode:
            self.controls.Pause()
            self.display.PauseShow()

    def ShowMenu(self):
        self.ResetFrame()
        self.controls.ShowMenu()
        self.display = MenuDisplay(self)

    def LoadGame(self, settings):
        if settings["movement"] == "Arrows":
            self.controls.LEFT = "Left"
            self.controls.RIGHT = "Right"
            self.controls.UP = "Up"
            self.controls.DOWN = "Down"
        else:
            self.controls.LEFT = "a"
            self.controls.RIGHT = "d"
            self.controls.UP = "w"
            self.controls.DOWN = "s"

        if settings["sprint"] == "Ctrl":
            self.controls.SPRINT = "Ctrl_L"
            self.controls.SNEAK = "Shift_L"
        else:
            self.controls.SPRINT = "Shift_L"
            self.controls.SNEAK = "Ctrl_L"

        self.ResetFrame()
        self.controls.LoadGame()
        self.display = LoadDisplay(self)
        self.data = settings
        self.display.Load(settings)

    def StartGame(self, levels):
        self.ResetFrame()
        self.controls.StartGame()
        self.display = GameDisplay(self, levels)
        self.display.Play()

    def GameOver(self, score):
        ScorePlayer("Ben", score, self.data["seed"], self.data["levels"], self.data["width"], self.data["height"])
        self.ResetFrame()
        self.controls.GameOver()
        self.display = GameOverDisplay(self)

    def Exit(self):
        answer = tk.messagebox.askyesno("Quit?", "Are you sure you want to quit?")
        if answer:
            self.master.destroy()


class Controls:
    def __init__(self):
        self.game_state = -1
        self.paused = True
        self.boss_mode = False

        self.konami = False
        self.ghost = False

        self.time_start = 0
        self.time_add = 0

        self.cheats_possible = {"Ghost": ["g", "h", "o", "s", "t"]}
        self.cheats_selected = []
        self.memory = []

        self.LEFT = None
        self.RIGHT = None
        self.UP = None
        self.DOWN = None
        self.SPRINT = None
        self.SNEAK = None
        self.CLIMB = "c"

        self.BOSS_KEY = "q"
        self.EXIT = "Escape"
        self.PAUSE_PLAY = "p"

    def GetTimeTaken(self):
        time_taken = self.time_add

        if not self.IsPaused():
            time_taken += time.time() - self.time_start

        if time_taken >= 3600:
            return "You've spent over an hour on this map."

        seconds = int(time_taken % 60)
        minutes = int((time_taken // 60) % 60)

        if seconds == 0:
            seconds = "00"
        elif seconds <= 9:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)

        if minutes == 0:
            minutes = "00"
        elif minutes <= 9:
            minutes = "0" + str(minutes)
        else:
            minutes = str(minutes)

        return "Time taken: " + minutes + " minutes, " + seconds + " seconds."

    def StartTimer(self):
        self.time_start = time.time()

    def PauseTimer(self):
        self.time_add += time.time() - self.time_start
        self.time_start = 0

    def EndTimer(self):
        self.PauseTimer()
        return self.time_add

    def KeyDown(self, keysym):
        if keysym == self.EXIT:
            return -1, -1

        elif keysym == self.BOSS_KEY:
            return -1, 0  # Boss key.

        elif keysym == self.PAUSE_PLAY:
            return -1, 1  # Pause key.

        elif keysym == self.CLIMB:
            return 1, 0  # Climb key.

        elif keysym == "Return":
            if self.game_state == 2:
                return 1, 1

            elif self.game_state == 3:
                return 1, 2

        elif not self.game_state == 2:  # In main menu:
            new_cheats_selected = []
            self.memory.append(keysym)

            for cheat_name in self.cheats_possible:
                cheat_mem_len = len(self.memory)
                cheat_len = len(self.cheats_possible[cheat_name])

                if cheat_len <= cheat_mem_len:
                    for i in range(cheat_mem_len - cheat_len + 1):
                        for j in range(cheat_len):
                            if self.memory[i + j] != self.cheats_possible[cheat_name][j]:
                                break

                        else:
                            new_cheats_selected.append(cheat_name)

            for cheat in new_cheats_selected:
                if cheat not in self.cheats_selected:
                    print("Adding cheat: " + cheat)
                    self.cheats_selected.append(cheat)

        elif keysym not in self.memory:
            self.memory.append(keysym)

        return self.IsMoveKeyDown()

    def KeyRelease(self, keysym):
        value = (None, None)
        if self.game_state == 2:
            value = self.IsMoveKeyDown()
            try:
                self.memory.remove(keysym)

            except ValueError:  # This means the key has already been removed, so no worries.
                pass

        return value

    def IsGhost(self):
        return self.ghost

    def IsMoveKeyDown(self):
        x = y = 0
        speed = 8

        if self.SPRINT in self.memory:
            speed = speed * 2

        if self.SNEAK in self.memory:
            speed = speed // 2

        if self.UP in self.memory:
            y += 1
        if self.DOWN in self.memory:
            y -= 1
        if self.LEFT in self.memory:
            x += 1
        if self.RIGHT in self.memory:
            x -= 1

        if x != 0 or y != 0:
            return 0, (x, y, speed)
        return 1, None  # Nothing to return.

    def ShowMenu(self):
        self.game_state = 0
        self.ClearMemory()

    def LoadGame(self):
        self.game_state = 1

        if "Ghost" in self.cheats_selected:
            self.ghost = True

        self.ClearMemory()

    def StartGame(self):
        self.game_state = 2
        self.ClearMemory()
        self.Play()

    def GameOver(self):
        self.game_state = 3
        self.Pause()

    def IsPaused(self):
        return self.paused

    def Pause(self):
        self.paused = True
        self.PauseTimer()

    def Play(self):
        self.paused = False
        self.StartTimer()

    def ClearMemory(self):
        self.memory = []


class Display:
    def __init__(self, master):
        self.master = master.frame
        self.main = master


class MenuDisplay(Display):
    def __init__(self, master):
        super().__init__(master)

        self.title_canvas = tk.Canvas(self.master)
        self.title_canvas.config(bg="red")

        self.start_button = tk.Button(self.master)

        self.menu_font = "helvetica 10"

        self.filename = ""

        self.sprint_changed = tk.StringVar()
        self.sneak_changed = tk.StringVar()

        self.levels_changed = tk.StringVar()
        self.width_changed = tk.StringVar()
        self.height_changed = tk.StringVar()
        self.seed_changed = tk.StringVar()

        self.sprint_changed.trace("w", self.SprintChanged)
        self.sneak_changed.trace("w", self.SneakChanged)

        self.levels_changed.trace("w", self.EntryValidation)
        self.width_changed.trace("w", self.EntryValidation)
        self.height_changed.trace("w", self.EntryValidation)
        self.seed_changed.trace("w", self.EntryValidation)

        self.BTN_load_file = tk.Button(
            self.master,
            text="Load File",
            font="helvetica 14",
            command=self.LoadFile
        )

        self.BTN_load_tile_map = tk.Button(
            self.master,
            text="Load Tile Map",
            font="helvetica 14",
            command=self.LoadTileMap
        )

        # Options:
        self.OPTIONS_LBL_title = tk.Label(
            self.master,
            text="Options:",
            font="helvetica 14"
        )

        self.OPTIONS_LBL_difficulty = tk.Label(
            self.master,
            text="Difficulty:",
            font=self.menu_font
        )

        self.OPTIONS_LBL_levels = tk.Label(
            self.master,
            text="Levels:",
            font=self.menu_font
        )

        self.OPTIONS_LBL_width = tk.Label(
            self.master,
            text="Maze Width:",
            font=self.menu_font
        )

        self.OPTIONS_LBL_height = tk.Label(
            self.master,
            text="Maze Height:",
            font=self.menu_font
        )

        self.OPTIONS_LBL_seed = tk.Label(
            self.master,
            text="Seed:",
            font=self.menu_font
        )

        self.OPTIONS_CBX_difficulty = ttk.Combobox(
            self.master,
            values=["Easy", "Normal", "Hard"],
            font=self.menu_font,
            state="readonly"
        )

        self.OPTIONS_ENT_levels = tk.Entry(
            self.master,
            font=self.menu_font,
            textvariable=self.levels_changed
        )

        self.OPTIONS_ENT_width = tk.Entry(
            self.master,
            font=self.menu_font,
            textvariable=self.width_changed
        )

        self.OPTIONS_ENT_height = tk.Entry(
            self.master,
            font=self.menu_font,
            textvariable=self.height_changed
        )

        self.OPTIONS_ENT_seed = tk.Entry(
            self.master,
            font=self.menu_font,
            textvariable=self.seed_changed
        )

        # Controls:
        self.CONTROLS_LBL_title = tk.Label(
            self.master,
            text="Controls:",
            font="helvetica 14"
        )

        self.CONTROLS_LBL_movement = tk.Label(
            self.master,
            text="Movement:",
            font=self.menu_font
        )

        self.CONTROLS_LBL_sprint = tk.Label(
            self.master,
            text="Sprint:",
            font=self.menu_font
        )

        self.CONTROLS_LBL_sneak = tk.Label(
            self.master,
            text="Sneak:",
            font=self.menu_font
        )

        self.CONTROLS_LBL_climb = tk.Label(
            self.master,
            text="Climb:",
            font=self.menu_font
        )

        self.CONTROLS_CBX_movement = ttk.Combobox(
            self.master,
            values=["WASD", "Arrows"],
            font=self.menu_font,
            state="readonly"
        )

        self.CONTROLS_CBX_sprint = ttk.Combobox(
            self.master,
            values=["Ctrl", "Shift"],
            font=self.menu_font,
            state="readonly",
            textvar=self.sprint_changed
        )

        self.CONTROLS_CBX_sneak = ttk.Combobox(
            self.master,
            values=["Ctrl", "Shift"],
            font=self.menu_font,
            state="readonly",
            textvar=self.sneak_changed
        )

        self.CONTROLS_CBX_climb = ttk.Combobox(
            self.master,
            values=["C", "Space"],
            font=self.menu_font,
            state="readonly"
        )

        # Leaderboard:
        self.LEADERBOARD_LBL_title = tk.Label(
            self.master,
            text="Leaderboard:",
            font="helvetica 14"
        )

        self.LEADERBOARD_LBX_leaderboard = tk.Listbox(
            self.master,
            font="times 14"
        )

        # Instructions:
        self.INSTRUCTIONS_LBL_title = tk.Label(
            self.master,
            text="Instructions:",
            font="helvetica 14"
        )

        self.INSTRUCTIONS_LBL_instructions = tk.Label(
            self.master,
            text="You have awoken to find yourself in the Labyrinth, an immense and elaborate maze. Designed by the "
                 "Great Artificer Daedalus for King Minos of Crete 3500 years ago, the Labyrinth was constructed to "
                 "trap the Minotaur, a powerful monster with the body of a man and the head of a bull.\n\nTo survive, "
                 "you must escape the maze as quickly as possible, as if caught in close combat, there is no doubt "
                 "that you will die.\n\nPoints will be awarded for speed in exiting the maze (or distance if you are "
                 "caught), how direct you are in passing each level, and how much information you are able to gather "
                 "(5 pieces of information can be found in each level). Points will be deducted for using "
                 "cheats.\n\nGood Luck!",
            wraplength=280,
            justify="left",
            anchor=tk.N
        )

        self.start_button.config(
            text="START",
            command=self.PrepareToStartGame,
            font="helvetica 24 bold",
            bg="#750505",
            fg="#ebad13",
            activebackground="#4f0000",
            activeforeground="#f2ad00"
        )

        self.ShowLeaderboard()

        self.PlaceAll()

    def LoadFile(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Game Save", ".savefile")])

    def LoadTileMap(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Tile Map", ".tilemap")])

    def ShowLeaderboard(self):
        self.LEADERBOARD_LBX_leaderboard.config(
            selectmode=tk.SINGLE,
            justify=tk.CENTER,
            relief=tk.FLAT,
            bd=0
        )

        for i in range(10):
            self.LEADERBOARD_LBX_leaderboard.insert(i, GetBeautifiedLeaderboard()[0][i])

        self.LEADERBOARD_LBX_leaderboard.bind("<<ListboxSelect>>", self.LeaderboardSelect)

    def LeaderboardSelect(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            seed, levels, width, height = GetBeautifiedLeaderboard()[1][index]  # seed, levels, width, height

            self.SetMeta(seed, levels, width, height)

    def SetMeta(self, seed, levels, width, height):
        if seed != "":
            self.seed_changed.set(seed)
            self.levels_changed.set(levels)
            self.width_changed.set(width)
            self.height_changed.set(height)

    def EntryValidation(self, *args):
        if self.OPTIONS_ENT_levels.get() != "":
            try:
                int(self.OPTIONS_ENT_levels.get())
            except ValueError:
                self.levels_changed.set(self.OPTIONS_ENT_levels.get()[:-1])

        if self.OPTIONS_ENT_width.get() != "":
            try:
                int(self.OPTIONS_ENT_width.get())
            except ValueError:
                self.width_changed.set(self.OPTIONS_ENT_width.get()[:-1])

        if self.OPTIONS_ENT_height.get() != "":
            try:
                int(self.OPTIONS_ENT_height.get())
            except ValueError:
                self.height_changed.set(self.OPTIONS_ENT_height.get()[:-1])

        if self.OPTIONS_ENT_seed.get() != "":
            try:
                int(self.OPTIONS_ENT_seed.get())
            except ValueError:
                self.seed_changed.set(self.OPTIONS_ENT_seed.get()[:-1])

    def SprintChanged(self, *args):
        keys = self.CONTROLS_CBX_sprint["values"]
        current_sprint = self.CONTROLS_CBX_sprint.get()

        if self.CONTROLS_CBX_sneak.get() == current_sprint:
            if keys[0] == current_sprint:
                self.CONTROLS_CBX_sneak.set(keys[1])
            else:
                self.CONTROLS_CBX_sneak.set(keys[0])

    def SneakChanged(self, *args):
        keys = self.CONTROLS_CBX_sneak["values"]
        current_sneak = self.CONTROLS_CBX_sneak.get()

        if self.CONTROLS_CBX_sprint.get() == current_sneak:
            if keys[0] == current_sneak:
                self.CONTROLS_CBX_sprint.set(keys[1])
            else:
                self.CONTROLS_CBX_sprint.set(keys[0])

    def PrepareToStartGame(self):
        self.main.LoadGame(
            {
                "movement": self.CONTROLS_CBX_movement.get(),
                "sprint": self.CONTROLS_CBX_sprint.get(),
                "seed": self.OPTIONS_ENT_seed.get(),
                "width": self.OPTIONS_ENT_width.get(),
                "height": self.OPTIONS_ENT_height.get(),
                "levels": self.OPTIONS_ENT_levels.get(),
                "filename": self.filename
            }
        )

    def PlaceAll(self):
        self.title_canvas.place(x=0, y=0, width=640, height=150)

        self.start_button.place(x=20, y=180, width=600, height=80)

        self.BTN_load_file.place(x=120, y=400, width=400, height=60)

        self.BTN_load_tile_map.place(x=120, y=500, width=400, height=60)

        self.OPTIONS_LBL_title.place(x=720, y=40, width=200, height=60)
        self.OPTIONS_LBL_difficulty.place(x=720, y=100, width=100, height=30)
        self.OPTIONS_LBL_levels.place(x=720, y=130, width=100, height=30)
        self.OPTIONS_LBL_width.place(x=720, y=160, width=100, height=30)
        self.OPTIONS_LBL_height.place(x=720, y=190, width=100, height=30)
        self.OPTIONS_LBL_seed.place(x=720, y=220, width=100, height=30)

        self.OPTIONS_CBX_difficulty.place(x=825, y=105, width=70, height=20)
        self.OPTIONS_CBX_difficulty.current(1)
        self.OPTIONS_ENT_levels.place(x=825, y=135, width=50, height=20)
        self.OPTIONS_ENT_width.place(x=825, y=165, width=50, height=20)
        self.OPTIONS_ENT_height.place(x=825, y=195, width=50, height=20)
        self.OPTIONS_ENT_seed.place(x=825, y=225, width=90, height=20)

        self.CONTROLS_LBL_title.place(x=1000, y=40, width=200, height=60)
        self.CONTROLS_LBL_movement.place(x=1000, y=100, width=100, height=30)
        self.CONTROLS_LBL_sprint.place(x=1000, y=130, width=100, height=30)
        self.CONTROLS_LBL_sneak.place(x=1000, y=160, width=100, height=30)
        self.CONTROLS_LBL_climb.place(x=1000, y=190, width=100, height=30)

        self.CONTROLS_CBX_movement.place(x=1105, y=105, width=70, height=20)
        self.CONTROLS_CBX_movement.current(1)
        self.CONTROLS_CBX_sprint.place(x=1105, y=135, width=70, height=20)
        self.CONTROLS_CBX_sprint.current(1)
        self.CONTROLS_CBX_sneak.place(x=1105, y=165, width=70, height=20)
        self.CONTROLS_CBX_sneak.current(0)
        self.CONTROLS_CBX_climb.place(x=1105, y=195, width=70, height=20)
        self.CONTROLS_CBX_climb.current(0)

        self.LEADERBOARD_LBL_title.place(x=720, y=280, width=200, height=60)
        self.LEADERBOARD_LBX_leaderboard.place(x=720, y=340, width=200, height=340)

        self.INSTRUCTIONS_LBL_title.place(x=950, y=280, width=300, height=60)
        self.INSTRUCTIONS_LBL_instructions.place(x=950, y=340, width=300, height=340)


class LoadDisplay(Display):
    def __init__(self, master):
        super().__init__(master)

        self.thread = None

        self.LBL_State = tk.Label(self.master)
        self.LBL_Percentage = tk.Label(self.master)

    def SetupGUI(self):
        self.LBL_State.config(width=50)
        self.LBL_State.place(x=70, y=100)
        self.LBL_State.config(text="Loading:")

        self.LBL_Percentage.config(width=50)
        self.LBL_Percentage.place(x=70, y=130)
        self.LBL_Percentage.config(text="0%")

    def MapFromFile(self, filename):
        self.thread = threading.Thread(target=CreateFromLoadedTileMap, args=[filename])

    def MapFromSeed(self, levels, width, height, seed):
        if levels == "":
            levels = 8
        else:
            levels = int(levels)

        if width == "":
            width = 32
        else:
            width = int(width)

        if height == "":
            height = 32
        else:
            height = int(height)

        if seed == "":
            seed = GetSeed(8)
        else:
            seed = int(seed)

        self.thread = threading.Thread(target=CreateMap, args=[levels, width, height, seed])

    def Load(self, kwargs):
        self.SetupGUI()
        filename = kwargs["filename"]
        levels = kwargs["levels"]
        width = kwargs["width"]
        height = kwargs["height"]
        seed = kwargs["seed"]

        if filename == "":
            self.MapFromSeed(levels, width, height, seed)

        else:
            self.MapFromFile(filename)

        self.thread.daemon = True
        self.thread.start()
        self.Loading()

    def Loading(self):
        global state
        global progress

        states = {
            0: "Perlin Noise Creation",
            1: "Perlin Noise Adjustments",
            2: "Tile ID Map",
            3: "Create Caves",
            4: "Remove Small Caves",
            5: "Combine Caves",
            6: "Tile Map",
            7: "Saving Map"
        }

        state_text = "Map " + str(state // 8) + ": " + states[state % 8]

        if self.thread.is_alive():
            self.LBL_State.config(text="Loading: " + state_text)
            self.LBL_Percentage.config(text=str(int(progress)) + "%")
            self.master.after(50, self.Loading)
        else:
            self.LBL_State.config(text="Loading:")
            self.LBL_Percentage.config(text="100%")
            self.master.after(2000, self.Loaded)

    def Loaded(self):
        global current_map_data

        map_data = current_map_data

        current_map_data = MapData()

        self.main.StartGame(map_data)


class GameDisplay(Display):
    def __init__(self, master, level_data):
        super().__init__(master)
        global save_data

        self.player_moving = False

        self.next_move = None

        self.can_choose_next_move = True

        self.levels = level_data.levels
        self.width = level_data.width
        self.height = level_data.height
        self.maps = level_data.maps
        self.map_graphs = level_data.map_graph
        self.ladders = level_data.ladders
        self.end_point = level_data.end
        self.documents = level_data.documents

        self.enemies = [Minotaur() for i in range(self.levels)]

        if save_data is None:
            self.level = 0
            self.documents_collected = 0
            self.minotaurs_defeated = 0
            self.start_point = level_data.start

        else:
            self.level = save_data[0]
            self.documents_collected = save_data[1]
            self.minotaurs_defeated = save_data[2]

            for i in range(len(self.enemies)):
                self.enemies[i].defeated = save_data[3][i]

            self.start_point = save_data[4]

        self.tiles = {}
        self.drawn_tiles = []
        self.overlay = None
        self.time_elapsed = None
        self.score = None

        self.tile_images = [tk.PhotoImage(file=tile_name) for tile_name in TILE_NAMES]

        self.pause_screens = [tk.PhotoImage(file=SAVE_AND_QUIT), tk.PhotoImage(file=QUIT)]

        self.drawn_pause = None

        self.save_and_quit_selected = False

        self.player = Player()

        self.canvas = None

        self.Setup()  # Setup variables that need to change on new level.

    def GetSaveData(self):
        return [
            self.level,
            self.documents_collected,
            self.minotaurs_defeated,
            [self.enemies[i].defeated for i in range(len(self.enemies))],
            self.player.GetCoordinates()
        ]

    def MakeSaveFile(self, filename):
        map_data = MapData(
            self.levels,
            self.width,
            self.height,
            self.maps,
            self.map_graphs,
            self.ladders,
            self.documents,
            self.start_point,
            self.end_point
        )

        SaveMapInstance(map_data, filename, self.GetSaveData())

    def Setup(self, coordinates=None):
        self.player_moving = False
        self.can_choose_next_move = True
        self.next_move = (0, 0, 0)

        self.tiles = {}  # An dictionary of canvas images.
        self.drawn_tiles = []

        self.canvas = tk.Canvas(self.master)
        self.canvas.config(bg="black", width=1280, height=720)
        self.canvas.pack()

        self.DrawLevel()
        self.PlacePlayerOnMap(coordinates)
        self.PlaceEnemiesOnMap()

    def DrawLevel(self):
        self.PopulateTiles()
        self.DrawTiles()
        self.DrawEnemy()
        self.DrawPlayer()
        self.DrawOverlay()
        self.DrawTimer()
        self.DrawScore()

    def PauseShow(self):
        self.drawn_pause = self.canvas.create_image(640, 360, image=self.pause_screens[0])
        self.save_and_quit_selected = True
        self.canvas.update()

    def PauseHide(self):
        self.canvas.delete(self.drawn_pause)
        self.drawn_pause = None
        self.save_and_quit_selected = False
        self.canvas.update()

    def ChangePause(self):
        self.canvas.delete(self.drawn_pause)

        if self.save_and_quit_selected:
            self.drawn_pause = self.canvas.create_image(640, 360, image=self.pause_screens[1])
            self.save_and_quit_selected = False

        else:
            self.drawn_pause = self.canvas.create_image(640, 360, image=self.pause_screens[0])
            self.save_and_quit_selected = True

        self.canvas.update()

    def PauseEnter(self):
        if self.save_and_quit_selected:
            filename = filedialog.asksaveasfile()(filetypes=[("Game Save", ".savefile")])
            self.MakeSaveFile(filename)
            self.main.Restart()
            print(100)

        else:
            self.main.Restart()

    def PopulateTiles(self):
        for level in range(self.levels):
            for y in range(self.height):
                for x in range(self.width):
                    self.tiles[(level, y, x)] = self.tile_images[self.maps[level][y][x]]

    def DrawTiles(self):
        for y in range(self.height):
            for x in range(self.width):
                self.drawn_tiles.append(self.canvas.create_image(
                    x * TILE_SIZE,
                    y * TILE_SIZE - 32,
                    image=self.tiles[(self.level, y, x)]
                ))

    def DrawEnemy(self):
        for enemy in self.enemies:
            enemy.image_position = self.canvas.create_image(640, 352, image=enemy.images[0])

    def DrawPlayer(self):
        self.player.image_position = self.canvas.create_image(640, 352, image=self.player.images[0])

    def DrawOverlay(self):
        self.overlay = tk.PhotoImage(file=OVERLAY_IMAGE)
        self.canvas.create_image(640, 360, image=self.overlay)

    def DrawTimer(self):
        self.time_elapsed = self.canvas.create_text(135, 20, fill="green", font="times 12 bold")
        self.UpdateTimer()

    def DrawScore(self):
        self.score = self.canvas.create_text(1000, 20, fill="green", font="times 12 bold")
        self.canvas.itemconfigure(self.score, text=self.ScoreSoFar())

    def PlacePlayerOnMap(self, coordinates):
        if coordinates is None:
            self.player.GoTo((self.start_point[1], self.start_point[2]))

        else:
            self.player.GoTo((coordinates[1], coordinates[2]))

        x, y = self.player.GetCoordinates()

        self.MoveTiles(- (x - 10) * TILE_SIZE, - (y - 6) * TILE_SIZE)

    def PlaceEnemiesOnMap(self):
        for level in range(self.levels):
            if level == self.level and not self.enemies[level].defeated:
                self.PlaceEnemy(random.choice(self.map_graphs.GetGraph(level).GetTiles()), self.enemies[level])

            else:
                self.PlaceEnemy((-100, -100), self.enemies[level])

    def MoveTiles(self, x, y):
        for tile in self.drawn_tiles:
            self.canvas.move(tile, x, y)

        for enemy in self.enemies:
            self.canvas.move(enemy.image_position, x, y)

    def MoveEnemy(self, x, y):
        self.canvas.move(self.enemies[self.level], x, y)

    def PlaceEnemy(self, coordinates, enemy):
        self.canvas.move(enemy.image_position, (coordinates[0] - 10) * TILE_SIZE, (coordinates[1] - 6) * TILE_SIZE)
        if coordinates != (-1, -1):
            self.enemies[self.level].GoTo(coordinates)

    def UpdateTimer(self):
        self.canvas.itemconfigure(self.time_elapsed, text=self.main.controls.GetTimeTaken())
        self.canvas.after(1000, self.UpdateTimer)

    def ScoreSoFar(self):
        return self.documents_collected + self.minotaurs_defeated

    def Play(self):
        while self.main.controls.game_state == 2:
            if not self.main.controls.IsPaused():
                self.canvas.after(16, self.UpdateLoop())

            else:
                self.canvas.after(50, self.PauseLoop())

    def PauseLoop(self):
        self.master.update()

    def UpdateLoop(self):
        """A loop to update the positions of all moving components.

        NOTE:   This code should allow both the player and enemy to move.
                Due to the time-complexity of Dijkstra's algorithm, and the time constraints, I have been unable to
                create a graph of path intersections (which would significantly reduce the time complexity of this
                algorithm. As such, this 'UpdateLoop' only has working code for the player. Code for the enemies has
                been left in, as I want to continue this work in my own time.
        """
        # enemy_x, enemy_y = self.enemies[self.level].GetCoordinates()

        # player_x, player_y = self.player.GetCoordinates()

        # distance = PythagoreanTheorem(player_x - enemy_x, player_y - enemy_y)
        #
        # if self.enemies[self.level].x_offset == 0 and self.enemies[self.level].y_offset == 0:
        #     if (distance < 10 and self.player.speed == 8)\
        #             or (distance < 6 and self.player.speed == 4)\
        #             or distance < 3:
        #
        #         self.enemies[self.level].GoTowards(
        #             self.level,
        #             player_x,
        #             player_y,
        #             self.map_graphs)
        #
        #     elif not self.enemies[self.level].path:
        #         self.enemies[self.level].GoTowards(self.level, player_x, player_y, self.map_graphs)
        #
        #     else:
        #         next_location = self.enemies[self.level].GetNextMove()
        #
        #         self.enemies[self.level].direction = (next_location[0] - self.enemies[self.level].x_position,
        #                                               next_location[1] - self.enemies[self.level].y_position)

        if self.player.x_offset == 0 and self.player.y_offset == 0:
            self.player.direction = (self.next_move[0], self.next_move[1])
            self.player.speed = self.next_move[2]
            self.next_move = (0, 0, 0)

            if self.player.direction == (0, 0):
                self.can_choose_next_move = True

            else:
                self.can_choose_next_move = False

        elif PythagoreanTheorem(self.player.x_offset, self.player.y_offset) >= 48:
            self.can_choose_next_move = True

        else:
            self.can_choose_next_move = False

        # if self.enemies[self.level].direction[0] == 1 and self.enemies[self.level].direction[1] == 1:
        #     self.enemies[self.level].x_offset += math.sqrt(8)
        #     self.enemies[self.level].y_offset += math.sqrt(8)
        #     enemy_delta_x = math.sqrt(8)
        #     enemy_delta_y = math.sqrt(8)
        #
        # elif self.enemies[self.level].direction[0] == -1 and self.enemies[self.level].direction[1] == 1:
        #     self.enemies[self.level].x_offset -= math.sqrt(8)
        #     self.enemies[self.level].y_offset += math.sqrt(8)
        #     enemy_delta_x = - math.sqrt(8)
        #     enemy_delta_y = math.sqrt(8)
        #
        # elif self.enemies[self.level].direction[0] == 1 and self.enemies[self.level].direction[1] == -1:
        #     self.enemies[self.level].x_offset += math.sqrt(8)
        #     self.enemies[self.level].y_offset -= math.sqrt(8)
        #     enemy_delta_x = math.sqrt(8)
        #     enemy_delta_y = - math.sqrt(8)
        #
        # elif self.enemies[self.level].direction[0] == -1 and self.enemies[self.level].direction[1] == -1:
        #     self.enemies[self.level].x_offset -= math.sqrt(8)
        #     self.enemies[self.level].y_offset -= math.sqrt(8)
        #     enemy_delta_x = - math.sqrt(8)
        #     enemy_delta_y = - math.sqrt(8)
        #
        # elif self.enemies[self.level].direction[0] == 1:  # Horizontal
        #     self.enemies[self.level].x_offset += 4
        #     self.enemies[self.level].y_offset = 0
        #     enemy_delta_x = 4
        #     enemy_delta_y = 0
        #
        # elif self.enemies[self.level].direction[0] == -1:  # Horizontal
        #     self.enemies[self.level].x_offset -= 4
        #     self.enemies[self.level].y_offset = 0
        #     enemy_delta_x = - 4
        #     enemy_delta_y = 0
        #
        # elif self.enemies[self.level].direction[1] == 1:  # Vertical
        #     self.enemies[self.level].x_offset = 0
        #     self.enemies[self.level].y_offset += 4
        #     enemy_delta_x = 0
        #     enemy_delta_y = 4
        #
        # elif self.enemies[self.level].direction[1] == -1:  # Vertical
        #     self.enemies[self.level].x_offset = 0
        #     self.enemies[self.level].y_offset -= 4
        #     enemy_delta_x = 0
        #     enemy_delta_y = - 4
        #
        # else:  # Not moving
        #     self.enemies[self.level].x_offset = 0
        #     self.enemies[self.level].y_offset = 0
        #     enemy_delta_x = 0
        #     enemy_delta_y = 0

        if self.player.direction[0] == 1 and self.player.direction[1] == 1:
            self.player.x_offset += math.sqrt(self.player.speed * 2)
            self.player.y_offset += math.sqrt(self.player.speed * 2)
            player_delta_x = math.sqrt(self.player.speed * 2)
            player_delta_y = math.sqrt(self.player.speed * 2)

        elif self.player.direction[0] == -1 and self.player.direction[1] == 1:
            self.player.x_offset -= math.sqrt(self.player.speed * 2)
            self.player.y_offset += math.sqrt(self.player.speed * 2)
            player_delta_x = - math.sqrt(self.player.speed * 2)
            player_delta_y = math.sqrt(self.player.speed * 2)

        elif self.player.direction[0] == 1 and self.player.direction[1] == -1:
            self.player.x_offset += math.sqrt(self.player.speed * 2)
            self.player.y_offset -= math.sqrt(self.player.speed * 2)
            player_delta_x = math.sqrt(self.player.speed * 2)
            player_delta_y = - math.sqrt(self.player.speed * 2)

        elif self.player.direction[0] == -1 and self.player.direction[1] == -1:
            self.player.x_offset -= math.sqrt(self.player.speed * 2)
            self.player.y_offset -= math.sqrt(self.player.speed * 2)
            player_delta_x = - math.sqrt(self.player.speed * 2)
            player_delta_y = - math.sqrt(self.player.speed * 2)

        elif self.player.direction[0] == 1:
            self.player.x_offset += self.player.speed
            self.player.y_offset = 0
            player_delta_x = self.player.speed
            player_delta_y = 0

        elif self.player.direction[0] == -1:
            self.player.x_offset -= self.player.speed
            self.player.y_offset = 0
            player_delta_x = - self.player.speed
            player_delta_y = 0

        elif self.player.direction[1] == 1:
            self.player.x_offset = 0
            self.player.y_offset += self.player.speed
            player_delta_x = 0
            player_delta_y = self.player.speed

        elif self.player.direction[1] == -1:
            self.player.x_offset = 0
            self.player.y_offset -= self.player.speed
            player_delta_x = 0
            player_delta_y = - self.player.speed

        else:  # Not moving
            self.player.x_offset = 0
            self.player.y_offset = 0
            player_delta_x = 0
            player_delta_y = 0

        # if abs(self.enemies[self.level].x_offset) >= TILE_SIZE:
        #     enemy_delta_x += (TILE_SIZE - abs(self.enemies[self.level].x_offset))
        #     self.enemies[self.level].x_offset = 0
        #
        # if abs(self.enemies[self.level].y_offset) >= TILE_SIZE:
        #     enemy_delta_y += (TILE_SIZE - abs(self.enemies[self.level].y_offset))
        #     self.enemies[self.level].y_offset = 0

        if self.player.x_offset >= TILE_SIZE:
            player_delta_x += (TILE_SIZE - self.player.x_offset)

            self.player.Move(1, 0)

            self.player.x_offset = 0

        if self.player.x_offset <= - TILE_SIZE:
            player_delta_x -= (self.player.x_offset + TILE_SIZE)

            self.player.Move(-1, 0)

            self.player.x_offset = 0

        if self.player.y_offset >= TILE_SIZE:
            player_delta_y += (TILE_SIZE - self.player.y_offset)

            self.player.Move(0, 1)

            self.player.y_offset = 0

        if self.player.y_offset <= - TILE_SIZE:
            player_delta_y -= (self.player.y_offset + TILE_SIZE)

            self.player.Move(0, -1)

            self.player.y_offset = 0

        # self.MoveEnemy(enemy_delta_x, enemy_delta_y)

        try:
            self.MoveTiles(player_delta_x, player_delta_y)
            self.master.update()
        except tk.TclError:
            pass

    def NextMove(self, xys):
        if self.can_choose_next_move:
            self.TryMove(xys[0], xys[1], xys[2])

    def TryMove(self, x, y, s):
        if self.CanMove(x, y):
            self.next_move = (x, y, s)

    def CanMove(self, x, y):
        player_coordinates = self.player.GetCoordinates()
        directions = self.GetAccessible(player_coordinates[0], player_coordinates[1])

        if (not self.main.controls.IsPaused()) and ((-x, -y) in directions or self.main.controls.IsGhost()):
            return True
        return

    def GetAccessible(self, x, y):
        accessible_tiles = [20, 21, 22, 23, 25, 27, 28, 29]

        accessible = []

        if self.GetTileAt(x + 1, y) in accessible_tiles:
            accessible.append((1, 0))

        if self.GetTileAt(x - 1, y) in accessible_tiles:
            accessible.append((-1, 0))

        if self.GetTileAt(x, y + 1) in accessible_tiles:
            accessible.append((0, 1))

        if self.GetTileAt(x, y - 1) in accessible_tiles:
            accessible.append((0, -1))

        if (0, 1) in accessible and (1, 0) in accessible and self.GetTileAt(x + 1, y + 1) in accessible_tiles:
            accessible.append((1, 1))
        if (0, -1) in accessible and (1, 0) in accessible and self.GetTileAt(x + 1, y - 1) in accessible_tiles:
            accessible.append((1, -1))
        if (0, 1) in accessible and (-1, 0) in accessible and self.GetTileAt(x - 1, y + 1) in accessible_tiles:
            accessible.append((-1, 1))
        if (0, -1) in accessible and (-1, 0) in accessible and self.GetTileAt(x - 1, y - 1) in accessible_tiles:
            accessible.append((-1, -1))

        return accessible

    def GetTileAt(self, x, y):
        return self.maps[self.level][y][x]

    def SpecialTileEvent(self):
        x, y = self.player.GetCoordinates()
        tile = self.GetTileAt(x, y)

        if tile == 27:
            self.TryClimbLadder()

        elif tile == 28:
            self.TryPickupDocument()

        elif tile == 29:
            print("You Win!!!")
            self.main.Exit()

        elif (x, y) == self.enemies[self.level].GetCoordinates():
            self.StartBattle()

    def StartBattle(self):
        print("Battle start")
        self.enemies[self.level].defeated = True
        self.PlaceEnemy((-1, -1), self.enemies[self.level])
        self.minotaurs_defeated += 1

    def TryClimbLadder(self):
        coordinates = self.player.GetCoordinates()
        coordinates = (self.level, coordinates[0], coordinates[1])

        new_coordinates_up = self.TryClimbUpLadder(coordinates)
        new_coordinates_down = self.TryClimbDownLadder(coordinates)

        if new_coordinates_up != coordinates:
            self.Climb(new_coordinates_up)

        elif new_coordinates_down != coordinates:
            self.Climb(new_coordinates_down)

    def TryClimbUpLadder(self, coordinates):
        for index in range(len(self.ladders)):
            if coordinates == self.ladders[index][0]:
                return self.ladders[index][1]
        return coordinates

    def TryClimbDownLadder(self, coordinates):
        for index in range(len(self.ladders)):
            if coordinates == self.ladders[index][1]:
                return self.ladders[index][0]
        return coordinates

    def Climb(self, new_coordinates):
        self.level = new_coordinates[0]
        self.Reset(new_coordinates)

    def TryPickupDocument(self):
        x, y = self.player.GetCoordinates()
        self.ChangeTile(self.level, x, y, 25)
        self.documents_collected += 1
        self.documents.remove((self.level, x, y))
        self.canvas.itemconfigure(self.score, text=self.ScoreSoFar())

    def ChangeTile(self, level, x, y, new_tile):
        self.maps[self.level][y][x] = new_tile
        if level == self.level:
            self.canvas.itemconfig(self.drawn_tiles[y * self.width + x], image=self.tile_images[new_tile])

    def Reset(self, coordinates):
        self.canvas.destroy()
        self.Setup(coordinates)

    def CanvasWaitNextMove(self, xys):
        self.canvas.after(50, self.CheckForDirection, xys)

    def CheckForDirection(self, xys):
        result = self.main.controls.IsMoveKeyDown()
        if result[0] == 0:
            self.NextMove(result[1])
        else:
            self.NextMove(xys)


class GameOverDisplay(Display):
    def __init__(self, master):
        super().__init__(master)

        self.canvas = tk.Canvas(self.master)
        self.canvas.config(bg="black", width=1280, height=720)
        self.canvas.pack()

        self.canvas_image = tk.PhotoImage(file=CONGRATULATIONS)
        self.canvas.create_image(640, 360, image=self.canvas_image)

class Entity:
    def __init__(self, x, y, speed, images):
        self.x_position = x
        self.y_position = y
        self.x_offset = 0
        self.y_offset = 0
        self.speed = speed
        self.direction = (0, 0)
        self.imgs = images
        self.images = [tk.PhotoImage(file=img) for img in self.imgs]
        self.image_position = None

    def GoTo(self, coordinates):
        self.x_position = coordinates[0]
        self.y_position = coordinates[1]

    def Move(self, x, y):
        self.x_position -= x
        self.y_position -= y

    def GetCoordinates(self):
        return self.x_position, self.y_position


class Player(Entity):
    def __init__(self):
        super().__init__(-1, -1, 1, PLAYER_SPRITES)


class Minotaur(Entity):
    def __init__(self):
        super().__init__(-1, -1, 1, MINOTAUR_SPRITES)
        self.path = []
        self.defeated = False

    def GoTowards(self, level, x, y, map_graph):
        self.path = map_graph.GetShortest(level, self.GetCoordinates(), (x, y))

    def GetNextMove(self):
        if len(self.path) > 0:
            next_move = self.path[0]
            self.path = self.path[1:]
            return next_move

        else:
            return -1, -1  # Error to get a new destination


# Map data struct
class MapData:
    def __init__(self,
                 levels=None,
                 width=None,
                 height=None,
                 maps=None,
                 map_graph=None,
                 ladders=None,
                 documents=None,
                 start=None,
                 end=None):

        self.levels = levels
        self.width = width
        self.height = height
        self.maps = maps
        self.map_graph = map_graph
        self.ladders = ladders
        self.documents = documents
        self.start = start
        self.end = end


class MapCreator:
    def __init__(self, levels, width, height, seed):
        # Constants:
        self.OCTAVES = 2
        self.SCALE = 1 / 15
        self.CUT_OFF_POINT = 0.5
        self.PERLIN_SAMPLE = 2
        self.BLOCK_SAMPLE = 3
        self.MIN_ROOM_SIZE = 4
        self.DIGITS_PER_SEED = 8

        # Parameters:
        self.levels = levels
        self.width = width
        self.height = height
        self.seeds = self.CreateSeeds(seed)

        # Level variables:
        self.perlin_seed = None
        self.ladder_seed = None

        # Map variables:
        self.map_graph = MapGraph()
        self.maps = []
        self.ladders = []
        self.documents = []
        self.start = None
        self.end = None

    def SaveToTempFile(self):
        """Saves self.levels, self.width, self.height, self.levels, self.ladders, self.maps
        """
        pass

    def CreateSeeds(self, base_seed):
        middle_square = MiddleSquareAlgorithm()
        seed_string = middle_square(base_seed, 8 * self.levels * 2)

        return [seed_string[i * 8:(i+1) * 8] for i in range(self.levels * 2)]

    def CreateMaps(self):
        interior_maps = []

        for level in range(self.levels):
            self.perlin_seed = self.seeds[level * 2]
            self.ladder_seed = self.seeds[level * 2 + 1]

            interior_maps.append(self.CreateMap())

        self.map_graph.CreateGraphs(interior_maps)

        self.AddSpecialTiles(interior_maps)

    def AddStart(self, interior_maps):
        start = random.choice(interior_maps[0])
        self.start = (0, start[0], start[1])
        return [self.start]

    def GetLadderFeet(self, interior_maps, special_tiles):
        ladder_feet = []
        current_level = 0

        while len(ladder_feet) < self.levels - 1:
            ladders_this_level = random.randint(1, min(self.levels - len(ladder_feet), 4))

            for ladder_index in range(ladders_this_level):
                current_ladder = self.start

                while current_ladder in special_tiles:
                    current_ladder = random.choice(interior_maps[current_level])
                    current_ladder = (current_level, current_ladder[0], current_ladder[1])

                else:
                    special_tiles.append(current_ladder)
                    ladder_feet.append(current_ladder)

            current_level += 1

        return ladder_feet, special_tiles

    def GetLevelsForLadderHeads(self, ladder_feet):
        level_feet_order = [ladder_foot[0] for ladder_foot in ladder_feet]  # A list of levels (with repeats).
        level_head_order = [level + 1 for level in range(self.levels - 1)]  # A list of levels (no repeats).

        while any(level_feet_order[index] == level_head_order[index] for index in range(self.levels - 1)):
            random.shuffle(level_head_order)

        return level_head_order

    def GetLadderHeads(self, interior_maps, special_tiles, level_head_order):
        ladder_heads = []

        for level in level_head_order:
            current_ladder = self.start

            while current_ladder in special_tiles:
                current_ladder = random.choice(interior_maps[level])
                current_ladder = (level, current_ladder[0], current_ladder[1])
            else:
                special_tiles.append(current_ladder)
                ladder_heads.append(current_ladder)

        return ladder_heads, special_tiles

    def CreateLadders(self, ladder_feet, ladder_heads):
        ladders = []

        for index in range(self.levels - 1):
            ladders.append((ladder_feet[index], ladder_heads[index]))

        return ladders

    def AddDocuments(self, interior_maps, special_tiles):
        documents = []

        for level in range(self.levels):
            doc_in_level = random.randint(MIN_DOCS_PER_LEVEL, MAX_DOCS_PER_LEVEL)

            for i in range(doc_in_level):
                current_doc = self.start

                while current_doc in special_tiles:
                    current_doc = random.choice(interior_maps[level])
                    current_doc = (level, current_doc[0], current_doc[1])
                else:
                    documents.append(current_doc)
                    special_tiles.append(current_doc)

        return documents, special_tiles

    def GetFurthestLevel(self):
        level_map = []

        for ladder in self.ladders:
            level_map.append((ladder[0][0], ladder[1][0]))  # Get levels.

        level_length = [[0]]

        is_at_end = False

        while not is_at_end:
            new_level_length = []
            is_at_end = True
            for level_string in level_length:
                new_level_string = []
                for index in range(len(level_map)):
                    if level_string[-1] == level_map[index][0]:
                        new_level_string = level_string.copy()
                        new_level_string.append(level_map[index][1])
                        new_level_length.append(new_level_string)
                        is_at_end = False

                if not new_level_string:
                    new_level_length.append(level_string)

            level_length = new_level_length

        index_of_longest = -1
        longest = -1

        for index in range(len(level_length)):
            if len(level_length[index]) >= longest:
                index_of_longest = index
                longest = len(level_length[index])

        return level_length[index_of_longest][-1]

    def AddEnd(self, interior_maps, special_tiles, last_level):
        tile = self.start

        while tile in special_tiles:
            tile = random.choice(interior_maps[last_level])
            tile = (last_level, tile[0], tile[1])

        else:
            self.end = tile

    def AddSpecialTiles(self, interior_maps):
        special_tiles = self.AddStart(interior_maps)

        ladder_feet, special_tiles = self.GetLadderFeet(interior_maps, special_tiles)

        level_head_order = self.GetLevelsForLadderHeads(ladder_feet)

        ladder_heads, special_tiles = self.GetLadderHeads(interior_maps, special_tiles, level_head_order)

        self.ladders = self.CreateLadders(ladder_feet, ladder_heads)

        self.documents, special_tiles = self.AddDocuments(interior_maps, special_tiles)

        furthest_level = self.GetFurthestLevel()

        self.AddEnd(interior_maps, special_tiles, furthest_level)

        for level in range(self.levels):
            self.maps.append(self.CreateMapFromCaveSystem(interior_maps[level], level))

    def CreateMap(self):
        interior_blocks = self.CreatePerlinMap()
        rooms = self.GetRooms(interior_blocks)
        cave_system = self.ConnectRooms(rooms)
        return cave_system

    def CreatePerlinMap(self):
        global state
        global progress

        state += 1
        progress = 0

        perlin_noise = PerlinNoise2D(self.perlin_seed, self.OCTAVES)

        interior_blocks = []

        noise = []

        min_val = -1
        max_val = -1

        for y in range(self.height * self.PERLIN_SAMPLE):
            noise.append([])

            for x in range(self.width * self.PERLIN_SAMPLE):
                current_noise = perlin_noise.ValueAt(y * self.SCALE, x * self.SCALE)

                if min_val == -1 or min_val > current_noise:
                    min_val = current_noise

                if max_val == -1 or max_val < current_noise:
                    max_val = current_noise

                noise[y].append(current_noise)

            progress = (100 * (y + 1)) / (self.height * self.PERLIN_SAMPLE)

        val_range = max_val - min_val

        state += 1
        progress = 0

        for y in range(self.height):
            for x in range(self.width):
                sum_sample = 0

                for j in range(self.PERLIN_SAMPLE):
                    for i in range(self.PERLIN_SAMPLE):
                        sum_sample += (noise[y * self.PERLIN_SAMPLE + j]
                                       [x * self.PERLIN_SAMPLE + i] - min_val) / val_range  # Between 0 and 1

                average = sum_sample / (math.pow(self.PERLIN_SAMPLE, 2))  # Between 0 and 1
                bordered = self.DarkenPerimeter(x, y, average)

                if self.BlackOrWhite(bordered) == 1:
                    interior_blocks.append((x, y))

            progress = (100 * (y + 1)) / self.height

        return interior_blocks

    def GetRooms(self, interior_blocks):
        global state
        global progress

        state += 1
        progress = 0

        rooms = []

        count = 0

        for coords_a in interior_blocks:
            count += 1

            adj_room_i = []  # AdjacentRoomIndices was quite long.
            if len(rooms) == 0:
                rooms.append([])
                rooms[0].append(coords_a)

            else:
                for room_index in range(len(rooms)):
                    for coords_b in rooms[room_index]:
                        if self.IsAdjacent(coords_a, coords_b):
                            adj_room_i.append(room_index)
                            break

                    # Breaks to here, so no repeated room indices.
                if len(adj_room_i) >= 1:  # Could be more than one room.
                    rooms[adj_room_i[0]].append(coords_a)

                    to_remove = []

                    while len(adj_room_i) >= 2:
                        rooms[adj_room_i[0]] += rooms[adj_room_i[1]]
                        to_remove.append(adj_room_i[1])
                        adj_room_i.pop(1)

                    while len(to_remove) >= 1:
                        rooms.pop(to_remove[-1])  # Remove the last room, so that indices aren't messed up.
                        to_remove.pop(-1)

                else:
                    rooms.append([])
                    rooms[-1].append(coords_a)

            progress = 100 * count / len(interior_blocks)

        return self.LimitRoomSize(rooms)

    def LimitRoomSize(self, rooms):
        global state
        global progress

        state += 1
        progress = 0

        new_rooms = []

        count = 0

        for room in rooms:
            count += 1

            if len(room) >= self.MIN_ROOM_SIZE:
                new_rooms.append(room)

            progress = 100 * count / len(rooms)

        return new_rooms

    def CreateMapFromCaveSystem(self, cave_system, level):
        global state
        global progress

        state += 1
        progress = 0

        current_map = []

        block_map = []
        for y in range(self.height):
            block_map.append([])

            for x in range(self.width):
                block = 0
                if (x, y) in cave_system:
                    block = 1
                block_map[y].append(block)

                progress = 100 * (y + 1) / self.height

        state += 1
        progress = 0

        ladder_points = []
        document_points = []

        if self.end[0] == level:
            end_point = (self.end[1], self.end[2])
        else:
            end_point = (-1, -1)

        for ladder in self.ladders:
            for ladder_point in range(2):
                if ladder[ladder_point][0] == level:
                    ladder_coordinates = ladder[ladder_point]
                    ladder_points.append((ladder_coordinates[1], ladder_coordinates[2]))

        for document in self.documents:
            if document[0] == level:
                document_points.append((document[1], document[2]))

        for y in range(self.height):
            current_map.append([])

            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    tileIndex = 26

                elif (x, y) in ladder_points:
                    tileIndex = 27

                elif (x, y) in document_points:
                    tileIndex = 28

                elif (x, y) == end_point:
                    tileIndex = 29

                else:
                    tileIndex = self.GetTile(self.GetBlocksAround(block_map, x, y))

                current_map[y].append(tileIndex)

            progress = 100 * (y + 1) / self.height

        return current_map

    def DarkenPerimeter(self, x, y, noise):
        inner_x = (x - self.width / 2) / (5 * self.width / 12)
        inner_y = (y - self.height / 2) / (5 * self.height / 12)

        outer_x = (x - self.width / 2) / (23 * self.width / 48)
        outer_y = (y - self.height / 2) / (23 * self.height / 48)

        radius_sqr1 = math.pow(inner_x, 2) + math.pow(inner_y, 2)
        radius_sqr2 = math.pow(outer_x, 2) + math.pow(outer_y, 2)

        if radius_sqr1 > 1:
            if radius_sqr2 <= 1:
                return (1 - (radius_sqr1 - 1) / (radius_sqr1 - radius_sqr2)) * noise

            else:
                return 0

        return noise

    def BlackOrWhite(self, value):
        if value < self.CUT_OFF_POINT:
            return 0

        return 1

    def IsAdjacent(self, point_a, point_b):

        distance = self.Distance(point_a, point_b, 0)

        if distance != -1 and distance <= 1:  # No diagonals, only horizontal and vertical.
            return True

        return False

    def DigDirection(self, from_a, to_b):
        distY, distX = self.Distance(from_a, to_b, 2)

        if distX < distY:
            if from_a[0] > to_b[0]:
                return "Up"
            return "Down"
        else:
            if from_a[1] < to_b[1]:
                return "Right"
            return "Left"

    def Dig(self, rooms, room_index_a, room_index_b, coords_a, coords_b):
        current_coords = coords_a

        while current_coords != coords_b:
            digDir = self.DigDirection(current_coords, coords_b)

            if digDir == "Right":
                current_coords = (current_coords[0], current_coords[1] + 1)

            elif digDir == "Up":
                current_coords = (current_coords[0] - 1, current_coords[1])

            elif digDir == "Left":
                current_coords = (current_coords[0], current_coords[1] - 1)

            elif digDir == "Down":
                current_coords = (current_coords[0] + 1, current_coords[1])

            else:
                raise Exception

            if current_coords == coords_b:
                rooms[room_index_a] = rooms[room_index_a] + rooms[room_index_b]

            else:
                rooms[room_index_a].append(current_coords)

        rooms.pop(room_index_b)
        return rooms

    def ConnectRooms(self, rooms):
        global state
        global progress

        state += 1
        progress = 0

        room_count = len(rooms)

        while len(rooms) > 1:
            bounds = self.GetRoomBounds(rooms)

            min_distance = -1
            coords = (-1, -1)

            for room_index_a in range(len(rooms) - 1):
                for room_index_b in range(len(rooms) - room_index_a - 1):
                    current_distance = self.BoundsMinDistance(
                        bounds[room_index_a],
                        bounds[room_index_a + room_index_b + 1]
                    )

                    if min_distance == -1 or current_distance < min_distance:
                        min_distance = current_distance
                        coords = (room_index_a, room_index_a + room_index_b + 1)

            min_distance = -1
            coords_a = (-1, -1)
            coords_b = (-1, -1)

            for block_a in rooms[coords[0]]:
                for block_b in rooms[coords[1]]:
                    current_distance = self.Distance(block_a, block_b)

                    if min_distance == -1 or current_distance < min_distance:
                        min_distance = current_distance
                        coords_a = block_a
                        coords_b = block_b

            rooms = self.Dig(rooms, coords[0], coords[1], coords_a, coords_b)

            progress = 100 * (1 - (len(rooms) / room_count))

        return rooms[0]

    @staticmethod
    def GetBlocksAround(block_map, x, y):
        blocks = []

        for j in range(3):
            for i in range(3):
                blocks.append(block_map[y + j - 1][x + i - 1])

        return blocks

    @staticmethod
    def BoundsMinDistance(bounds_a, bounds_b):
        a_min_x = bounds_a[0]
        a_min_y = bounds_a[1]
        a_max_x = bounds_a[2]
        a_max_y = bounds_a[3]

        b_min_x = bounds_b[0]
        b_min_y = bounds_b[1]
        b_max_x = bounds_b[2]
        b_max_y = bounds_b[3]

        if (a_min_x <= b_min_x <= a_max_x) or (a_min_x <= b_max_x <= a_max_x):
            delta_x = 0

        else:
            delta_x = min(abs(b_min_x - a_max_x), abs(a_min_x - b_max_x))

        if (a_min_y <= b_min_y <= a_max_y) or (a_min_y <= b_max_y <= a_max_y):
            delta_y = 0

        else:
            delta_y = min(abs(b_min_y - a_max_y), abs(a_min_y - b_max_y))

        return math.sqrt(delta_x * delta_x + delta_y * delta_y)

    @staticmethod
    def GetRoomBounds(rooms):
        room_bounds = []  # An array of (min_x, min_y, max_x, max_y)

        for room_index in range(len(rooms)):
            room_bounds.append((-1, -1, -1, -1))
            for coords in rooms[room_index]:
                bounds = room_bounds[room_index]

                min_x = min(bounds[0], coords[0])
                min_y = min(bounds[1], coords[1])
                max_x = max(bounds[2], coords[0])
                max_y = max(bounds[3], coords[1])

                if min_x == -1:
                    min_x = coords[0]

                if min_y == -1:
                    min_y = coords[1]

                room_bounds[room_index] = (min_x, min_y, max_x, max_y)

        return room_bounds

    @staticmethod
    def GetTile(blocks_around):
        def IsBlock(surrounding_blocks, test_block):
            is_block = True

            for blockIndex in range(9):
                if test_block[blockIndex] != 2 and test_block[blockIndex] != surrounding_blocks[blockIndex]:
                    # If not optional, and not desired:

                    is_block = False
                    break

            return is_block

        # Walls:

        if (IsBlock(blocks_around, [2, 0, 2,
                                    0, 0, 0,
                                    2, 1, 2])):
            return 0

        elif (IsBlock(blocks_around, [2, 0, 2,
                                      1, 0, 0,
                                      2, 0, 2])):
            return 1

        elif (IsBlock(blocks_around, [2, 1, 2,
                                      0, 0, 0,
                                      2, 0, 2])):
            return 2

        elif (IsBlock(blocks_around, [2, 0, 2,
                                      0, 0, 1,
                                      2, 0, 2])):
            return 3

        # Inner Corners:

        elif (IsBlock(blocks_around, [0, 0, 0,
                                      0, 0, 0,
                                      0, 0, 1])):
            return 4

        elif (IsBlock(blocks_around, [0, 0, 0,
                                      0, 0, 0,
                                      1, 0, 0])):
            return 5

        elif (IsBlock(blocks_around, [1, 0, 0,
                                      0, 0, 0,
                                      0, 0, 0])):
            return 6

        elif (IsBlock(blocks_around, [0, 0, 1,
                                      0, 0, 0,
                                      0, 0, 0])):
            return 7

        # Outer Corners:

        elif (IsBlock(blocks_around, [0, 0, 2,
                                      0, 0, 1,
                                      2, 1, 1])):
            return 8

        elif (IsBlock(blocks_around, [2, 0, 0,
                                      1, 0, 0,
                                      1, 1, 2])):
            return 9

        elif (IsBlock(blocks_around, [1, 1, 2,
                                      1, 0, 0,
                                      2, 0, 0])):
            return 10

        elif (IsBlock(blocks_around, [2, 1, 1,
                                      0, 0, 1,
                                      0, 0, 2])):
            return 11

        # Wall End:

        elif (IsBlock(blocks_around, [2, 0, 2,
                                      1, 0, 1,
                                      1, 1, 1])):
            return 12

        elif (IsBlock(blocks_around, [1, 1, 2,
                                      1, 0, 0,
                                      1, 1, 2])):
            return 13

        elif (IsBlock(blocks_around, [1, 1, 1,
                                      1, 0, 1,
                                      2, 0, 2])):
            return 14

        elif (IsBlock(blocks_around, [2, 1, 1,
                                      0, 0, 1,
                                      2, 1, 1])):
            return 15

        elif (IsBlock(blocks_around, [1, 1, 0,
                                      1, 0, 1,
                                      1, 1, 1])):
            return 16

        elif (IsBlock(blocks_around, [1, 1, 1,
                                      1, 0, 1,
                                      1, 1, 0])):
            return 17

        elif (IsBlock(blocks_around, [1, 1, 1,
                                      1, 0, 1,
                                      0, 1, 1])):
            return 18

        elif (IsBlock(blocks_around, [0, 1, 1,
                                      1, 0, 1,
                                      1, 1, 1])):
            return 19

        # Walls: Blocks 20 to 23 have been changed to 25, as they didn't fit properly.

        elif (IsBlock(blocks_around, [2, 0, 2,
                                      0, 1, 1,
                                      2, 1, 2])):
            return 25

        elif (IsBlock(blocks_around, [2, 0, 2,
                                      1, 1, 0,
                                      2, 1, 2])):
            return 25

        elif (IsBlock(blocks_around, [2, 1, 2,
                                      1, 1, 0,
                                      2, 0, 2])):
            return 25

        elif (IsBlock(blocks_around, [2, 1, 2,
                                      0, 1, 1,
                                      2, 0, 2])):
            return 25

        # Pillar:

        elif (IsBlock(blocks_around, [1, 1, 1,
                                      1, 0, 1,
                                      1, 1, 1])):
            return 24

        # Floor:

        elif (IsBlock(blocks_around, [2, 2, 2,
                                      2, 1, 2,
                                      2, 2, 2])):
            return 25

        else:

            return 26

    @staticmethod
    def Distance(point_a, point_b, dist_type=1):

        xDistance = abs(point_a[0] - point_b[0])
        yDistance = abs(point_a[1] - point_b[1])

        if dist_type == 0:
            if yDistance == 0:
                return xDistance

            elif xDistance == 0:
                return yDistance

            else:
                return -1  # Using abs, so this works as an error code.

        elif dist_type == 1:
            return math.sqrt(xDistance * xDistance + yDistance * yDistance)

        elif dist_type == 2:
            return xDistance, yDistance

        else:
            raise TypeError


class Compass:
    def __init__(self):
        pass


class Graph:  # Weighted, undirected, cyclic.
    class Node:
        def __init__(self, coords):
            self.Coords = coords
            self.Edges = {}

        def AddEdge(self, to_node, weighting):
            self.Edges[to_node] = weighting

        def GetConnected(self):
            return [node for node in self.Edges]

        def GetWeight(self, to_node):
            return self.Edges[to_node]

        def FindShortest(self, to_node, node_array, cost):
            traversed_nodes = node_array.copy()
            traversed_nodes.append(self)

            if self == to_node:
                return traversed_nodes, cost

            else:
                shortest = (None, -1)

                for node in self.GetConnected():
                    if node not in traversed_nodes:
                        this_traversal = node.FindShortest(to_node, traversed_nodes, cost + self.Edges[node])

                        if shortest[1] == -1 or shortest[1] > this_traversal[1]:
                            shortest = this_traversal

                return shortest

    def __init__(self):
        self.Nodes = {}

    def AddNode(self, coords):
        self.Nodes[coords] = self.Node(coords)

    def AddEdge(self, coords_a, coords_b, weighting):
        self.Nodes[coords_a].AddEdge(self.Nodes[coords_b], weighting)
        self.Nodes[coords_b].AddEdge(self.Nodes[coords_a], weighting)

    def Shortest(self, start_coords, end_coords):
        print(100)
        shortest = self.Nodes[start_coords].FindShortest(self.Nodes[end_coords], [], 0)
        print(500)
        return [node.Coords for node in shortest[0]], shortest[1]


class CoordGraph(Graph):
    def __init__(self):
        super().__init__()
        self.coordinates = []

    def CreateGraph(self, coordinates):
        # Each coordinate held in coordinates is expressed as (x-coordinate, y-coordinate, level).
        self.coordinates = coordinates

        coord_set = set()

        [coord_set.add(coords) for coords in coordinates]

        [self.AddNode(coords) for coords in coordinates]

        NE = False
        SE = False
        SW = False
        NW = False

        for x, y in coord_set:
            if (x - 1, y) in coord_set:
                self.AddEdge((x, y), (x - 1, y), 1)
                SW = True
                NW = True

            if (x + 1, y) in coord_set:
                self.AddEdge((x, y), (x + 1, y), 1)
                NE = True
                SE = True

            if (x, y - 1) in coord_set:
                self.AddEdge((x, y), (x, y - 1), 1)

                if NE and (x + 1, y - 1) in coord_set:
                    self.AddEdge((x, y), (x + 1, y - 1), 1.41)

                if NW and (x - 1, y - 1) in coord_set:
                    self.AddEdge((x, y), (x - 1, y - 1), 1.41)

            if (x, y + 1) in coord_set:
                self.AddEdge((x, y), (x, y + 1), 1)

                if SE and (x + 1, y + 1) in coord_set:
                    self.AddEdge((x, y), (x + 1, y + 1), 1.41)

                if SW and (x - 1, y + 1) in coord_set:
                    self.AddEdge((x, y), (x - 1, y + 1), 1.41)

    def GetTiles(self):
        return self.coordinates


class MapGraph:
    def __init__(self):
        self.levels = []

    def CreateGraphs(self, interior_tiles):
        self.levels = []
        for level in range(len(interior_tiles)):
            self.levels.append(CoordGraph())
            self.levels[level].CreateGraph(interior_tiles[level])

    def GetGraph(self, level):
        return self.levels[level]

    def GetShortest(self, level, start_coordinates, end_coordinates):
        return self.GetGraph(level).Shortest(start_coordinates, end_coordinates)

    def AsArray(self):
        return [self.GetGraph(level).GetTiles() for level in range(len(self.levels))]


current_map_data = MapData()
save_data = None

if __name__ == '__main__':
    BeginGame()

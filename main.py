import random
import math
from matplotlib import pyplot as plt
from pathlib import Path

### Simulation Parameters ###
simulation_count = 100000
leader = 0
artillery = 0
blockade = False
fort = 2
breach = False


class Siege:

    def __init__(self, leader:int=0, artillery:int = 0, blockade: bool=False, fort:int = 2, breach:int = 0) -> None:
        self.leader = leader                # Leader bonus
        self.artillery = artillery          # Artillery bonus
        self.blockade = blockade * 2 - 2    # 0 if no blockade, -2 if blockade
        self.fort = fort                    # Fort level, applied as negative
        self.breach = breach                # Breach bonus

        self.siege_progress = 0

    def __find_win_prob(self):
        progress = self.leader + self.artillery + self.blockade - self.fort + self.breach + self.siege_progress
        win_prob = (progress - 5) / 14
        return 100 * round(win_prob, 4)
    
    def __find_total_progress(self):
        progress = self.leader + self.artillery + self.blockade - self.fort + self.breach + self.siege_progress
        return progress
    
    def get_advantage(self):
        return self.leader + self.artillery + self.blockade - self.fort
    
    def get_progress(self):
        return self.__find_win_prob()

    
    def __siege_progress(self, roll, siege_roll):
        # Surrender check
        if siege_roll >= 20:
            return True
        # Disease outbreak check
        if roll == 1:
            return False
        # Breach
        if roll + self.artillery / 3 + self.fort / 10 >= 14:
            if self.breach <= 3:
                self.breach += 1
            self.siege_progress += 2
        # Supplies shortage
        elif siege_roll >= 5 and siege_roll <= 11:
            self.siege_progress += 1
        # Food shortage
        elif siege_roll >= 12 and siege_roll <= 13:
            self.siege_progress += 2
        # Water shortage
        elif siege_roll >= 14 and siege_roll <= 15:
            self.siege_progress += 3
        # Defenders desert
        elif siege_roll >= 16 and siege_roll <= 19:
            self.siege_progress += 2
        # The remaining rolls are status quo
        # Check max progress
        if self.fort <= 2:
            max_progress = 12
        else:
            max_progress = 11 + math.floor(self.fort / 2)
        if self.siege_progress > max_progress:
            self.siege_progress = max_progress
        return False
            

    def progress(self, verbose=False):
        # Get a roll
        roll = random.randint(1, 14)
        # Calculate the siege roll
        siege_roll = self.__find_total_progress() + roll
        # Progress the siege
        surrendered = self.__siege_progress(roll, siege_roll)
        # Return the results
        if verbose:
            print(roll, siege_roll)
        return surrendered, self.__find_total_progress()

def progress_2_win_prob(progress):
    win_prob = (progress - 5) / 14
    return 100 * round(win_prob, 4)
progresses = range(6, 20)
win_probs = [progress_2_win_prob(i) for i in progresses]
win_prob_counts = [0] * len(win_probs)
for i in range(simulation_count):
    siege = Siege(leader=leader, artillery=artillery, blockade=blockade, fort=fort, breach=breach)
    surrendered = False
    while not surrendered:
        surrendered, progress = siege.progress()
    win_prob_counts[progress - 6] += 1

plt.bar(win_probs, win_prob_counts, width=100/28)
plt.title(str(simulation_count) + ' simulations, advantage: ' + str(siege.get_advantage()))
plt.xlabel('Siege winning percentage')
plt.ylabel('Siege winning count')
save_path = Path(__file__).parent / 'Figures'
plt.savefig(save_path / ('Sim' + str(simulation_count) + 'Adv' + str(siege.get_advantage())))

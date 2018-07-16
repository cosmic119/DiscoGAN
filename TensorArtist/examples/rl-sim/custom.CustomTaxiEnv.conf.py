# -*- coding:utf8 -*-


def make():
    from tartist.app.rl.simulator import automake
    game = automake('custom.CustomTaxiEnv', dense_reward=True)
    # you need to restart your game here
    game.restart()
    return game

name = 'custom.CustomTaxiEnv'
action_names = ['UP', 'RIGHT', 'DOWN', 'LEFT']
action_keys = [65362, 65363, 65364, 65361]
quit_action_key = 113

# default min size is a tuple (min_dim, max_dim)
default_winsize = (600, 800)
# ignore no-action (action=0) in logging
mute_noaction = False

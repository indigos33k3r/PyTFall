label special_items_slime_bottle:
    if not(hero.has_flag("slime_bottle")):
        $ hero.set_flag("slime_bottle", value=True)
    scene bg h_profile with dissolve
    menu:
        "An old bottle with unknown, thick liquid inside. Do you want to open it?"
        "Yes":
            "The seal is durable, but eventually it gives up, and pressurized fluid breaks out."
            if hero.level <= 5:
                $ levels = randint (1,5)
            else:
                $ levels = randint(hero.level*0.7, hero.level*1.3)
            $ new_slime = build_rc(id="Slime", level=levels, pattern=choice(["Warrior", "ServiceGirl"]))
            $ new_slime.disposition += 300
            $ hero.remove_item("Unusual Bottle")
            $ spr = new_slime.get_vnsprite()
            if hero.flag("slime_bottle"):
                $ new_slime.override_portrait("portrait", "happy")
                "The liquid quickly took the form of a girl."
                show expression spr at center with dissolve
                if dice(90):
                    $ new_slime.set_status("free")
                    new_slime.say "Finally someone opened it! Thanks a lot!"
                    new_slime.say "They promised me to smuggle me in the city, but something went gone wrong, and I was trapped there for months!"
                    new_slime.say "All I wanted is a steady job and a roof over my head..."
                    menu:
                        "Propose to work for you":
                            new_slime.say "Gladly!"
                            $ hero.add_char(new_slime)
                            "Looks like you have a new worker."
                        "Leave her be":
                            "Thanks again, [hero.name]."
                            hide expression spr with dissolve
                            "She leaves."
                else:
                    $ new_slime.set_status("slave")
                    new_slime.say "Oh, hello. Are you my new owner? I was told I will be transported to a new owner inside this bottle."
                    menu:
                        "Yes":
                            new_slime.say "It's a pleasure to serve you."
                            $ hero.add_char(new_slime)
                            "Looks like you have a new slave."
                        "No":
                            $ new_slime.override_portrait("portrait", "sad")
                            new_slime.say "Oh, this is bad... What should I do now? I guess I'll try to find my old master then..."
                            menu:
                                "Propose to become her owner":
                                    $ new_slime.override_portrait("portrait", "happy")
                                    $ hero.add_char(new_slime)
                                    new_slime.say "Of course! It's a pleasure to serve you."
                                    "Looks like you have a new slave."
                                "Leave her be":
                                    hide expression spr with dissolve
                                    "She leaves."
            else:
                $ new_slime.override_portrait("portrait", "angry")
                "The liquid quickly took the form of a girl."
                show expression spr at center with dissolve
                new_slime.say "AAAAGHHHHHH!"
                "She attack you!"
                $ new_slime.front_row = True
                $ enemy_team = Team(name="Enemy Team", max_size=3)
                $ enemy_team.add(new_slime)
                $ result = run_default_be(enemy_team, slaves=True, background="content/gfx/bg/be/b_dungeon_1.jpg", track="random", prebattle=True, death=True)
                if not(result):
                    jump game_over
                else:
                    scene bg h_profile
                    "You managed to beat her. Her liquid body quickly decays. Looks like she spent way too much time in that bottle..."
                    $ new_slime.health = 0
                    python:
                        for member in hero.team:
                            member.exp += adjust_exp(member, 200)
                        
        "No":
            "Maybe another time."
            jump char_equip
    $ new_slime.restore_portrait()
    if dice(50): # no easy save scumming
        $ hero.set_flag("slime_bottle", value=True)
    else:
        $ hero.set_flag("slime_bottle", value=False)
    jump char_equip
    
label special_items_empty_extractor:
    scene bg h_profile with dissolve
    if eqtarget.exp <= 2000:
        if eqtarget<>hero:
            "Unfortunately, [eqtarget] is not experienced enough yet to share her knowledge with anybody."
        else:
            "Unfortunately, you are not experienced enough yet to share your knowledge with anybody."
        jump char_equip
    else:
        if eqtarget<>hero:
            "This device will extract some of [eqtarget.name]'s experience."
        else:
            "This device will extract some of your experience."
        menu:
            "Do you want to use it?"
            "Yes":
                if eqtarget<>hero:
                    "She slightly shudders when the device starts to work."
                    $ eqtarget.disposition -= randint(20, 30)
                else:
                    "For a moment you feel weak, but unpleasant pain somewhere inside your head."
                $ eqtarget.exp -= 2000
                $ eqtarget.remove_item("Empty Extractor", 1)
                $ eqtarget.add_item("Full Extractor", 1)
                "The device is full of energy."
            "No":
                $ pass
jump char_equip

label special_items_full_extractor:
    scene bg h_profile with dissolve
    if eqtarget<>hero:
        "The energy of knowledge slowly flows inside [eqtarget.name]. She became more experienced."
    else:
        "The energy of knowledge slowly flows inside you. You became more experienced."
    $ eqtarget.exp += 1000
    "The device does not work any longer."
    $ eqtarget.remove_item("Full Extractor", 1)
jump char_equip
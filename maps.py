maps = [['    F',
         '   *#',
         '  *##',
         ' *###',
         'S####',
         '#####'],

        ['         ',
         '      *  ',
         '  * *   F',
         'S    # ##',
         '## # # ##',
         '##-#-#-##'],

        ['         ',
         '         ',
         '  * * *  ',
         'S       F',
         '# + + + #',
         '#--------'],

        ['         ',
         '         ',
         '  * *    ',
         'S     * F',
         '##  #  ##',
         '##--#--##'],

        ['        ',
         '       F',
         ' ***  ##',
         '    ####',
         '    ####',
         'S   ####',
         '#^^^####'],

        ['        ',
         '       F',
         '   *#++#',
         '  # #--#',
         '  # ####',
         'S *    *',
         '#^#^####'],

        ['         ',
         '      *  ',
         '        F',
         '  *     #',
         'S   ++^+*',
         '##-#--#-#'],

        ['              ',
         '       *     F',
         'S      +    +#',
         '#+++#      +  ',
         '#+*+##    + * ',
         '#+++###--#  ^ ',
         '#---######----'],

        ['         #           ',
         '         #           ',
         'S        #           ',
         '#+  +    #*    +    F',
         '#   *    ##  #+  +  #',
         '#   +        # *+   #',
         '#            # +    #',
         '#-------####^#------#'],

        ['#     #         #',
         '#    S#F        #',
         '# +  #####  ## ##',
         '# +      #      #',
         '#*+      #      #',
         '#++  #+++#    ^ #',
         '#----#   #      #',
         '######          #',
         '## *           ^#',
         '##              #',
         '######     +    #',
         '######   ##*  ^##',
         '######---###--###'],

        ['          ',
         ' *        ',
         ' #   S    ',
         '----##### ',
         '          ',
         '          ',
         '  ####### ',
         '      #   ',
         '     *#*  ',
         '  ######^-',
         '          ',
         '          ',
         '    #    F',
         '#####---##'],

        ['        ',
         '   S    ',
         '   #    ',
         '        ',
         '        ',
         '++++++++',
         '+*++++++',
         '++++++++',
         '---+++++',
         '+++++++*',
         '++++++++',
         '     ---',
         '  *  ###',
         '       #',
         '     F #',
         '---#####'],

        ['    # # # # ',
         '    # # # # ',
         '    # # # * ',
         '    # # * # ',
         '    # * # # ',
         '      # # # ',
         '    # # # # ',
         'S          F',
         '#^^-#####-##'],

        ['####              ',
         '# *#   F          ',
         '# ##   #          ',
         '#           #     ',
         '#          # #    ',
         '#^## #^##   # #  *',
         '#        #   #    ',
         '#         #       ',
         '#*  ^   S ##     ^',
         '###----#######---#'],

        ['         ',
         '    *    ',
         '    +    ',
         ' +       ',
         '         ',
         ' *       ',
         '^+      F',
         '    #   #',
         'S  #  # *',
         '#-------#'],

        ['                                        ',
         '     F                                  ',
         '  #######                               ',
         '           +                    --#     ',
         '        # +                    #####    ',
         '        #+                     #    #   ',
         '       ^#    ++     #        --#    # ^ ',
         '        # #      #  #--#--#    #    #   ',
         '        # ##     #  ####### ^  # S      ',
         '       ^# #-     #^ #  #  #    #####   ^',
         '        # #      #  #  #    -  #    +++ ',
         '        # # ^    #     *     ^ #        ',
         '  -    ^# # #    # ^#  #  #    *        ',
         '  #       #* # # #  #  #  #    #        ',
         '  #---    #^     #  #  #  #   ^#  #     ',
         '   ###^^ + #-#-###  #  #  #    #     +  ',
         '                                        ']]

# easy
map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, -2],
        [0, 3, 0, 3, 0, 0, 1, 0, 1],
        [-1, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 2, 2, 2, 2, 2, 2, 2, 2]]
# hard
maps1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [3, 0, 3, 0, 0, 0, 0, 0, 0],
         [1, 0, 1, 0, 0, 0, 0, 0, -2],
         [0, 0, 0, 0, 1, 0, 0, 0, 1],
         [-1, 0, 0, 1, 0, 0, 1, 0, 3],
         [1, 2, 2, 2, 2, 2, 2, 2, 1]]

map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 3, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, -2],
        [0, 0, 0, 0, 1, 0, 0, 0, 1],
        [-1, 0, 0, 1, 0, 0, 1, 0, 3],
        [1, 2, 2, 2, 2, 2, 2, 2, 1]]

map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 3, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, -2],
        [0, 0, 0, 0, 1, 0, 0, 0, 1],
        [-1, 0, 4, 1, 0, 0, 1, 0, 3],
        [1, 2, 2, 2, 2, 2, 2, 2, 1]]

l16 = ['                                               ',
       '                                               ',
       '                       ######## ############## ',
       '                       #     #               # ',
       '                       # ##### ########### # # ',
       '                      ^# #     #     #   # # # ',
       '                       # # ##### ### # ### # # ',
       '     + ++              # #     #   # #     # # ',
       '  #---------#######  ^ # # ### ##### #^####### ',
       '# #################    #   # # #               ',
       '  # # #  *             # #^# # # ############# ',
       '           #        ^  #     #               # ',
       ' ^#-#-#-#--#############^#######^############# ',
       '                       #                       ',
       '                       #   F                   ',
       '^S                     # #####                 ',
       ' #                     #     #+                ',
       '                       #     # #  # ## #  ###  ',
       '                       #     # #  # # # # #  # ',
       '                       # #   # #  # # # # #  # ',
       '                       #  ###   ### # # # ###  ',
       '                       #                  #    ',
       '                       #                  #    ',
       '                       #                  #    ',
       '########################                       ']
